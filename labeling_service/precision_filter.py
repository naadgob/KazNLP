"""
Post-filter to improve precision on language == mixed (reduce false positives).

Usage (after labeling):
    import pandas as pd
    from precision_filter import refine_dataframe

    df = pd.read_csv("labeled.csv")
    df = refine_dataframe(df)
    df.to_csv("labeled_filtered.csv", index=False, encoding="utf-8-sig")
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from essential_ru_kaz import kazakh_dict
from popular_ru_kaz import popular_ru_kaz_dict

KAZAKH_CHARS = set("әіңғүұқөһ")
# Kazakh lexicon: keys from essential + values from popular (ru->kz)
KZ_LEXICON = {w.lower() for w in kazakh_dict} | {w.lower() for w in popular_ru_kaz_dict.values()}
# Russian function words (high precision signal)
RU_LEXICON = {w.lower() for w in popular_ru_kaz_dict if len(w) >= 2}

WORD_RE = re.compile(r"[\w']+", re.UNICODE)
URL_RE = re.compile(r"https?://|t\.me/|tg://", re.I)
MIN_MIXED_CHARS = 12
MIN_MIXED_WORDS = 2


def _words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def has_kazakh_signal(text: str) -> bool:
    t = text.lower()
    if any(c in KAZAKH_CHARS for c in t):
        return True
    words = set(_words(t))
    if len(words) >= 2 and len(words & KZ_LEXICON) >= 1:
        return True
    return False


def has_russian_signal(text: str) -> bool:
    words = set(_words(text.lower()))
    if len(words & RU_LEXICON) >= 1:
        return True
    # Cyrillic sentence with no kazakh letters: likely Russian social text
    if re.search(r"[а-яё]{3,}", text.lower()) and not any(c in KAZAKH_CHARS for c in text.lower()):
        return True
    return False


def is_low_signal_text(text: str) -> bool:
    t = text.strip()
    if len(t) < MIN_MIXED_CHARS:
        return True
    if URL_RE.search(t) and len(_words(t)) <= 3:
        return True
    if re.fullmatch(r"[\d\s\W👏🔥❤️🤣😂✅]+", t):
        return True
    alpha = re.sub(r"\s+", "", t)
    if len(alpha) <= 4:
        return True
    return False


def refine_language(text: str, language: str, confidence: float | None = None) -> tuple[str, float, bool, str]:
    """
    Returns (language, confidence, needs_review, note).
  If mixed fails checks, downgrade to ru/kz and flag for review.
    """
    lang = str(language).strip().lower()
    if lang in ("kaz", "kk"):
        lang = "kz"
    try:
        conf = float(confidence) if confidence is not None and not pd.isna(confidence) else 0.8
    except (TypeError, ValueError):
        conf = 0.8

    if lang != "mixed":
        return lang, conf, False, ""

    note = ""
    if is_low_signal_text(text):
        return "ru", min(conf, 0.6), True, "mixed_rejected:low_signal"

    has_kz = has_kazakh_signal(text)
    has_ru = has_russian_signal(text)

    if has_kz and has_ru:
        return "mixed", conf, False, ""

    if has_kz and not has_ru:
        return "kz", conf, True, "mixed_rejected:kz_only"
    if has_ru and not has_kz:
        return "ru", conf, True, "mixed_rejected:ru_only"

    return "ru", min(conf, 0.5), True, "mixed_rejected:no_bilingual_signal"


def refine_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "needs_review" not in out.columns:
        out["needs_review"] = False
    if "confidence" not in out.columns:
        out["confidence"] = pd.NA

    notes: list[str] = []
    for i in range(len(out)):
        lang, conf, review, note = refine_language(
            str(out.at[i, "text"]),
            out.at[i, "language"],
            out.at[i, "confidence"],
        )
        out.at[i, "language"] = lang
        out.at[i, "confidence"] = conf
        if review or note:
            out.at[i, "needs_review"] = True
        notes.append(note)

    out["filter_note"] = notes
    return out


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Refine mixed labels for higher precision")
    p.add_argument("input_csv")
    p.add_argument("-o", "--output", help="output path (default: input_filtered.csv)")
    args = p.parse_args()
    inp = Path(args.input_csv)
    out = Path(args.output) if args.output else inp.with_name(inp.stem + "_filtered.csv")
    df = refine_dataframe(pd.read_csv(inp))
    before = (pd.read_csv(inp)["language"].astype(str).str.lower() == "mixed").sum()
    after = (df["language"].astype(str).str.lower() == "mixed").sum()
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"mixed: {before} -> {after}  saved: {out}")
