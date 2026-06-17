"""Fast queue resolution for large labeling jobs."""

from __future__ import annotations

import re
from typing import Any

import numpy as np
import pandas as pd

from domain_heuristics import VALID_DOMAINS, domain_series
from job_cache import get_queue_cache, remove_row_from_queue_caches, set_queue_indices
from label_utils import canonical_tone
from text_heuristics import label_heuristics

KAZ_LETTERS_RE = re.compile(r"[әіңғүұқөһ]", re.I)
CYRILLIC_RE = re.compile(r"[а-яё]", re.I)
CYRILLIC_WORD_RE = re.compile(r"[а-яё]{3,}", re.I)
URL_RE = re.compile(r"https?://|t\.me/|tg://", re.I)

LARGE_JOB_ROWS = 10_000


def _lang_codes_fast(df: pd.DataFrame) -> pd.Series:
    raw = df["language"]
    empty = raw.isna() | raw.astype(str).str.strip().isin(["", "nan", "none", "null", "<na>"])
    normed = raw.astype(str).str.strip().str.lower().replace({"kaz": "kz", "kk": "kz"})
    normed = normed.where(~empty, other=None)
    return normed.where(normed.isin(["ru", "kz", "mixed"]), other=None)


def _llm_norm_series(df: pd.DataFrame) -> pd.Series:
    if "llm_language" not in df.columns:
        return pd.Series([None] * len(df), index=df.index, dtype="object")
    raw = df["llm_language"]
    empty = raw.isna() | raw.astype(str).str.strip().isin(["", "nan", "none", "null", "<na>"])
    normed = raw.astype(str).str.strip().str.lower().replace({"kaz": "kz", "kk": "kz"})
    normed = normed.where(~empty, other=None)
    return normed.where(normed.isin(["ru", "kz", "mixed"]), other=None)


def _effective_lang_series(df: pd.DataFrame) -> pd.Series:
    """Manual label when set, otherwise LLM hint (upload clears language for review)."""
    manual = _lang_codes_fast(df)
    hint = _llm_norm_series(df)
    return manual.where(manual.notna(), hint)


def _text_series(df: pd.DataFrame) -> pd.Series:
    return df["text"].astype(str)


def _has_kazakh_letters_series(texts: pd.Series) -> pd.Series:
    return texts.str.contains(KAZ_LETTERS_RE, na=False)


def _low_signal_series(texts: pd.Series) -> pd.Series:
    stripped = texts.str.strip()
    word_counts = texts.str.findall(r"\w+", flags=re.UNICODE).str.len()
    alpha_len = stripped.str.replace(r"\s+", "", regex=True).str.len()
    return (
        (stripped.str.len() < 12)
        | (texts.str.contains(URL_RE, na=False) & (word_counts <= 3))
        | (alpha_len <= 4)
    )


def _potential_real_mixed_series(texts: pd.Series, has_kz: pd.Series) -> pd.Series:
    has_cyr = texts.str.contains(CYRILLIC_RE, na=False)
    has_ru_word = texts.str.contains(CYRILLIC_WORD_RE, na=False)
    return has_kz & (has_cyr | has_ru_word)


def _russian_cyrillic_series(texts: pd.Series) -> pd.Series:
    return texts.str.contains(CYRILLIC_WORD_RE, na=False)


def row_has_kazakh_letters(text: str) -> bool:
    return bool(KAZ_LETTERS_RE.search(text))


def _tone_codes_fast(df: pd.DataFrame) -> pd.Series:
    if "label" not in df.columns:
        return pd.Series([None] * len(df), index=df.index, dtype="object")
    return df["label"].apply(lambda x: canonical_tone(x))


