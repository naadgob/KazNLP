"""Shared label parsing and normalization for all LLM providers."""

from __future__ import annotations

import json
import re
from typing import Any

VALID_LANGUAGES = frozenset({"ru", "kz", "mixed"})
VALID_TONES = frozenset({"positive", "negative", "skip"})


def is_empty_tone(val: Any) -> bool:
    if val is None or (isinstance(val, float) and str(val) == "nan"):
        return True
    s = str(val).strip().lower()
    return s in ("", "nan", "none", "null", "<na>")


def canonical_tone(val: Any) -> str | None:
    """Map raw CSV value to positive/negative/skip or None if empty."""
    if is_empty_tone(val):
        return None
    tone = str(val).strip().lower()
    aliases = {
        "pos": "positive",
        "positive": "positive",
        "позитив": "positive",
        "neg": "negative",
        "negative": "negative",
        "негатив": "negative",
        "skip": "skip",
        "neutral": "skip",
        "нейтраль": "skip",
    }
    return aliases.get(tone)


def canonical_language(val: Any) -> str | None:
    """Map raw CSV value to ru/kz/mixed or None if empty/unknown."""
    if val is None or (isinstance(val, float) and str(val) == "nan"):
        return None
    lang = str(val).strip().lower()
    if lang in ("", "nan", "none", "null"):
        return None
    if lang in ("kaz", "kk"):
        return "kz"
    if lang in VALID_LANGUAGES:
        return lang
    return None


def _flatten_label_items(parsed: Any) -> list[dict]:
    """Normalize array / nested array / dict responses into flat label dicts."""
    if isinstance(parsed, dict):
        if "row_id" in parsed and "language" in parsed:
            return [parsed]
        items: list[dict] = []
        for value in parsed.values():
            items.extend(_flatten_label_items(value))
        return items
    if isinstance(parsed, list):
        items: list[dict] = []
        for value in parsed:
            items.extend(_flatten_label_items(value))
        return items
    raise ValueError(f"Unexpected JSON label shape: {type(parsed)}")


def _scan_json_objects(text: str) -> list[dict]:
    """Extract dicts with row_id+language by scanning balanced braces."""
    objects: list[dict] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] != "{":
            i += 1
            continue
        depth = 0
        for j in range(i, n):
            ch = text[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    snippet = text[i : j + 1]
                    try:
                        obj = json.loads(snippet)
                    except json.JSONDecodeError:
                        i = j + 1
                        break
                    if isinstance(obj, dict) and "row_id" in obj and "language" in obj:
                        objects.append(obj)
                    i = j + 1
                    break
        else:
            i += 1
    return objects


def _dedupe_by_row_id(items: list[dict]) -> list[dict]:
    by_id: dict[int, dict] = {}
    for item in items:
        by_id[int(item["row_id"])] = item
    return [by_id[k] for k in sorted(by_id)]


def extract_json_array(raw: str) -> list[dict]:
    """Parse model output; tolerate nested/broken JSON from small local models."""
    text = raw.strip()
    if not text:
        raise ValueError("Empty model response")

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text).strip()

    # 1) Standard JSON array / object
    start, end = text.find("["), text.rfind("]")
    if start != -1 and end > start:
        try:
            parsed = json.loads(text[start : end + 1])
            flat = _flatten_label_items(parsed)
            if flat:
                return _dedupe_by_row_id(flat)
        except json.JSONDecodeError:
            pass

    obj_start, obj_end = text.find("{"), text.rfind("}")
    if obj_start != -1 and obj_end > obj_start:
        try:
            parsed = json.loads(text[obj_start : obj_end + 1])
            flat = _flatten_label_items(parsed)
            if flat:
                return _dedupe_by_row_id(flat)
        except json.JSONDecodeError:
            pass

    # 2) Scan individual {...} blocks (Ollama often nests or breaks arrays)
    scanned = _scan_json_objects(text)
    if scanned:
        return _dedupe_by_row_id(scanned)

    raise ValueError(f"Could not parse labels from response: {text[:300]}")


def normalize_label(item: dict) -> dict[str, Any]:
    lang = str(item.get("language", "")).strip().lower()
    if lang in ("kaz", "kk"):
        lang = "kz"
    needs_review = bool(item.get("needs_review", False))
    if lang not in VALID_LANGUAGES:
        lang = "mixed"
        needs_review = True
    try:
        confidence = float(item.get("confidence", 0.5))
    except (TypeError, ValueError):
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))
    if confidence < 0.7:
        needs_review = True
    return {
        "row_id": int(item["row_id"]),
        "language": lang,
        "confidence": confidence,
        "needs_review": needs_review,
    }
