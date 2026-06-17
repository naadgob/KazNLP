"""Text signals and label QA heuristics for ru/kz/mixed manual review."""

from __future__ import annotations

import re
from typing import Any

KAZAKH_CHARS = set("әіңғүұқөһ")
WORD_RE = re.compile(r"[\w']+", re.UNICODE)

try:
    from precision_filter import (
        has_kazakh_signal as _has_kazakh_signal,
        has_russian_signal as _has_russian_signal,
        is_low_signal_text as _is_low_signal_text,
    )
except ImportError:
    def _has_kazakh_signal(text: str) -> bool:
        t = text.lower()
        return any(c in KAZAKH_CHARS for c in t)

    def _has_russian_signal(text: str) -> bool:
        return bool(re.search(r"[а-яё]{3,}", text.lower())) and not _has_kazakh_signal(text)

    def _is_low_signal_text(text: str) -> bool:
        return len(text.strip()) < 12


def has_kazakh_letters(text: str) -> bool:
    return any(c in KAZAKH_CHARS for c in text.lower())


def text_signals(text: str) -> dict[str, bool]:
    has_kz = _has_kazakh_signal(text)
    has_ru = _has_russian_signal(text)
    return {
        "has_kazakh_letters": has_kazakh_letters(text),
        "has_kazakh_signal": has_kz,
        "has_russian_signal": has_ru,
        "potential_real_mixed": has_kz and has_ru,
        "low_signal": _is_low_signal_text(text),
        "likely_pure_ru": has_ru and not has_kz,
        "likely_pure_kz": has_kz and not has_ru,
    }


def label_heuristics(text: str, language: str | None) -> dict[str, Any]:
    """Compare gold label with text signals; flag likely mislabels."""
    sig = text_signals(text)
    lang = (language or "").strip().lower() or None
    if lang in ("kaz", "kk"):
        lang = "kz"

    reasons: list[str] = []
    if lang == "ru":
        if sig["has_kazakh_letters"]:
            reasons.append("ru_but_kazakh_letters")
        if sig["potential_real_mixed"]:
            reasons.append("ru_but_bilingual")
    elif lang == "kz":
        if not sig["has_kazakh_signal"]:
            reasons.append("kz_without_kazakh_signal")
        if sig["likely_pure_ru"]:
            reasons.append("kz_likely_ru_only")
    elif lang == "mixed":
        if sig["low_signal"]:
            reasons.append("mixed_low_signal")
        elif sig["likely_pure_ru"]:
            reasons.append("mixed_likely_ru_only")
        elif sig["likely_pure_kz"]:
            reasons.append("mixed_likely_kz_only")
        elif not sig["potential_real_mixed"]:
            reasons.append("mixed_weak_bilingual")

    quality = 100
    if reasons:
        quality = max(20, 100 - 25 * len(reasons))
    if lang == "mixed" and sig["potential_real_mixed"] and sig["has_kazakh_letters"]:
        quality = 100

    return {
        **sig,
        "label_mismatch": bool(reasons),
        "suspicious_label": bool(reasons),
        "mismatch_reasons": reasons,
        "quality_score": quality,
    }


MISMATCH_LABELS: dict[str, str] = {
    "ru_but_kazakh_letters": "RU label but text has Kazakh letters (ә/ң/…)",
    "ru_but_bilingual": "RU label but both RU+KZ signals — maybe mixed?",
    "kz_without_kazakh_signal": "KZ label but no Kazakh signal in text",
    "kz_likely_ru_only": "KZ label but text looks Russian-only",
    "mixed_low_signal": "MIXED label but text too short / low signal",
    "mixed_likely_ru_only": "MIXED label but likely pure Russian",
    "mixed_likely_kz_only": "MIXED label but likely pure Kazakh",
    "mixed_weak_bilingual": "MIXED label but weak bilingual evidence",
}