def _build_mask(
    df: pd.DataFrame,
    filter_name: str,
    search: str,
    class_filter: str,
    domain_filter: str = "any",
) -> pd.Series:
    texts = _text_series(df)
    langs = _lang_codes_fast(df)
    effective = _effective_lang_series(df)
    has_kz = _has_kazakh_letters_series(texts)
    has_ru_cyr = _russian_cyrillic_series(texts)
    mask = pd.Series(True, index=df.index)

    if class_filter == "unlabeled":
        mask &= langs.isna()
    elif class_filter != "any":
        mask &= effective == class_filter

    if search:
        mask &= texts.str.lower().str.contains(search.lower(), na=False, regex=False)

    llm_norm = _llm_norm_series(df)
    src = df["label_source"].astype(str).str.strip().str.lower() if "label_source" in df.columns else pd.Series([""] * len(df))
    tone_src = (
        df["tone_source"].astype(str).str.strip().str.lower()
        if "tone_source" in df.columns
        else pd.Series([""] * len(df))
    )
    tones = _tone_codes_fast(df)
    needs = df["needs_review"].fillna(False).astype(bool) if "needs_review" in df.columns else pd.Series([False] * len(df))
    prm = _potential_real_mixed_series(texts, has_kz)
    low_sig = _low_signal_series(texts)

    if domain_filter != "any" and domain_filter in VALID_DOMAINS:
        mask &= domain_series(texts) == domain_filter

    if filter_name == "all":
        pass
    elif filter_name == "unlabeled":
        mask &= langs.isna()
    elif filter_name == "unlabeled_kazakh":
        mask &= langs.isna() & has_kz
    elif filter_name == "mixed":
        mask &= effective == "mixed"
    elif filter_name == "llm_mixed":
        mask &= llm_norm == "mixed"
    elif filter_name == "needs_review":
        mask &= needs
    elif filter_name == "manual":
        mask &= src == "manual"
    elif filter_name == "disagree":
        mask &= langs.notna() & llm_norm.notna() & (langs != llm_norm)
    elif filter_name == "label_ru":
        mask &= effective == "ru"
    elif filter_name == "label_kz":
        mask &= effective == "kz"
    elif filter_name == "label_mixed":
        mask &= effective == "mixed"
    elif filter_name == "potential_real_mixed":
        mask &= prm
    elif filter_name == "low_signal":
        mask &= low_sig
    elif filter_name == "ru_but_kazakh":
        mask &= (effective == "ru") & has_kz
    elif filter_name == "kaz_letters_in_ru_text":
        mask &= has_kz & has_ru_cyr
    elif filter_name == "mixed_false_positive":
        mask &= (effective == "mixed") & ~prm
    elif filter_name == "kz_no_signal":
        mask &= (effective == "kz") & ~has_kz
    elif filter_name == "suspicious":
        idxs = np.flatnonzero(mask.values)
        suspicious = pd.Series(False, index=df.index)
        for i in idxs:
            lang = effective.at[i]
            if lang is None or (isinstance(lang, float) and pd.isna(lang)):
                continue
            if label_heuristics(str(df.at[i, "text"]), lang)["suspicious_label"]:
                suspicious.at[i] = True
        mask &= suspicious
    elif filter_name == "unlabeled_tone":
        mask &= tones.isna()
    elif filter_name == "mixed_unlabeled_tone":
        mask &= (effective == "mixed") & tones.isna()
    elif filter_name == "tone_positive":
        mask &= tones == "positive"
    elif filter_name == "tone_negative":
        mask &= tones == "negative"
    elif filter_name == "tone_skip":
        mask &= tones == "skip"
    elif filter_name == "tone_manual":
        mask &= tone_src == "manual"
    elif filter_name == "domain_review":
        mask &= domain_series(texts) == "review"
    elif filter_name == "domain_logistics":
        mask &= domain_series(texts) == "logistics"
    elif filter_name == "domain_other":
        mask &= domain_series(texts) == "other"
    else:
        mask &= False

    return mask


def queue_cache_key(filter_name: str, search: str, class_filter: str, domain_filter: str = "any") -> str:
    return f"{filter_name}|{class_filter}|{domain_filter}|{search}"


def get_queue_indices(
    job_id: str,
    df: pd.DataFrame,
    filter_name: str,
    search: str = "",
    class_filter: str = "any",
    domain_filter: str = "any",
    *,
    rebuild: bool = False,
) -> np.ndarray:
    key = queue_cache_key(filter_name, search, class_filter, domain_filter)
    job_cache = get_queue_cache(job_id)
    if not rebuild and key in job_cache:
        return job_cache[key]
    mask = _build_mask(df, filter_name, search, class_filter, domain_filter)
    indices = np.flatnonzero(mask.values)
    set_queue_indices(job_id, key, indices)
    return indices


def queue_page(
    job_id: str,
    df: pd.DataFrame,
    filter_name: str,
    search: str = "",
    class_filter: str = "any",
    domain_filter: str = "any",
    position: int = 0,
    *,
    rebuild: bool = False,
) -> dict[str, Any]:
    indices = get_queue_indices(job_id, df, filter_name, search, class_filter, domain_filter, rebuild=rebuild)
    total = int(len(indices))
    if total == 0:
        return {
            "total": 0,
            "position": 0,
            "row_id": None,
            "has_prev": False,
            "has_next": False,
        }
    pos = max(0, min(position, total - 1))
    row_id = int(indices[pos])
    return {
        "total": total,
        "position": pos,
        "row_id": row_id,
        "has_prev": pos > 0,
        "has_next": pos < total - 1,
    }


