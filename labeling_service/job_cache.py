"""In-memory job dataframe, fast JSONL patches, CSV flush only on export."""

from __future__ import annotations

import json
import re
import threading
import time
from typing import Any

import numpy as np
import pandas as pd

from csv_processor import ensure_output_columns, job_dir, load_dataframe, save_output

KAZ_LETTERS_RE = re.compile(r"[әіңғүұқөһ]", re.I)
PATCHES_NAME = "manual_patches.jsonl"
STATE_DEBOUNCE_SEC = 3.0

_DF_CACHE: dict[str, pd.DataFrame] = {}
_DERIVED: dict[str, bool] = {}
_QUEUE_INDEX_CACHE: dict[str, dict[str, np.ndarray]] = {}
_STATE_CACHE: dict[str, dict] = {}
_PATCH_BUFFER: dict[str, list[dict]] = {}
_state_timers: dict[str, threading.Timer] = {}
_cache_lock = threading.Lock()


def invalidate_job_cache(job_id: str) -> None:
    with _cache_lock:
        _DF_CACHE.pop(job_id, None)
        _DERIVED.pop(job_id, None)
        _QUEUE_INDEX_CACHE.pop(job_id, None)


def invalidate_queue_cache(job_id: str) -> None:
    with _cache_lock:
        _QUEUE_INDEX_CACHE.pop(job_id, None)


def get_queue_cache(job_id: str) -> dict[str, np.ndarray]:
    return _QUEUE_INDEX_CACHE.setdefault(job_id, {})


def set_queue_indices(job_id: str, key: str, indices: np.ndarray) -> None:
    with _cache_lock:
        _QUEUE_INDEX_CACHE.setdefault(job_id, {})[key] = indices


def remove_row_from_queue_caches(job_id: str, row_id: int) -> None:
    with _cache_lock:
        job_cache = _QUEUE_INDEX_CACHE.get(job_id)
        if not job_cache:
            return
        for key, indices in list(job_cache.items()):
            pos = int(np.searchsorted(indices, row_id))
            if pos < len(indices) and int(indices[pos]) == row_id:
                job_cache[key] = np.delete(indices, pos)


def ensure_derived_columns(df: pd.DataFrame, job_id: str) -> pd.DataFrame:
    if _DERIVED.get(job_id):
        return df
    texts = df["text"].astype(str)
    df["_has_kz"] = texts.str.contains(KAZ_LETTERS_RE, na=False)
    df["_has_ru_cyr"] = texts.str.contains(r"[а-яё]{3,}", na=False, regex=True)
    _DERIVED[job_id] = True
    return df


def apply_patches(df: pd.DataFrame, job_id: str) -> None:
    path = job_dir(job_id) / PATCHES_NAME
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        patch = json.loads(line)
        rid = int(patch["row_id"])
        for key in ("language", "label", "label_source", "tone_source", "needs_review", "confidence"):
            if key in patch:
                df.at[rid, key] = patch[key]


def load_job_dataframe(job_id: str) -> pd.DataFrame:
    with _cache_lock:
        cached = _DF_CACHE.get(job_id)
        if cached is not None:
            return cached

    out = job_dir(job_id) / "output.csv"
    if not out.exists():
        raise FileNotFoundError("Job not found")
    df = ensure_output_columns(load_dataframe(out))
    apply_patches(df, job_id)
    ensure_derived_columns(df, job_id)
    with _cache_lock:
        _DF_CACHE[job_id] = df
    return df


def update_cached_row(job_id: str, row_id: int, updates: dict[str, Any]) -> pd.DataFrame:
    df = load_job_dataframe(job_id)
    for col, val in updates.items():
        df.at[row_id, col] = val
    return df


def load_job_state(job_id: str) -> dict:
    with _cache_lock:
        cached = _STATE_CACHE.get(job_id)
        if cached is not None:
            return dict(cached)
    from csv_processor import load_state

    state = load_state(job_id) or {}
    with _cache_lock:
        _STATE_CACHE[job_id] = state
    return dict(state)


def _cancel_state_timer(job_id: str) -> None:
    timer = _state_timers.pop(job_id, None)
    if timer:
        timer.cancel()


def flush_state(job_id: str, state: dict) -> None:
    from csv_processor import save_state

    with _cache_lock:
        _STATE_CACHE[job_id] = state
        _cancel_state_timer(job_id)
    save_state(job_id, state)


def schedule_state_save(job_id: str, state: dict) -> None:
    with _cache_lock:
        _STATE_CACHE[job_id] = state
        _cancel_state_timer(job_id)

        def _write() -> None:
            from csv_processor import save_state

            snap = _STATE_CACHE.get(job_id, state)
            save_state(job_id, snap)

        timer = threading.Timer(STATE_DEBOUNCE_SEC, _write)
        timer.daemon = True
        _state_timers[job_id] = timer
        timer.start()


def schedule_job_save(job_id: str, row_id: int, updates: dict[str, Any]) -> None:
    payload = {"row_id": row_id, **updates, "ts": time.time()}
    with _cache_lock:
        buf = _PATCH_BUFFER.setdefault(job_id, [])
        buf.append(payload)
        if len(buf) < 5:
            return
        to_write = buf[:]
        _PATCH_BUFFER[job_id] = []

    path = job_dir(job_id) / PATCHES_NAME
    with open(path, "a", encoding="utf-8") as f:
        for item in to_write:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def flush_job_save(job_id: str) -> None:
    with _cache_lock:
        df = _DF_CACHE.get(job_id)
        to_write = _PATCH_BUFFER.pop(job_id, [])
        state = _STATE_CACHE.get(job_id)
        _cancel_state_timer(job_id)
    if to_write:
        path = job_dir(job_id) / PATCHES_NAME
        with open(path, "a", encoding="utf-8") as f:
            for item in to_write:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
    if df is None:
        df = load_job_dataframe(job_id)
    save_output(df, job_id)
    if state is not None:
        from csv_processor import save_state

        save_state(job_id, state)


def pending_save_labels(job_id: str) -> int:
    with _cache_lock:
        n = len(_PATCH_BUFFER.get(job_id, []))
    path = job_dir(job_id) / PATCHES_NAME
    if not path.exists():
        return n
    return n + sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
