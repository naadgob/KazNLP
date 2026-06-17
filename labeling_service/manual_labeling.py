"""Manual language labeling: metrics, queues, row updates."""

from __future__ import annotations

import re
import time
from typing import Any

import pandas as pd

from csv_processor import ensure_output_columns, is_empty_language, job_dir, load_dataframe, load_state, save_state
from job_cache import (
    flush_job_save,
    flush_state,
    load_job_dataframe,
    load_job_state,
    remove_row_from_queue_caches,
    schedule_job_save,
    schedule_state_save,
    update_cached_row,
)
from domain_heuristics import DOMAIN_LABELS, VALID_DOMAINS, text_domain
from label_utils import VALID_LANGUAGES, VALID_TONES, canonical_language, canonical_tone, is_empty_tone
from metrics_cache import apply_label_delta
from queue_engine import (
    LARGE_JOB_ROWS,
    compute_heuristic_metrics_fast,
    compute_heuristic_metrics_fast_lite,
    queue_next_after_label,
    queue_page,
    row_has_kazakh_letters,
)
from text_heuristics import MISMATCH_LABELS, label_heuristics

FILTERS = frozenset(
    {
        "unlabeled",
        "mixed",
        "llm_mixed",
        "needs_review",
        "manual",
        "disagree",
        "all",
        "potential_real_mixed",
        "suspicious",
        "ru_but_kazakh",
        "kaz_letters_in_ru_text",
        "mixed_false_positive",
        "kz_no_signal",
        "unlabeled_kazakh",
        "low_signal",
        "label_ru",
        "label_kz",
        "label_mixed",
        "unlabeled_tone",
        "mixed_unlabeled_tone",
        "tone_positive",
        "tone_negative",
        "tone_skip",
        "tone_manual",
        "domain_review",
        "domain_logistics",
        "domain_other",
    }
)

SENTIMENT_FILTERS = frozenset(
    {
        "unlabeled_tone",
        "mixed_unlabeled_tone",
        "tone_positive",
        "tone_negative",
        "tone_skip",
        "tone_manual",
        "domain_review",
        "domain_logistics",
        "domain_other",
        "all",
        "label_mixed",
        "mixed",
    }
)

DOMAIN_FILTERS = frozenset({"any", *VALID_DOMAINS})

CLASS_FILTERS = frozenset({"any", "unlabeled", "ru", "kz", "mixed"})

# Filters where row leaves queue after a successful manual label
CONSUMING_FILTERS = frozenset(
    {
        "unlabeled",
        "llm_mixed",
        "needs_review",
        "suspicious",
        "ru_but_kazakh",
        "kaz_letters_in_ru_text",
        "mixed_false_positive",
        "kz_no_signal",
        "unlabeled_kazakh",
        "low_signal",
        "unlabeled_tone",
        "mixed_unlabeled_tone",
    }
)

TONE_CONSUMING_FILTERS = frozenset({"unlabeled_tone", "mixed_unlabeled_tone"})

CLASS_KEYS = ("ru", "kz", "mixed")
TONE_KEYS = ("positive", "negative", "skip")


def empty_class_counts() -> dict[str, int]:
    return {"ru": 0, "kz": 0, "mixed": 0}


def ensure_session_by_class(session: dict[str, Any]) -> dict[str, int]:
    by_class = session.get("by_class")
    if not isinstance(by_class, dict):
        by_class = empty_class_counts()
        session["by_class"] = by_class
    for key in CLASS_KEYS:
        by_class.setdefault(key, 0)
    return by_class


def manual_class_counts(df: pd.DataFrame) -> dict[str, int]:
    from queue_engine import _lang_codes_fast

    counts = empty_class_counts()
    if "label_source" not in df.columns:
        return counts
    langs = _lang_codes_fast(df)
    manual = df["label_source"].astype(str).str.strip().str.lower() == "manual"
    for key in CLASS_KEYS:
        counts[key] = int((manual & (langs == key)).sum())
    return counts


