"""FastAPI language labeling service with SSE streaming."""

from __future__ import annotations

import asyncio
import json
import logging
import math
import os
import time
from pathlib import Path
from typing import Any, AsyncIterator

import httpx
from dotenv import load_dotenv
from fastapi import Body, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

from csv_processor import (
    apply_labels,
    ensure_output_columns,
    export_counts,
    export_dataframe,
    init_job,
    job_dir,
    language_stats,
    load_dataframe,
    load_state,
    rows_to_process,
    save_output,
    save_state,
    EXPORT_MODES,
)
from label_enhance import use_precision_filter
from llm_provider import get_batch_size, get_provider_info, is_configured, stream_label_batch
from job_cache import flush_job_save, flush_state, load_job_dataframe, load_job_state, pending_save_labels, schedule_state_save
from manual_labeling import (
    CONSUMING_FILTERS,
    DOMAIN_FILTERS,
    TONE_CONSUMING_FILTERS,
    apply_manual_label,
    apply_manual_sentiment,
    compute_metrics,
    filter_catalog,
    get_or_build_metrics,
    row_dict,
    undo_manual,
    FILTERS,
    CLASS_FILTERS,
)
from precision_filter import refine_dataframe
from queue_engine import queue_batch, queue_page, queue_shuffle_batch
from translate import translate_to_russian

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="KazNLP Language Labeler", version="1.0.0")
BASE = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
templates = Jinja2Templates(directory=BASE / "templates")

def sse_event(event: str, data: dict | str) -> str:
    payload = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    info = await get_provider_info()
    return templates.TemplateResponse(
        request,
        "index.html",
        {"provider_info": info},
    )


@app.get("/api/health")
async def health() -> dict:
    info = await get_provider_info()
    return {"status": "ok", **info}


@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    try:
        job_id, stats = init_job(content, file.filename or "upload.csv")
        load_job_dataframe(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"job_id": job_id, **stats}


async def run_labeling(
    job_id: str,
    only_empty: bool,
    resume: bool,
) -> AsyncIterator[str]:
    d = job_dir(job_id)
    input_path = d / "input.csv"
    output_path = d / "output.csv"

    if not input_path.exists():
        yield sse_event("label_error", {"message": "Job not found"})
        return

    try:
        df = load_dataframe(output_path if output_path.exists() else input_path)
        df = ensure_output_columns(df.copy())
    except ValueError as exc:
        yield sse_event("label_error", {"message": str(exc)})
        return

    state = load_state(job_id) or {}
    checkpoint: set[int] = set(state.get("labeled_indices", []))
    skip = checkpoint if resume else set()

    indices = rows_to_process(df, only_empty=only_empty, resume_from=skip)

    total = len(indices)
    stats = language_stats(df)
    num_batches = math.ceil(total / get_batch_size()) if total else 0
    start_time = time.time()
    processed = 0

    yield sse_event(
        "progress",
        {
            "processed": 0,
            "total": total if total else len(df),
            "percent": 100.0 if total == 0 else 0.0,
            "stats": stats,
            "message": f"Starting: {total} rows in {num_batches} batches",
        },
    )

    if total == 0:
        save_output(df, job_id)
        save_state(job_id, {**state, "done": True, "stats": stats})
        yield sse_event(
            "done",
            {
                "job_id": job_id,
                "stats": stats,
                "processed": 0,
                "message": (
                    "Nothing to label: 0 rows queued. "
                    "Uncheck Resume to run again, or enable 'only empty language', "
                    "or clear the language column in CSV for a full LLM pass."
                ),
            },
        )
        return

    batch_size = get_batch_size()
    for batch_num in range(num_batches):
        batch_start = batch_num * batch_size
        batch_indices = indices[batch_start : batch_start + batch_size]
        items = [{"row_id": idx, "text": str(df.at[idx, "text"])} for idx in batch_indices]

        yield sse_event(
            "batch_start",
            {
                "batch": batch_num + 1,
                "total_batches": num_batches,
                "rows": batch_indices,
            },
        )

        labels: list[dict] = []
        raw = ""
        try:
            async for event in stream_label_batch(items):
                if event["type"] == "chunk":
                    yield sse_event("llm_chunk", {"text": event["text"], "batch": batch_num + 1})
                elif event["type"] == "result":
                    labels = event["labels"]
                    raw = event["raw"]
        except Exception as exc:
            logger.exception("Batch %s failed", batch_num + 1)
            save_output(df, job_id)
            yield sse_event("label_error", {"message": str(exc), "batch": batch_num + 1})
            return

        apply_labels(df, labels)
        stats = language_stats(df)
        for item in labels:
            checkpoint.add(item["row_id"])
            yield sse_event(
                "row_labeled",
                {
                    "row_id": item["row_id"],
                    "language": item["language"],
                    "confidence": item.get("confidence"),
                    "needs_review": item.get("needs_review"),
                },
            )

        processed += len(batch_indices)
        save_output(df, job_id)
        elapsed = time.time() - start_time
        eta = (elapsed / processed) * (total - processed) if processed else None

        save_state(
            job_id,
            {
                **state,
                "done": False,
                "processed": processed + len(skip),
                "total_to_process": total,
                "only_empty": only_empty,
                "stats": stats,
                "labeled_indices": sorted(checkpoint),
            },
        )

        yield sse_event(
            "batch_done",
            {
                "batch": batch_num + 1,
                "total_batches": num_batches,
                "raw_preview": raw[:500],
                "labels_count": len(labels),
            },
        )

        yield sse_event(
            "progress",
            {
                "processed": processed,
                "total": total,
                "stats": stats,
                "eta_seconds": round(eta, 1) if eta is not None else None,
                "percent": round(100 * processed / total, 1),
            },
        )

        await asyncio.sleep(float(os.getenv("BATCH_DELAY_SEC", "1.0")))

    if use_precision_filter():
        yield sse_event("batch_start", {"batch": 0, "total_batches": 0, "rows": [], "message": "final precision pass"})
        before_mixed = sum(1 for i in range(len(df)) if str(df.at[i, "language"]).lower() == "mixed")
        df = refine_dataframe(df)
        after_mixed = sum(1 for i in range(len(df)) if str(df.at[i, "language"]).lower() == "mixed")
        save_output(df, job_id)
        stats = language_stats(df)
        yield sse_event(
            "llm_chunk",
            {"text": f"\n[final filter: mixed {before_mixed} -> {after_mixed}]\n", "batch": 0},
        )

    save_state(
        job_id,
        {
            **state,
            "done": True,
            "processed": processed,
            "total_to_process": total,
            "only_empty": only_empty,
            "stats": stats,
            "labeled_indices": sorted(checkpoint),
        },
    )
    yield sse_event("done", {"job_id": job_id, "stats": stats, "processed": processed})