def queue_next_after_label(
    job_id: str,
    df: pd.DataFrame,
    filter_name: str,
    search: str,
    class_filter: str,
    position: int,
    labeled_row_id: int,
    domain_filter: str = "any",
) -> dict[str, Any]:
    """Next row after manual label — always skip the row just labeled."""
    remove_row_from_queue_caches(job_id, labeled_row_id)
    key = queue_cache_key(filter_name, search, class_filter, domain_filter)
    job_cache = get_queue_cache(job_id)
    if key in job_cache:
        indices = job_cache[key]
        indices = indices[indices != labeled_row_id]
        set_queue_indices(job_id, key, indices)
    else:
        indices = np.flatnonzero(_build_mask(df, filter_name, search, class_filter, domain_filter).values)
        indices = indices[indices != labeled_row_id]
        set_queue_indices(job_id, key, indices)

    total = int(len(indices))
    if total == 0:
        return {
            "total": 0,
            "position": 0,
            "row_id": None,
            "has_prev": False,
            "has_next": False,
        }
    pos = max(0, min(position, total - 1))
    row_id = int(indices[pos])
    return {
        "total": total,
        "position": pos,
        "row_id": row_id,
        "has_prev": pos > 0,
        "has_next": pos < total - 1,
    }


def queue_batch(
    job_id: str,
    df: pd.DataFrame,
    filter_name: str,
    search: str = "",
    class_filter: str = "any",
    domain_filter: str = "any",
    position: int = 0,
    batch: int = 1,
) -> dict[str, Any]:
    indices = get_queue_indices(job_id, df, filter_name, search, class_filter, domain_filter)
    total = int(len(indices))
    if total == 0:
        return {"total": 0, "position": 0, "rows": [], "has_prev": False, "has_next": False}
    pos = max(0, min(position, total - 1))
    batch = max(1, min(batch, 50))
    rows: list[dict[str, Any]] = []
    for offset in range(batch):
        p = pos + offset
        if p >= total:
            break
        rid = int(indices[p])
        rows.append({"position": p, "row_id": rid})
    last_pos = rows[-1]["position"] if rows else pos
    return {
        "total": total,
        "position": pos,
        "rows": rows,
        "has_prev": pos > 0,
        "has_next": last_pos < total - 1,
    }


def queue_shuffle_batch(
    job_id: str,
    df: pd.DataFrame,
    filter_name: str,
    search: str = "",
    class_filter: str = "any",
    domain_filter: str = "any",
    batch: int = 20,
) -> dict[str, Any]:
    indices = get_queue_indices(job_id, df, filter_name, search, class_filter, domain_filter)
    total = int(len(indices))
    if total == 0:
        return {
            "mode": "shuffle",
            "total": 0,
            "batch_size": 0,
            "rows": [],
            "has_prev": False,
            "has_next": False,
        }
    batch = max(1, min(batch, 50))
    n = min(batch, total)
    picked = np.random.default_rng().choice(indices, size=n, replace=False)
    rows = [{"position": i, "row_id": int(rid)} for i, rid in enumerate(picked)]
    return {
        "mode": "shuffle",
        "total": total,
        "batch_size": n,
        "rows": rows,
        "has_prev": False,
        "has_next": n > 1,
    }


def compute_heuristic_metrics_fast(df: pd.DataFrame) -> dict[str, int]:
    texts = _text_series(df)
    langs = _lang_codes_fast(df)
    has_kz = _has_kazakh_letters_series(texts)
    prm = _potential_real_mixed_series(texts, has_kz)
    low_sig = _low_signal_series(texts)
    unlabeled = langs.isna()
    labeled = langs.notna()
    is_ru = langs == "ru"
    is_kz = langs == "kz"
    is_mixed = langs == "mixed"
    has_ru_cyr = _russian_cyrillic_series(texts)

    return {
        "potential_real_mixed": int(prm.sum()),
        "potential_real_mixed_labeled": int((prm & labeled).sum()),
        "potential_real_mixed_unlabeled": int((prm & unlabeled).sum()),
        "suspicious_labeled": 0,
        "ru_with_kazakh_letters": int((is_ru & has_kz).sum()),
        "kaz_letters_in_ru_text": int((has_kz & has_ru_cyr).sum()),
        "mixed_false_positive": int((is_mixed & ~prm).sum()),
        "mixed_with_kazakh_letters": int((is_mixed & has_kz).sum()),
        "kz_no_signal": int((is_kz & ~has_kz).sum()),
        "unlabeled_kazakh": int((unlabeled & has_kz).sum()),
        "low_signal_text": int(low_sig.sum()),
    }


def compute_heuristic_metrics_fast_lite(df: pd.DataFrame) -> dict[str, int]:
    return compute_heuristic_metrics_fast(df)
