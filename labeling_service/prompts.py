"""System and user prompts for Kazakh–Russian language labeling."""

from __future__ import annotations

import json
import os
from typing import Any

RULES_CORE = """You are an expert linguist annotating Kazakhstan social-media text (Telegram, reviews).
Classify each text into exactly one class: ru, kz, or mixed.

## ru — monolingual Russian
- Entire utterance is Russian in meaning.
- Kazakh name/brand/hashtag alone does NOT make mixed.

## kz — monolingual Kazakh
- Entire utterance is Kazakh (Cyrillic without ә/ң/ү is still kz): «Мен мектепке барамын», «рахмет сізге».
- Shared Cyrillic letters alone are NOT Russian.

## mixed — intrasentential code-switch (shala-Kazakh)
- Russian AND Kazakh in ONE coherent reply, both carrying meaning.
- Examples: «Спасибо, рахмет, очень помогли»; «Бәрі жақсы, но цена высокая»; «Кеттим домой, устал жұмыстан».

## NOT mixed (common mistakes — avoid false positives)
- Pure Russian: «Абсолютно абсурдный приговор», «отличный товар», news comments.
- Emoji-only, numbers-only, links-only: «👏👏👏», «25», «t.me/...».
- One Kazakh loanword in Russian sentence: «спасибо, рахмет» alone in otherwise Russian shop review → often ru unless clear switch.
- Pure Kazakh → kz, not mixed.

## Decision order
1) If only one language → ru or kz.
2) mixed ONLY if you can point to both Russian and Kazakh parts in the same message.
3) If unsure between kz and mixed → mixed only with explicit bilingualism; else kz.
4) If unsure overall → needs_review=true, confidence<=0.75.

## Output
ONE flat JSON array only. No markdown.
[{"row_id": 0, "language": "ru", "confidence": 0.95, "needs_review": false}, ...]
row_id must match input. language ∈ {ru, kz, mixed}."""

FEW_SHOT = """
## Labeled examples (follow this style)
{"row_id": 0, "text": "Отличный товар, доставка быстрая", "language": "ru"}
{"row_id": 1, "text": "Мен бүгін базарға барамын", "language": "kz"}
{"row_id": 2, "text": "Спасибо, рахмет, очень помогли", "language": "mixed"}
{"row_id": 3, "text": "👏👏👏", "language": "ru"}
{"row_id": 4, "text": "Абсолютно абсурдный приговор! Умысел доказан", "language": "ru"}
{"row_id": 5, "text": "Бәрі жақсы, но цена высокая", "language": "mixed"}
{"row_id": 6, "text": "рахмет, жақсы қызмет", "language": "kz"}
"""

VERIFY_SYSTEM = """You are a strict reviewer for code-switching labels.
Many models over-predict "mixed". Confirm mixed ONLY if Russian and Kazakh both appear meaningfully in the same message.
Otherwise correct to ru or kz. Return ONE flat JSON array with row_id, language, confidence, needs_review. No markdown."""

QUALITY_PRESETS: dict[str, dict[str, Any]] = {
    "fast": {"batch_size": 50, "few_shot": False, "verify_mixed": False},
    "balanced": {"batch_size": 25, "few_shot": True, "verify_mixed": False},
    "high": {"batch_size": 10, "few_shot": True, "verify_mixed": True},
    "max": {"batch_size": 3, "few_shot": True, "verify_mixed": True},
}


def get_quality_mode() -> str:
    mode = os.getenv("LABELER_QUALITY", "high").strip().lower()
    return mode if mode in QUALITY_PRESETS else "high"


def get_quality_config() -> dict[str, Any]:
    mode = get_quality_mode()
    cfg = dict(QUALITY_PRESETS[mode])
    if os.getenv("OLLAMA_BATCH_SIZE") and os.getenv("LABELER_PROVIDER", "ollama") == "ollama":
        cfg["batch_size"] = int(os.getenv("OLLAMA_BATCH_SIZE"))
    return cfg


def get_system_prompt() -> str:
    parts = [RULES_CORE]
    if get_quality_config()["few_shot"]:
        parts.append(FEW_SHOT)
    return "\n".join(parts)


# backward compatibility
SYSTEM_PROMPT = get_system_prompt()


def build_user_prompt(items: list[dict]) -> str:
    lines = [
        "Classify each item. Return one flat JSON array for ALL row_ids below.\n",
        "Before labeling, check: both languages present? If not → not mixed.\n",
    ]
    for item in items:
        text = str(item["text"]).replace("\n", " ").strip()
        lines.append(json.dumps({"row_id": item["row_id"], "text": text}, ensure_ascii=False))
    return "\n".join(lines)


def build_verify_prompt(items: list[dict], preliminary: list[dict]) -> str:
    by_id = {int(p["row_id"]): p for p in preliminary}
    lines = [
        "These were labeled mixed. Verify strictly; downgrade to ru/kz if not true code-switch.\n",
    ]
    for item in items:
        rid = int(item["row_id"])
        prev = by_id.get(rid, {})
        lines.append(
            json.dumps(
                {
                    "row_id": rid,
                    "text": str(item["text"]).replace("\n", " ")[:500],
                    "previous_language": prev.get("language", "mixed"),
                },
                ensure_ascii=False,
            )
        )
    return "\n".join(lines)
