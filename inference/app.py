from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from inference.config import WEB_DIR
from inference.pipeline import InferencePipeline

pipeline = InferencePipeline()
_analyze_lock = asyncio.Lock()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_task = asyncio.create_task(asyncio.to_thread(pipeline.load_all))

    async def _watch_load() -> None:
        try:
            await load_task
        except asyncio.CancelledError:
            load_task.cancel()
            raise

    watcher = asyncio.create_task(_watch_load())
    yield
    watcher.cancel()
    try:
        await watcher
    except asyncio.CancelledError:
        pass


app = FastAPI(title="KazNLP Inference", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1)
    tone_model: Literal["auto", "ru", "kz", "mixed"] = "auto"


class HealthResponse(BaseModel):
    status: str
    device: str
    models_loaded: list[str]
    loading: bool = False
    errors: dict[str, str] | None = None


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    if pipeline.status.loading:
        status = "loading"
    elif pipeline.status.ready:
        status = "ok"
    else:
        status = "degraded"
    return HealthResponse(
        status=status,
        device=pipeline.status.device,
        models_loaded=pipeline.status.models_loaded,
        loading=pipeline.status.loading,
        errors=pipeline.status.errors or None,
    )


@app.post("/analyze")
async def analyze(req: AnalyzeRequest) -> dict:
    if pipeline.status.loading:
        raise HTTPException(
            status_code=503,
            detail="Модели ещё загружаются (обычно 1–3 мин на CPU). Подождите и попробуйте снова.",
        )
    if not pipeline.status.ready:
        detail = (
            "Модели не загружены. Положите веса в models/xlm-roberta/ "
            "(xlm-r_v2.pt, tone_v1.pt) и перезапустите сервер."
        )
        if pipeline.status.errors:
            detail += " " + "; ".join(
                f"{k}: {v}" for k, v in pipeline.status.errors.items()
            )
        raise HTTPException(status_code=503, detail=detail)
    try:
        async with _analyze_lock:
            return await asyncio.to_thread(
                pipeline.analyze,
                req.text.strip(),
                req.tone_model,
            )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if WEB_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")