def empty_tone_counts() -> dict[str, int]:
    return {"positive": 0, "negative": 0, "skip": 0}


def ensure_sentiment_session(session: dict[str, Any]) -> dict[str, int]:
    by_tone = session.get("by_tone")
    if not isinstance(by_tone, dict):
        by_tone = empty_tone_counts()
        session["by_tone"] = by_tone
    for key in TONE_KEYS:
        by_tone.setdefault(key, 0)
    return by_tone


def manual_tone_counts(df: pd.DataFrame) -> dict[str, int]:
    counts = empty_tone_counts()
    if "tone_source" not in df.columns:
        return counts
    manual = df["tone_source"].astype(str).str.strip().str.lower() == "manual"
    for key in TONE_KEYS:
        counts[key] = int((manual & (df["label"].apply(lambda x: canonical_tone(x)) == key)).sum())
    return counts


def filter_catalog() -> dict[str, Any]:
    return {
        "filters": sorted(FILTERS),
        "sentiment_filters": sorted(SENTIMENT_FILTERS),
        "class_filters": sorted(CLASS_FILTERS),
        "domain_filters": sorted(DOMAIN_FILTERS),
        "domain_labels": DOMAIN_LABELS,
        "consuming_filters": sorted(CONSUMING_FILTERS),
        "tone_consuming_filters": sorted(TONE_CONSUMING_FILTERS),
        "mismatch_labels": MISMATCH_LABELS,
        "tones": sorted(VALID_TONES),
    }


def _load_job_df(job_id: str) -> pd.DataFrame:
    return load_job_dataframe(job_id)


def _row_heuristics(df: pd.DataFrame, idx: int) -> dict[str, Any]:
    text = str(df.at[idx, "text"])
    lang = canonical_language(df.at[idx, "language"])
    return label_heuristics(text, lang)


def _match_class(df: pd.DataFrame, idx: int, class_filter: str) -> bool:
    if class_filter == "any":
        return True
    lang = canonical_language(df.at[idx, "language"])
    if class_filter == "unlabeled":
        return lang is None
    effective = lang
    if effective is None and "llm_language" in df.columns:
        effective = canonical_language(df.at[idx, "llm_language"])
    return effective == class_filter


def row_dict_lite(df: pd.DataFrame, idx: int) -> dict[str, Any]:
    """Fast row payload for navigation — no lexicon heuristics."""
    lang = canonical_language(df.at[idx, "language"])
    llm = canonical_language(df.at[idx, "llm_language"]) if "llm_language" in df.columns else None
    src = str(df.at[idx, "label_source"]).strip().lower() if "label_source" in df.columns else ""
    if src in ("", "nan", "none"):
        src = None
    text = str(df.at[idx, "text"])
    has_kz = bool(df.at[idx, "_has_kz"]) if "_has_kz" in df.columns else row_has_kazakh_letters(text)
    has_ru = bool(df.at[idx, "_has_ru_cyr"]) if "_has_ru_cyr" in df.columns else bool(re.search(r"[а-яё]{3,}", text, re.I))
    prm = has_kz and has_ru
    disagree = lang and llm and lang != llm

    return {
        "row_id": idx,
        "text": text,
        "language": lang or "",
        "llm_language": llm or "",
        "label_source": src,
        "tone": canonical_tone(df.at[idx, "label"]) or "",
        "tone_source": (
            None
            if "tone_source" not in df.columns or pd.isna(df.at[idx, "tone_source"])
            else str(df.at[idx, "tone_source"]).strip().lower()
        ),
        "domain": text_domain(text),
        "confidence": None,
        "needs_review": bool(df.at[idx, "needs_review"]) if not pd.isna(df.at[idx, "needs_review"]) else False,
        "filter_note": "",
        "has_kazakh_chars": has_kz,
        "has_kazakh_signal": has_kz,
        "has_russian_signal": has_ru,
        "potential_real_mixed": prm,
        "low_signal": len(text.strip()) < 12,
        "label_mismatch": False,
        "suspicious_label": False,
        "mismatch_reasons": [],
        "mismatch_labels": [],
        "quality_score": 100,
        "disagree_llm": disagree,
        "word_count": len(re.findall(r"\w+", text, flags=re.UNICODE)),
    }


