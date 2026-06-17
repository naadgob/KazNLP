"""Cheap machine translation for labeler hints (not LLM)."""

from __future__ import annotations

import hashlib
import os
import re
import httpx

MYMEMORY_URL = "https://api.mymemory.translated.net/get"
MAX_CHUNK_CHARS = 450
KAZAKH_CHARS_RE = re.compile(r"[әіңғүұқөһӘІҢҒҮҰҚӨҺ]")

_cache: dict[str, str] = {}
_CACHE_MAX = 8000


def _cache_get(key: str) -> str | None:
    return _cache.get(key)


def _cache_set(key: str, value: str) -> None:
    if len(_cache) >= _CACHE_MAX:
        _cache.clear()
    _cache[key] = value


def needs_translation(text: str) -> bool:
    t = (text or "").strip()
    if len(t) < 2:
        return False
    return bool(KAZAKH_CHARS_RE.search(t))


def _chunks(text: str, max_len: int = MAX_CHUNK_CHARS) -> list[str]:
    text = text.strip()
    if len(text) <= max_len:
        return [text]
    parts: list[str] = []
    buf: list[str] = []
    size = 0
    for word in re.split(r"(\s+)", text):
        if size + len(word) > max_len and buf:
            parts.append("".join(buf).strip())
            buf = [word]
            size = len(word)
        else:
            buf.append(word)
            size += len(word)
    if buf:
        parts.append("".join(buf).strip())
    return [p for p in parts if p]


def _mymemory_chunk(text: str, langpair: str, email: str | None) -> str:
    params: dict[str, str] = {"q": text, "langpair": langpair}
    if email:
        params["de"] = email
    with httpx.Client(timeout=20.0) as client:
        r = client.get(MYMEMORY_URL, params=params)
        r.raise_for_status()
        data = r.json()
    if data.get("quotaFinished"):
        raise RuntimeError("MyMemory daily quota exceeded — try tomorrow or set MYMEMORY_EMAIL in .env")
    resp = data.get("responseData") or {}
    translated = (resp.get("translatedText") or "").strip()
    if not translated:
        raise RuntimeError("empty translation response")
    if translated.upper() == text.upper():
        return translated
    return translated


def _is_mymemory_warning(text: str) -> bool:
    return "MYMEMORY WARNING" in (text or "").upper()


def translate_to_russian(text: str, *, force: bool = False) -> dict[str, str | bool]:
    """
    Translate review text to Russian for labeling hints.
    Uses MyMemory (free). Kazakh+mixed → kk|ru; Russian-only → as-is unless force.
    """
    raw = (text or "").strip()
    if not raw:
        return {"translated": "", "provider": "none", "cached": False, "skipped": True}

    if not needs_translation(raw) and not force:
        return {
            "translated": raw,
            "provider": "none",
            "cached": False,
            "skipped": True,
            "note": "Похоже, уже монолингвальный русский (T — принудительно)",
        }

    cache_key = hashlib.sha256((raw + "|f" if force else raw).encode("utf-8")).hexdigest()
    hit = _cache_get(cache_key)
    if hit is not None:
        return {"translated": hit, "provider": "mymemory", "cached": True, "skipped": False}

    email = os.getenv("MYMEMORY_EMAIL", "").strip() or None
    langpair = "kk|ru"
    pieces: list[str] = []
    for chunk in _chunks(raw):
        piece = _mymemory_chunk(chunk, langpair, email)
        if _is_mymemory_warning(piece):
            raise RuntimeError(piece)
        pieces.append(piece)

    translated = " ".join(pieces)
    if _is_mymemory_warning(translated):
        raise RuntimeError(translated)
    _cache_set(cache_key, translated)
    return {
        "translated": translated,
        "provider": "mymemory",
        "cached": False,
        "skipped": False,
        "langpair": langpair,
    }
