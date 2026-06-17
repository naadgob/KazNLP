"""Incremental metrics updates — avoid full-dataset scans on each label."""

from __future__ import annotations

import re
import time
from typing import Any

from label_utils import canonical_language
from queue_engine import row_has_kazakh_letters


def _lang_code(val: Any) -> str | None:
    return canonical_language(val)


def _row_flags(text: str) -> dict[str, bool]:
    has_kz = row_has_kazakh_letters(text)
    has_ru_cyr = bool(re.search(r"[а-яё]{3,}", text, re.I))
    has_cyr = bool(re.search(r"[а-яё]", text, re.I))
    prm = has_kz and (has_cyr or has_ru_cyr)
    return {"has_kz": has_kz, "has_ru_cyr": has_ru_cyr, "prm": prm}


def apply_label_delta(
    snapshot: dict[str, Any],
    *,
    prev_language: Any,
    new_language: str,
    text: str,
    prev_source: Any,
    session_labeled: int,
    session_started_at: float | None,
    session_distribution: dict[str, int] | None = None,
) -> dict[str, Any]:
    snap = {**snapshot}
    dist = dict(snap.get("distribution") or {"ru": 0, "kz": 0, "mixed": 0})
    manual_dist = dict(snap.get("manual_distribution") or {"ru": 0, "kz": 0, "mixed": 0})
    heur = dict(snap.get("heuristics") or {})

    prev = _lang_code(prev_language)
    new = _lang_code(new_language) or new_language
    flags = _row_flags(text)

    if prev in dist:
        dist[prev] = max(0, dist[prev] - 1)
    elif prev is None:
        snap["unlabeled"] = max(0, snap.get("unlabeled", 0) - 1)
        snap["labeled"] = snap.get("labeled", 0) + 1

    if new in dist:
        dist[new] = dist.get(new, 0) + 1

    was_manual = str(prev_source).strip().lower() == "manual"
    if was_manual and prev in manual_dist:
        manual_dist[prev] = max(0, manual_dist[prev] - 1)
    if new in manual_dist:
        manual_dist[new] = manual_dist.get(new, 0) + 1

    total = snap.get("total", 0)
    snap["distribution"] = dist
    snap["manual_distribution"] = manual_dist
    snap["labeled_pct"] = round(100 * snap.get("labeled", 0) / total, 1) if total else 0
    snap["mixed_pct"] = round(100 * dist.get("mixed", 0) / total, 2) if total else 0

    if str(prev_source).strip().lower() != "manual":
        snap["manual_count"] = snap.get("manual_count", 0) + 1

    snap["session_distribution"] = session_distribution or snap.get(
        "session_distribution", {"ru": 0, "kz": 0, "mixed": 0}
    )

    if prev is None and flags["has_kz"]:
        heur["unlabeled_kazakh"] = max(0, heur.get("unlabeled_kazakh", 0) - 1)

    if new == "ru" and flags["has_kz"]:
        heur["ru_with_kazakh_letters"] = heur.get("ru_with_kazakh_letters", 0) + 1
    if prev == "ru" and flags["has_kz"]:
        heur["ru_with_kazakh_letters"] = max(0, heur.get("ru_with_kazakh_letters", 0) - 1)

    if flags["prm"] and prev is None:
        heur["potential_real_mixed_unlabeled"] = max(0, heur.get("potential_real_mixed_unlabeled", 0) - 1)
        heur["potential_real_mixed_labeled"] = heur.get("potential_real_mixed_labeled", 0) + 1

    snap["heuristics"] = heur
    snap["session_labeled"] = session_labeled
    snap["session_started_at"] = session_started_at
    if session_started_at and session_labeled > 0:
        elapsed_h = max((time.time() - session_started_at) / 3600, 1 / 60)
        snap["labels_per_hour"] = round(session_labeled / elapsed_h, 1)
    snap["mixed_with_kazakh_chars"] = heur.get("mixed_with_kazakh_letters", 0)
    return snap