def row_dict(df: pd.DataFrame, idx: int, *, lite: bool = False) -> dict[str, Any]:
    if lite:
        return row_dict_lite(df, idx)
    lang = canonical_language(df.at[idx, "language"])
    llm = canonical_language(df.at[idx, "llm_language"]) if "llm_language" in df.columns else None
    src = str(df.at[idx, "label_source"]).strip().lower() if "label_source" in df.columns else ""
    if src in ("", "nan", "none"):
        src = None
    disagree = lang and llm and lang != llm
    text = str(df.at[idx, "text"])
    heur = label_heuristics(text, lang)
    mismatch_human = [MISMATCH_LABELS.get(r, r) for r in heur["mismatch_reasons"]]

    return {
        "row_id": idx,
        "text": text,
        "language": lang or "",
        "llm_language": llm or "",
        "label_source": src,
        "tone": canonical_tone(df.at[idx, "label"]) or "",
        "tone_source": (
            None
            if "tone_source" not in df.columns or pd.isna(df.at[idx, "tone_source"])
            else str(df.at[idx, "tone_source"]).strip().lower()
        ),
        "domain": text_domain(text),
        "confidence": (
            None
            if "confidence" not in df.columns or pd.isna(df.at[idx, "confidence"])
            else float(df.at[idx, "confidence"])
        ),
        "needs_review": bool(df.at[idx, "needs_review"]) if not pd.isna(df.at[idx, "needs_review"]) else False,
        "filter_note": (
            ""
            if "filter_note" not in df.columns or pd.isna(df.at[idx, "filter_note"])
            else str(df.at[idx, "filter_note"])
        ),
        "has_kazakh_chars": heur["has_kazakh_letters"],
        "has_kazakh_signal": heur["has_kazakh_signal"],
        "has_russian_signal": heur["has_russian_signal"],
        "potential_real_mixed": heur["potential_real_mixed"],
        "low_signal": heur["low_signal"],
        "label_mismatch": heur["label_mismatch"],
        "suspicious_label": heur["suspicious_label"],
        "mismatch_reasons": heur["mismatch_reasons"],
        "mismatch_labels": mismatch_human,
        "quality_score": heur["quality_score"],
        "disagree_llm": disagree,
        "word_count": len(re.findall(r"\w+", text, flags=re.UNICODE)),
    }


