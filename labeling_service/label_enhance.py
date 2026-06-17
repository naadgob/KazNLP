"""Post-LLM enhancements: precision filter + shared helpers."""

from __future__ import annotations

import os

from precision_filter import refine_language


def use_precision_filter() -> bool:
    return os.getenv("APPLY_PRECISION_FILTER", "true").strip().lower() in ("1", "true", "yes", "on")


def refine_llm_labels(items: list[dict], labels: list[dict]) -> tuple[list[dict], int]:
    """
    Apply dictionary/heuristic precision filter to LLM labels.
    Returns (refined labels, count of changed rows).
    """
    text_by_id = {int(i["row_id"]): str(i["text"]) for i in items}
    changed = 0
    refined: list[dict] = []

    for lab in labels:
        rid = int(lab["row_id"])
        text = text_by_id.get(rid, "")
        old_lang = str(lab.get("language", "")).lower()
        lang, conf, review, note = refine_language(text, lab.get("language"), lab.get("confidence"))
        if lang != old_lang:
            changed += 1
        refined.append(
            {
                **lab,
                "row_id": rid,
                "language": lang,
                "confidence": conf,
                "needs_review": bool(review or lab.get("needs_review")),
                "filter_note": note or lab.get("filter_note", ""),
            }
        )

    return refined, changed