@app.get("/api/jobs/{job_id}/label")
async def label_stream(
    job_id: str,
    only_empty: bool = Query(False),
    resume: bool = Query(False),
) -> StreamingResponse:
    if not is_configured():
        raise HTTPException(
            status_code=503,
            detail="LLM not configured. Set LABELER_PROVIDER=ollama (default) or GEMINI_API_KEY for gemini.",
        )

    async def event_generator() -> AsyncIterator[str]:
        async for event in run_labeling(job_id, only_empty, resume):
            yield event

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/jobs/{job_id}/status")
async def job_status(job_id: str) -> dict[str, Any]:
    state = load_state(job_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return state


@app.get("/api/jobs/{job_id}/download")
async def download_result(
    job_id: str,
    mode: str = Query("full"),
) -> FileResponse:
    if mode not in EXPORT_MODES:
        raise HTTPException(
            status_code=400,
            detail=f"mode must be one of: {', '.join(sorted(EXPORT_MODES))}",
        )
    flush_job_save(job_id)
    state = load_job_state(job_id)
    if state:
        flush_state(job_id, state)
    df = _job_df_or_404(job_id)
    counts = export_counts(df)
    if mode != "full" and counts[mode] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No rows to export for mode '{mode}'",
        )

    suffix = {"full": "full", "labeled": "labeled", "manual": "manual_gold"}[mode]
    out = job_dir(job_id) / f"export_{suffix}.csv"
    export_df = export_dataframe(df, mode)
    export_df.to_csv(out, index=False, encoding="utf-8-sig")
    return FileResponse(
        out,
        media_type="text/csv",
        filename=f"dataset_{suffix}_{job_id}.csv",
    )


@app.get("/api/jobs/{job_id}/export/info")
async def export_info(job_id: str) -> dict[str, Any]:
    state = load_job_state(job_id)
    snap = state.get("metrics_snapshot")
    if snap:
        counts = {
            "total": snap["total"],
            "full": snap["total"],
            "labeled": snap["labeled"],
            "manual": snap.get("manual_count", 0),
            "unlabeled": snap.get("unlabeled", 0),
        }
    else:
        df = _job_df_or_404(job_id)
        counts = export_counts(df)
    return {
        "modes": sorted(EXPORT_MODES),
        "counts": counts,
        "default_mode": "labeled" if counts["labeled"] < counts["total"] else "full",
        "pending_patches": pending_save_labels(job_id),
    }