def match_filter(
    df: pd.DataFrame,
    idx: int,
    filter_name: str,
    search: str,
    class_filter: str = "any",
    domain_filter: str = "any",
) -> bool:
    if not _match_class(df, idx, class_filter):
        return False
    if search and search.lower() not in str(df.at[idx, "text"]).lower():
        return False
    if domain_filter != "any" and domain_filter in VALID_DOMAINS:
        if text_domain(str(df.at[idx, "text"])) != domain_filter:
            return False

    lang = canonical_language(df.at[idx, "language"])
    tone = canonical_tone(df.at[idx, "label"])
    tone_src = (
        str(df.at[idx, "tone_source"]).strip().lower()
        if "tone_source" in df.columns and not pd.isna(df.at[idx, "tone_source"])
        else ""
    )
    llm = canonical_language(df.at[idx, "llm_language"]) if "llm_language" in df.columns else None
    effective = lang or llm
    src = str(df.at[idx, "label_source"]).strip().lower() if "label_source" in df.columns else ""
    needs = bool(df.at[idx, "needs_review"]) if not pd.isna(df.at[idx, "needs_review"]) else False
    heur = _row_heuristics(df, idx)

    if filter_name == "all":
        return True
    if filter_name == "unlabeled":
        return lang is None
    if filter_name == "mixed":
        return effective == "mixed"
    if filter_name == "llm_mixed":
        return llm == "mixed"
    if filter_name == "needs_review":
        return needs
    if filter_name == "manual":
        return src == "manual"
    if filter_name == "disagree":
        return bool(lang and llm and lang != llm)
    if filter_name == "label_ru":
        return effective == "ru"
    if filter_name == "label_kz":
        return effective == "kz"
    if filter_name == "label_mixed":
        return effective == "mixed"
    if filter_name == "potential_real_mixed":
        return heur["potential_real_mixed"]
    if filter_name == "suspicious":
        return effective is not None and heur["suspicious_label"]
    if filter_name == "ru_but_kazakh":
        return effective == "ru" and heur["has_kazakh_letters"]
    if filter_name == "kaz_letters_in_ru_text":
        return heur["has_kazakh_letters"] and heur["has_russian_signal"]
    if filter_name == "mixed_false_positive":
        return effective == "mixed" and not heur["potential_real_mixed"]
    if filter_name == "kz_no_signal":
        return effective == "kz" and not heur["has_kazakh_signal"]
    if filter_name == "unlabeled_kazakh":
        return lang is None and heur["has_kazakh_letters"]
    if filter_name == "low_signal":
        return heur["low_signal"]
    if filter_name == "unlabeled_tone":
        return tone is None
    if filter_name == "mixed_unlabeled_tone":
        return effective == "mixed" and tone is None
    if filter_name == "tone_positive":
        return tone == "positive"
    if filter_name == "tone_negative":
        return tone == "negative"
    if filter_name == "tone_skip":
        return tone == "skip"
    if filter_name == "tone_manual":
        return tone_src == "manual"
    if filter_name == "domain_review":
        return text_domain(str(df.at[idx, "text"])) == "review"
    if filter_name == "domain_logistics":
        return text_domain(str(df.at[idx, "text"])) == "logistics"
    if filter_name == "domain_other":
        return text_domain(str(df.at[idx, "text"])) == "other"
    return True


def queue_indices(
    df: pd.DataFrame,
    filter_name: str,
    search: str = "",
    class_filter: str = "any",
) -> list[int]:
    """Legacy helper — prefer queue_page() for large jobs."""
    from queue_engine import get_queue_indices

    return get_queue_indices("", df, filter_name, search, class_filter).tolist()


def compute_heuristic_metrics(df: pd.DataFrame) -> dict[str, int]:
    if len(df) > LARGE_JOB_ROWS:
        return compute_heuristic_metrics_fast_lite(df)
    return compute_heuristic_metrics_fast(df)


