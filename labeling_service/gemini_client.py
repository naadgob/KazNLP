"""Gemini API client with streaming, retries, and JSON parsing."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any, AsyncIterator

from google import genai
from google.genai import types

from label_utils import extract_json_array, normalize_label
from prompts import (
    VERIFY_SYSTEM,
    build_user_prompt,
    build_verify_prompt,
    get_quality_config,
    get_system_prompt,
)

logger = logging.getLogger(__name__)

def get_batch_size() -> int:
    return int(get_quality_config().get("batch_size", 25))


BATCH_SIZE = get_batch_size()
MAX_RETRIES = 5
INITIAL_BACKOFF = 2.0


def get_client() -> tuple[genai.Client, str]:
    import os

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Add it to .env in project root.")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return genai.Client(api_key=api_key), model


def _is_retryable_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return (
        "429" in msg
        or "503" in msg
        or "rate" in msg
        or "quota" in msg
        or "resource_exhausted" in msg
        or "unavailable" in msg
    )


def _parse_retry_seconds(exc: Exception) -> float | None:
    msg = str(exc)
    m = re.search(r"retry in ([0-9.]+)s", msg, re.I)
    if m:
        return float(m.group(1)) + 1.0
    return None


def _extract_json_array(raw: str) -> list[dict]:
    return extract_json_array(raw)


def _normalize_label(item: dict) -> dict[str, Any]:
    return normalize_label(item)


async def _verify_mixed_labels(items: list[dict], labels: list[dict]) -> list[dict]:
    text_by_id = {int(i["row_id"]): i["text"] for i in items}
    mixed = [lab for lab in labels if lab["language"] == "mixed"]
    if not mixed:
        return labels

    client, model = get_client()
    verify_items = [{"row_id": m["row_id"], "text": text_by_id.get(int(m["row_id"]), "")} for m in mixed]
    config = types.GenerateContentConfig(
        temperature=0,
        system_instruction=VERIFY_SYSTEM,
        response_mime_type="application/json",
    )
    resp = await client.aio.models.generate_content(
        model=model,
        contents=build_verify_prompt(verify_items, mixed),
        config=config,
    )
    raw = resp.text or ""
    verified = [_normalize_label(x) for x in _extract_json_array(raw)]
    by_id = {int(lab["row_id"]): lab for lab in labels}
    for v in verified:
        by_id[int(v["row_id"])] = v
    return [by_id[int(i["row_id"])] for i in items if int(i["row_id"]) in by_id]


async def stream_label_batch(items: list[dict]) -> AsyncIterator[dict[str, Any]]:
    """
    Async generator: yields {"type": "chunk", "text": "..."} then
    {"type": "result", "labels": [...], "raw": "..."}.
    """
    client, model = get_client()
    user_prompt = build_user_prompt(items)
    config = types.GenerateContentConfig(
        temperature=0,
        system_instruction=get_system_prompt(),
        response_mime_type="application/json",
    )

    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        raw_parts: list[str] = []
        try:
            stream = await client.aio.models.generate_content_stream(
                model=model,
                contents=user_prompt,
                config=config,
            )
            async for chunk in stream:
                if chunk.text:
                    raw_parts.append(chunk.text)
                    yield {"type": "chunk", "text": chunk.text}

            raw = "".join(raw_parts)
            parsed = _extract_json_array(raw)
            labels = [_normalize_label(x) for x in parsed]
            if get_quality_config().get("verify_mixed"):
                yield {"type": "chunk", "text": "\n[verify mixed...]\n"}
                labels = await _verify_mixed_labels(items, labels)
                raw += "\n/* verified mixed */"
            yield {"type": "result", "labels": labels, "raw": raw}
            return

        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES - 1:
                if _is_retryable_error(exc):
                    wait = _parse_retry_seconds(exc) or INITIAL_BACKOFF * (2**attempt)
                    logger.warning("Retryable error (attempt %s), waiting %.1fs", attempt + 1, wait)
                else:
                    wait = INITIAL_BACKOFF * (2**attempt)
                    logger.warning("Batch failed (attempt %s), retry in %.1fs: %s", attempt + 1, wait, exc)
                await asyncio.sleep(wait)
                raw_parts.clear()
                continue
            raise

    raise last_error or RuntimeError("Batch labeling failed")