def _job_df_or_404(job_id: str):
    try:
        return load_job_dataframe(job_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Job not found") from exc


@app.get("/api/jobs/{job_id}/metrics")
async def job_metrics(job_id: str) -> dict[str, Any]:
    df = _job_df_or_404(job_id)
    state = load_job_state(job_id)
    metrics = get_or_build_metrics(df, state)
    if state.get("metrics_snapshot") != metrics:
        schedule_state_save(job_id, {**state, "metrics_snapshot": metrics})
    return metrics


@app.get("/api/manual/filters")
async def manual_filters() -> dict[str, Any]:
    return filter_catalog()


@app.get("/api/jobs/{job_id}/manual/queue")
async def manual_queue(
    job_id: str,
    filter: str = Query("unlabeled", alias="filter"),
    search: str = Query(""),
    class_filter: str = Query("any"),
    domain_filter: str = Query("any"),
    position: int = Query(0, ge=0),
    batch: int = Query(1, ge=1, le=50),
    lite: bool = Query(True),
    include_row: bool = Query(True),
) -> dict[str, Any]:
    if filter not in FILTERS:
        filter = "unlabeled"
    if class_filter not in CLASS_FILTERS:
        class_filter = "any"
    if domain_filter not in DOMAIN_FILTERS:
        domain_filter = "any"
    df = _job_df_or_404(job_id)
    consuming = sorted(CONSUMING_FILTERS if filter not in TONE_CONSUMING_FILTERS else TONE_CONSUMING_FILTERS)
    if batch > 1:
        page = queue_batch(job_id, df, filter, search.strip(), class_filter, domain_filter, position, batch)
        result: dict[str, Any] = {
            "filter": filter,
            "search": search,
            "class_filter": class_filter,
            "domain_filter": domain_filter,
            "consuming_filters": consuming,
            **page,
        }
        if include_row:
            for item in page["rows"]:
                item["row"] = row_dict(df, int(item["row_id"]), lite=lite)
        if page["rows"]:
            first = page["rows"][0]
            result["row_id"] = first["row_id"]
            result["position"] = first["position"]
            if include_row:
                result["row"] = first.get("row")
        else:
            result["row_id"] = None
            result["position"] = 0
        return result

    page = queue_page(job_id, df, filter, search.strip(), class_filter, domain_filter, position)
    result = {
        "filter": filter,
        "search": search,
        "class_filter": class_filter,
        "domain_filter": domain_filter,
        "consuming_filters": consuming,
        **page,
    }
    if include_row and page.get("row_id") is not None:
        result["row"] = row_dict(df, int(page["row_id"]), lite=lite)
    return result


@app.get("/api/jobs/{job_id}/manual/shuffle")
async def manual_shuffle(
    job_id: str,
    filter: str = Query("unlabeled", alias="filter"),
    search: str = Query(""),
    class_filter: str = Query("any"),
    domain_filter: str = Query("any"),
    batch: int = Query(20, ge=1, le=50),
    lite: bool = Query(True),
) -> dict[str, Any]:
    if filter not in FILTERS:
        filter = "unlabeled"
    if class_filter not in CLASS_FILTERS:
        class_filter = "any"
    if domain_filter not in DOMAIN_FILTERS:
        domain_filter = "any"
    df = _job_df_or_404(job_id)
    consuming = sorted(CONSUMING_FILTERS if filter not in TONE_CONSUMING_FILTERS else TONE_CONSUMING_FILTERS)
    page = queue_shuffle_batch(job_id, df, filter, search.strip(), class_filter, domain_filter, batch)
    result: dict[str, Any] = {
        "filter": filter,
        "search": search,
        "class_filter": class_filter,
        "domain_filter": domain_filter,
        "consuming_filters": consuming,
        **page,
    }
    for item in page["rows"]:
        item["row"] = row_dict(df, int(item["row_id"]), lite=lite)
    if page["rows"]:
        first = page["rows"][0]
        result["row_id"] = first["row_id"]
        result["position"] = 0
        result["row"] = first.get("row")
    else:
        result["row_id"] = None
        result["position"] = 0
    return result


@app.get("/api/jobs/{job_id}/rows/{row_id}")
async def get_row(job_id: str, row_id: int) -> dict[str, Any]:
    df = _job_df_or_404(job_id)
    if row_id < 0 or row_id >= len(df):
        raise HTTPException(status_code=404, detail="Row not found")
    return row_dict(df, row_id)


@app.post("/api/jobs/{job_id}/manual/label")
async def manual_label(
    job_id: str,
    payload: dict = Body(...),
) -> dict[str, Any]:
    try:
        return apply_manual_label(
            job_id,
            int(payload["row_id"]),
            str(payload["language"]),
            needs_review=bool(payload.get("needs_review", False)),
            queue_filter=payload.get("queue_filter"),
            queue_class=str(payload.get("queue_class", "any")),
            queue_search=str(payload.get("queue_search", "")),
            queue_domain=str(payload.get("queue_domain", "any")),
            queue_position=int(payload.get("queue_position", 0)),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/jobs/{job_id}/manual/sentiment-label")
async def manual_sentiment_label(
    job_id: str,
    payload: dict = Body(...),
) -> dict[str, Any]:
    try:
        return apply_manual_sentiment(
            job_id,
            int(payload["row_id"]),
            str(payload["tone"]),
            queue_filter=payload.get("queue_filter"),
            queue_class=str(payload.get("queue_class", "any")),
            queue_search=str(payload.get("queue_search", "")),
            queue_domain=str(payload.get("queue_domain", "any")),
            queue_position=int(payload.get("queue_position", 0)),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/translate")
async def api_translate(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Machine translation hint for manual labeling (MyMemory, not LLM)."""
    text = str(body.get("text") or "")
    force = bool(body.get("force"))
    try:
        return await asyncio.to_thread(translate_to_russian, text, force=force)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Translation API error: {exc}") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=429, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/jobs/{job_id}/manual/undo")
async def manual_undo(job_id: str) -> dict[str, Any]:
    try:
        result = undo_manual(job_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if result is None:
        raise HTTPException(status_code=400, detail="Nothing to undo")
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