def compute_metrics(df: pd.DataFrame, state: dict | None = None) -> dict[str, Any]:
    from queue_engine import _lang_codes_fast, _text_series

    total = len(df)
    langs = _lang_codes_fast(df)
    stats = {
        "ru": int((langs == "ru").sum()),
        "kz": int((langs == "kz").sum()),
        "mixed": int((langs == "mixed").sum()),
    }
    unlabeled = int(langs.isna().sum())
    labeled = total - unlabeled

    manual = 0
    if "label_source" in df.columns:
        manual = int((df["label_source"].astype(str).str.strip().str.lower() == "manual").sum())

    llm_mixed = 0
    if "llm_language" in df.columns:
        llm_mixed = int(df["llm_language"].apply(lambda x: canonical_language(x) == "mixed").sum())

    needs_review = 0
    if "needs_review" in df.columns:
        needs_review = int(df["needs_review"].fillna(False).astype(bool).sum())

    disagree = 0
    if "llm_language" in df.columns:
        llm_norm = df["llm_language"].apply(lambda x: canonical_language(x) if not is_empty_language(x) else None)
        disagree = int((langs.notna() & llm_norm.notna() & (langs != llm_norm)).sum())

    mixed_word_lens: list[int] = []
    if stats["mixed"]:
        texts = _text_series(df)
        mixed_mask = langs == "mixed"
        mixed_word_lens = [
            len(re.findall(r"\w+", t, flags=re.UNICODE))
            for t in texts[mixed_mask].head(5000)
        ]

    session = (state or {}).get("manual_session", {})
    session_distribution = ensure_session_by_class(dict(session))
    heur = compute_heuristic_metrics(df)

    session_started = session.get("started_at")
    labels_per_hour = None
    if session_started and session.get("labeled", 0) > 0:
        elapsed_h = max((time.time() - session_started) / 3600, 1 / 60)
        labels_per_hour = round(session.get("labeled", 0) / elapsed_h, 1)

    manual_distribution = manual_class_counts(df)

    tones = df["label"].apply(lambda x: canonical_tone(x)) if "label" in df.columns else pd.Series(dtype="object")
    tone_stats = {
        "positive": int((tones == "positive").sum()),
        "negative": int((tones == "negative").sum()),
        "skip": int((tones == "skip").sum()),
        "unlabeled": int(tones.isna().sum()),
    }
    tone_labeled = tone_stats["positive"] + tone_stats["negative"] + tone_stats["skip"]
    tone_manual = 0
    if "tone_source" in df.columns:
        tone_manual = int((df["tone_source"].astype(str).str.strip().str.lower() == "manual").sum())

    from domain_heuristics import domain_series

    domains = domain_series(_text_series(df))
    domain_stats = {
        "review": int((domains == "review").sum()),
        "logistics": int((domains == "logistics").sum()),
        "other": int((domains == "other").sum()),
    }
    mixed_mask = langs == "mixed"
    mixed_domains = domain_series(_text_series(df)[mixed_mask]) if mixed_mask.any() else pd.Series(dtype="object")
    mixed_domain_stats = {
        "review": int((mixed_domains == "review").sum()) if len(mixed_domains) else 0,
        "logistics": int((mixed_domains == "logistics").sum()) if len(mixed_domains) else 0,
        "other": int((mixed_domains == "other").sum()) if len(mixed_domains) else 0,
    }

    sentiment_session = (state or {}).get("sentiment_session", {})
    sentiment_distribution = ensure_sentiment_session(dict(sentiment_session))
    sentiment_started = sentiment_session.get("started_at")
    tone_labels_per_hour = None
    if sentiment_started and sentiment_session.get("labeled", 0) > 0:
        elapsed_h = max((time.time() - sentiment_started) / 3600, 1 / 60)
        tone_labels_per_hour = round(sentiment_session.get("labeled", 0) / elapsed_h, 1)

    manual_tone_distribution = manual_tone_counts(df)

    return {
        "total": total,
        "labeled": labeled,
        "unlabeled": unlabeled,
        "labeled_pct": round(100 * labeled / total, 1) if total else 0,
        "mixed_pct": round(100 * stats["mixed"] / total, 2) if total else 0,
        "manual_count": manual,
        "llm_mixed_count": llm_mixed,
        "needs_review_count": needs_review,
        "disagree_count": disagree,
        "mixed_avg_words": round(sum(mixed_word_lens) / len(mixed_word_lens), 1) if mixed_word_lens else 0,
        "distribution": stats,
        "manual_distribution": manual_distribution,
        "session_labeled": session.get("labeled", 0),
        "session_distribution": session_distribution,
        "session_started_at": session_started,
        "labels_per_hour": labels_per_hour,
        "heuristics": heur,
        "mixed_with_kazakh_chars": heur["mixed_with_kazakh_letters"],
        "tone_distribution": tone_stats,
        "tone_labeled": tone_labeled,
        "tone_labeled_pct": round(100 * tone_labeled / total, 1) if total else 0,
        "tone_manual_count": tone_manual,
        "manual_tone_distribution": manual_tone_distribution,
        "domain_distribution": domain_stats,
        "mixed_domain_distribution": mixed_domain_stats,
        "sentiment_session_labeled": sentiment_session.get("labeled", 0),
        "sentiment_session_distribution": sentiment_distribution,
        "sentiment_session_started_at": sentiment_started,
        "tone_labels_per_hour": tone_labels_per_hour,
    }


