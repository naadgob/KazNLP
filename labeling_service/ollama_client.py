"""Ollama local LLM client with streaming, quality modes, mixed verification."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import Any, AsyncIterator

import httpx

from label_utils import extract_json_array, normalize_label
from prompts import (
    VERIFY_SYSTEM,
    build_user_prompt,
    build_verify_prompt,
    get_quality_config,
    get_quality_mode,
    get_system_prompt,
)

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
INITIAL_BACKOFF = 2.0
DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen2.5:3b"


def get_batch_size() -> int:
    return int(get_quality_config()["batch_size"])


BATCH_SIZE = get_batch_size()


def get_config() -> tuple[str, str]:
    base_url = os.getenv("OLLAMA_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    model = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
    return base_url, model


def is_configured() -> bool:
    return True


def _ollama_options() -> dict[str, Any]:
    return {
        "temperature": 0,
        "num_ctx": int(os.getenv("OLLAMA_NUM_CTX", "8192")),
        "top_p": 0.9,
        "repeat_penalty": 1.1,
    }


async def check_connection() -> dict[str, Any]:
    base_url, model = get_config()
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{base_url}/api/tags")
        resp.raise_for_status()
        names = {m["name"] for m in resp.json().get("models", [])}
        model_ok = model in names or any(
            n == model or n.startswith(f"{model}:") or model.startswith(n.split(":")[0] + ":")
            for n in names
        )
        return {
            "reachable": True,
            "model": model,
            "model_installed": model_ok,
            "installed": sorted(names),
            "quality_mode": get_quality_mode(),
        }


async def _chat_once(system: str, user: str) -> str:
    base_url, model = get_config()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": _ollama_options(),
    }
    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(600.0, connect=10.0)) as client:
                resp = await client.post(f"{base_url}/api/chat", json=payload)
                resp.raise_for_status()
                return resp.json().get("message", {}).get("content", "")
        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(INITIAL_BACKOFF * (2**attempt))
                continue
            raise
    raise last_error or RuntimeError("Ollama chat failed")


async def _run_chat_streaming(system: str, user: str) -> AsyncIterator[dict[str, Any]]:
    base_url, model = get_config()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": True,
        "options": _ollama_options(),
    }

    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        raw_parts: list[str] = []
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(600.0, connect=10.0)) as client:
                async with client.stream("POST", f"{base_url}/api/chat", json=payload) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line.strip():
                            continue
                        data = json.loads(line)
                        chunk = data.get("message", {}).get("content", "")
                        if chunk:
                            raw_parts.append(chunk)
                            yield {"type": "chunk", "text": chunk}
                        if data.get("done"):
                            break

            parsed = extract_json_array("".join(raw_parts))
            labels = [normalize_label(x) for x in parsed]
            yield {"type": "result", "labels": labels, "raw": "".join(raw_parts)}
            return

        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES - 1:
                wait = INITIAL_BACKOFF * (2**attempt)
                logger.warning("Ollama batch failed (attempt %s), retry in %.1fs: %s", attempt + 1, wait, exc)
                await asyncio.sleep(wait)
                continue
            raise

    raise last_error or RuntimeError("Ollama batch labeling failed")


async def _verify_mixed_labels(items: list[dict], labels: list[dict]) -> list[dict]:
    text_by_id = {int(i["row_id"]): i["text"] for i in items}
    mixed = [lab for lab in labels if lab["language"] == "mixed"]
    if not mixed:
        return labels

    verify_items = [{"row_id": m["row_id"], "text": text_by_id.get(int(m["row_id"]), "")} for m in mixed]
    raw = await _chat_once(VERIFY_SYSTEM, build_verify_prompt(verify_items, mixed))
    verified = [normalize_label(x) for x in extract_json_array(raw)]

    by_id = {int(lab["row_id"]): lab for lab in labels}
    for v in verified:
        by_id[int(v["row_id"])] = v

    return [by_id[int(i["row_id"])] for i in items if int(i["row_id"]) in by_id]


async def stream_label_batch(items: list[dict]) -> AsyncIterator[dict[str, Any]]:
    cfg = get_quality_config()
    system = get_system_prompt()
    user_prompt = build_user_prompt(items)

    labels: list[dict] = []
    raw = ""

    async for event in _run_chat_streaming(system, user_prompt):
        if event["type"] == "chunk":
            yield event
        elif event["type"] == "result":
            labels = event["labels"]
            raw = event["raw"]

    if cfg.get("verify_mixed") and labels:
        yield {"type": "chunk", "text": "\n[verify mixed...]\n"}
        labels = await _verify_mixed_labels(items, labels)
        raw += "\n/* verified mixed */"

    yield {"type": "result", "labels": labels, "raw": raw}
