"""Route labeling requests to Gemini or Ollama with full quality pipeline."""

from __future__ import annotations

import os
from typing import Any, AsyncIterator

import gemini_client
import ollama_client
from label_enhance import refine_llm_labels, use_precision_filter
from prompts import get_quality_mode


def get_provider() -> str:
    return os.getenv("LABELER_PROVIDER", "ollama").strip().lower()


def get_batch_size() -> int:
    if get_provider() == "gemini":
        return gemini_client.get_batch_size()
    return ollama_client.get_batch_size()


def is_configured() -> bool:
    if get_provider() == "gemini":
        return bool(os.getenv("GEMINI_API_KEY"))
    return ollama_client.is_configured()


async def get_provider_info() -> dict[str, Any]:
    provider = get_provider()
    base: dict[str, Any] = {
        "quality_mode": get_quality_mode(),
        "precision_filter": use_precision_filter(),
        "batch_size": get_batch_size(),
    }
    if provider == "gemini":
        return {
            "provider": "gemini",
            "configured": is_configured(),
            "model": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            **base,
        }
    base_url, model = ollama_client.get_config()
    info: dict[str, Any] = {
        "provider": "ollama",
        "configured": True,
        "model": model,
        "base_url": base_url,
        **base,
    }
    try:
        conn = await ollama_client.check_connection()
        info.update(conn)
    except Exception as exc:
        info["reachable"] = False
        info["error"] = str(exc)
    return info


async def stream_label_batch(items: list[dict]) -> AsyncIterator[dict[str, Any]]:
    if get_provider() == "gemini":
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY is not set. Add it to .env or switch LABELER_PROVIDER=ollama")
        stream_fn = gemini_client.stream_label_batch
    else:
        stream_fn = ollama_client.stream_label_batch

    labels: list[dict] = []
    raw = ""

    async for event in stream_fn(items):
        if event["type"] == "chunk":
            yield event
        elif event["type"] == "result":
            labels = event["labels"]
            raw = event["raw"]

    if use_precision_filter() and labels:
        labels, n_changed = refine_llm_labels(items, labels)
        if n_changed:
            yield {"type": "chunk", "text": f"\n[precision filter: {n_changed} labels adjusted]\n"}
        raw += "\n/* precision_filter */"

    yield {"type": "result", "labels": labels, "raw": raw}