def get_or_build_metrics(df: pd.DataFrame, state: dict | None) -> dict[str, Any]:
    state = state or {}
    snap = state.get("metrics_snapshot")
    if snap and snap.get("total") == len(df):
        return snap
    return compute_metrics(df, state)


def apply_manual_label(
    job_id: str,
    row_id: int,
    language: str,
    *,
    needs_review: bool = False,
    queue_filter: str | None = None,
    queue_class: str = "any",
    queue_search: str = "",
    queue_domain: str = "any",
    queue_position: int = 0,
) -> dict[str, Any]:
    lang = canonical_language(language)
    if lang not in VALID_LANGUAGES:
        raise ValueError(f"language must be one of: ru, kz, mixed")

    df = _load_job_df(job_id)
    if row_id < 0 or row_id >= len(df):
        raise ValueError("Invalid row_id")

    state = load_job_state(job_id)
    undo = state.get("manual_undo", [])
    prev_lang = df.at[row_id, "language"]
    prev_source = df.at[row_id, "label_source"] if "label_source" in df.columns else None
    text = str(df.at[row_id, "text"])

    undo.append(
        {
            "kind": "language",
            "row_id": row_id,
            "language": prev_lang,
            "label_source": prev_source,
            "needs_review": df.at[row_id, "needs_review"],
            "confidence": df.at[row_id, "confidence"],
            "applied_language": lang,
            "ts": time.time(),
        }
    )
    undo = undo[-50:]

    prev = row_dict(df, row_id)
    update_cached_row(
        job_id,
        row_id,
        {
            "language": lang,
            "label_source": "manual",
            "needs_review": needs_review,
            "confidence": 1.0,
        },
    )
    remove_row_from_queue_caches(job_id, row_id)
    schedule_job_save(
        job_id,
        row_id,
        {
            "language": lang,
            "label_source": "manual",
            "needs_review": needs_review,
            "confidence": 1.0,
        },
    )

    session = state.get("manual_session", {"labeled": 0, "started_at": None})
    if not session.get("started_at"):
        session["started_at"] = time.time()
    session["labeled"] = session.get("labeled", 0) + 1
    by_class = ensure_session_by_class(session)
    if lang in by_class:
        by_class[lang] += 1

    metrics_base = get_or_build_metrics(df, state)
    metrics = apply_label_delta(
        metrics_base,
        prev_language=prev_lang,
        new_language=lang,
        text=text,
        prev_source=prev_source,
        session_labeled=session["labeled"],
        session_started_at=session.get("started_at"),
        session_distribution=by_class,
    )

    schedule_state_save(
        job_id,
        {
            **state,
            "manual_undo": undo,
            "manual_session": session,
            "metrics_snapshot": metrics,
            "stats": metrics["distribution"],
        },
    )

    result: dict[str, Any] = {
        "row": row_dict(df, row_id),
        "previous": prev,
        "metrics": metrics,
        "pending_save": True,
    }

    if queue_filter:
        page = queue_next_after_label(
            job_id,
            df,
            queue_filter,
            queue_search,
            queue_class,
            queue_position,
            row_id,
            queue_domain,
        )
        result["next"] = page
        if page.get("row_id") is not None:
            result["next"]["row"] = row_dict(df, int(page["row_id"]), lite=True)

    return result


def apply_manual_sentiment(
    job_id: str,
    row_id: int,
    tone: str,
    *,
    queue_filter: str | None = None,
    queue_class: str = "any",
    queue_search: str = "",
    queue_domain: str = "any",
    queue_position: int = 0,
) -> dict[str, Any]:
    tone_val = canonical_tone(tone)
    if tone_val not in VALID_TONES:
        raise ValueError(f"tone must be one of: positive, negative, skip")

    df = _load_job_df(job_id)
    if row_id < 0 or row_id >= len(df):
        raise ValueError("Invalid row_id")

    state = load_job_state(job_id)
    undo = state.get("manual_undo", [])
    prev_label = df.at[row_id, "label"]
    prev_tone_source = df.at[row_id, "tone_source"] if "tone_source" in df.columns else None

    undo.append(
        {
            "kind": "sentiment",
            "row_id": row_id,
            "label": prev_label,
            "tone_source": prev_tone_source,
            "applied_tone": tone_val,
            "ts": time.time(),
        }
    )
    undo = undo[-50:]

    prev = row_dict(df, row_id)
    update_cached_row(
        job_id,
        row_id,
        {
            "label": tone_val,
            "tone_source": "manual",
        },
    )
    remove_row_from_queue_caches(job_id, row_id)
    schedule_job_save(
        job_id,
        row_id,
        {
            "label": tone_val,
            "tone_source": "manual",
        },
    )

    sentiment_session = state.get(
        "sentiment_session",
        {"labeled": 0, "started_at": None, "by_tone": empty_tone_counts()},
    )
    if not sentiment_session.get("started_at"):
        sentiment_session["started_at"] = time.time()
    sentiment_session["labeled"] = sentiment_session.get("labeled", 0) + 1
    by_tone = ensure_sentiment_session(sentiment_session)
    if tone_val in by_tone:
        by_tone[tone_val] += 1

    metrics = compute_metrics(df, {**state, "sentiment_session": sentiment_session})
    schedule_state_save(
        job_id,
        {
            **state,
            "manual_undo": undo,
            "sentiment_session": sentiment_session,
            "metrics_snapshot": metrics,
        },
    )

    result: dict[str, Any] = {
        "row": row_dict(df, row_id),
        "previous": prev,
        "metrics": metrics,
        "pending_save": True,
    }

    if queue_filter:
        page = queue_next_after_label(
            job_id,
            df,
            queue_filter,
            queue_search,
            queue_class,
            queue_position,
            row_id,
            queue_domain,
        )
        result["next"] = page
        if page.get("row_id") is not None:
            result["next"]["row"] = row_dict(df, int(page["row_id"]), lite=True)

    return result


def undo_manual(job_id: str) -> dict[str, Any] | None:
    state = load_job_state(job_id)
    undo = state.get("manual_undo", [])
    if not undo:
        return None

    last = undo.pop()
    df = _load_job_df(job_id)
    row_id = int(last["row_id"])
    kind = last.get("kind", "language")

    if kind == "sentiment":
        updates = {
            "label": last.get("label"),
            "tone_source": last.get("tone_source"),
        }
        sentiment_session = state.get("sentiment_session", {"labeled": 0, "by_tone": empty_tone_counts()})
        sentiment_session["labeled"] = max(0, sentiment_session.get("labeled", 1) - 1)
        by_tone = ensure_sentiment_session(sentiment_session)
        applied = canonical_tone(last.get("applied_tone"))
        if applied in by_tone:
            by_tone[applied] = max(0, by_tone[applied] - 1)
        session_patch = {"sentiment_session": sentiment_session}
    else:
        updates = {
            "language": last["language"],
            "label_source": last.get("label_source"),
            "needs_review": last.get("needs_review"),
            "confidence": last.get("confidence"),
        }
        session = state.get("manual_session", {"labeled": 0})
        session["labeled"] = max(0, session.get("labeled", 1) - 1)
        by_class = ensure_session_by_class(session)
        applied = canonical_language(last.get("applied_language"))
        if applied in by_class:
            by_class[applied] = max(0, by_class[applied] - 1)
        session_patch = {"manual_session": session}

    update_cached_row(job_id, row_id, updates)
    from job_cache import invalidate_queue_cache

    invalidate_queue_cache(job_id)
    schedule_job_save(job_id, row_id, updates)

    metrics = compute_metrics(df, {**state, **session_patch})
    schedule_state_save(
        job_id,
        {**state, "manual_undo": undo, **session_patch, "metrics_snapshot": metrics},
    )
    return {
        "row_id": row_id,
        "row": row_dict(df, row_id),
        "metrics": metrics,
    }
