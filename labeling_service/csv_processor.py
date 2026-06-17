"""CSV validation, row selection, and incremental save for labeling jobs."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

import pandas as pd

from label_utils import canonical_language, canonical_tone, is_empty_tone

REQUIRED_COLUMNS = ("text", "language", "label")
MAX_FILE_BYTES = 50 * 1024 * 1024
MAX_ROWS_WARN = 500_000

UPLOADS_DIR = Path(__file__).parent / "uploads"


def new_job_id() -> str:
    return uuid.uuid4().hex[:12]


def job_dir(job_id: str) -> Path:
    path = UPLOADS_DIR / job_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_upload(content: bytes, filename: str) -> None:
    if len(content) > MAX_FILE_BYTES:
        raise ValueError(f"File too large (max {MAX_FILE_BYTES // (1024 * 1024)} MB)")
    if not filename.lower().endswith(".csv"):
        raise ValueError("Only CSV files are supported")


def load_dataframe(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8", on_bad_lines="skip")
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    return df


def is_empty_language(val: Any) -> bool:
    if val is None or pd.isna(val):
        return True
    s = str(val).strip().lower()
    return s in ("", "nan", "none", "null", "<na>")


def rows_to_process(df: pd.DataFrame, only_empty: bool, resume_from: set[int] | None = None) -> list[int]:
    """Return row indices that need labeling."""
    indices: list[int] = []
    for idx in range(len(df)):
        if resume_from and idx in resume_from:
            continue
        if only_empty:
            if is_empty_language(df.at[idx, "language"]):
                indices.append(idx)
        else:
            indices.append(idx)
    return indices


def language_stats(df: pd.DataFrame) -> dict[str, int]:
    stats = {"ru": 0, "kz": 0, "mixed": 0}
    for i in range(len(df)):
        lang = canonical_language(df.at[i, "language"])
        if lang in stats:
            stats[lang] += 1
    return stats


def normalize_language_column(df: pd.DataFrame) -> None:
    """kaz -> kz in place for export consistency."""
    for i in range(len(df)):
        lang = canonical_language(df.at[i, "language"])
        if lang:
            df.at[i, "language"] = lang


def analyze_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    empty_lang = sum(is_empty_language(df.at[i, "language"]) for i in range(len(df)))
    lang_stats = language_stats(df)
    preview = []
    for i in range(min(5, len(df))):
        preview.append(
            {
                "text": str(df.at[i, "text"])[:120],
                "language": "" if is_empty_language(df.at[i, "language"]) else str(df.at[i, "language"]),
                "label": "" if pd.isna(df.at[i, "label"]) else str(df.at[i, "label"]),
            }
        )
    warn_rows = len(df) > MAX_ROWS_WARN
    return {
        "total_rows": len(df),
        "empty_language": empty_lang,
        "filled_language": len(df) - empty_lang,
        "language_stats": lang_stats,
        "columns_ok": True,
        "preview": preview,
        "warn_large": warn_rows,
    }


def ensure_output_columns(df: pd.DataFrame) -> pd.DataFrame:
    if "confidence" not in df.columns:
        df["confidence"] = pd.NA
    if "needs_review" not in df.columns:
        df["needs_review"] = pd.NA
    if "filter_note" not in df.columns:
        df["filter_note"] = pd.NA
    if "llm_language" not in df.columns:
        df["llm_language"] = pd.NA
    if "label_source" not in df.columns:
        df["label_source"] = pd.NA
    if "tone_source" not in df.columns:
        df["tone_source"] = pd.NA
    df["language"] = df["language"].astype("object")
    df["label"] = df["label"].astype("object")
    df["tone_source"] = df["tone_source"].astype("object")
    df["llm_language"] = df["llm_language"].astype("object")
    df["label_source"] = df["label_source"].astype("object")
    df["confidence"] = df["confidence"].astype("object")
    df["needs_review"] = df["needs_review"].astype("object")
    return df


def prepare_manual_review(df: pd.DataFrame) -> None:
    """Save LLM/auto labels as llm_language hint; clear language for non-manual rows."""
    for i in range(len(df)):
        src = ""
        if "label_source" in df.columns and not pd.isna(df.at[i, "label_source"]):
            src = str(df.at[i, "label_source"]).strip().lower()
        if src == "manual":
            continue

        if not is_empty_language(df.at[i, "language"]):
            lang = canonical_language(df.at[i, "language"])
            if lang:
                if is_empty_language(df.at[i, "llm_language"]):
                    df.at[i, "llm_language"] = lang
                df.at[i, "language"] = pd.NA
                df.at[i, "label_source"] = pd.NA


def apply_labels(df: pd.DataFrame, labels: list[dict]) -> None:
    """Update language/confidence/needs_review; never touch label."""
    for item in labels:
        idx = item["row_id"]
        if idx < 0 or idx >= len(df):
            continue
        df.at[idx, "language"] = item["language"]
        df.at[idx, "confidence"] = item.get("confidence", pd.NA)
        df.at[idx, "needs_review"] = item.get("needs_review", pd.NA)
        df.at[idx, "label_source"] = "llm"
        if "filter_note" in item and item.get("filter_note"):
            df.at[idx, "filter_note"] = item["filter_note"]


def save_state(job_id: str, state: dict) -> None:
    path = job_dir(job_id) / "state.json"
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def load_state(job_id: str) -> dict | None:
    path = job_dir(job_id) / "state.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_output(df: pd.DataFrame, job_id: str) -> Path:
    normalize_language_column(df)
    out = job_dir(job_id) / "output.csv"
    df.to_csv(out, index=False, encoding="utf-8-sig")
    return out


EXPORT_MODES = frozenset({"full", "labeled", "manual", "tone_labeled", "tone_manual"})


def export_row_indices(df: pd.DataFrame, mode: str = "full") -> list[int]:
    if mode == "full":
        return list(range(len(df)))
    if mode == "labeled":
        return [i for i in range(len(df)) if not is_empty_language(df.at[i, "language"])]
    if mode == "manual":
        if "label_source" not in df.columns:
            return []
        return [
            i
            for i in range(len(df))
            if str(df.at[i, "label_source"]).strip().lower() == "manual"
        ]
    if mode == "tone_labeled":
        return [
            i
            for i in range(len(df))
            if canonical_tone(df.at[i, "label"]) in ("positive", "negative")
        ]
    if mode == "tone_manual":
        if "tone_source" not in df.columns:
            return []
        return [
            i
            for i in range(len(df))
            if str(df.at[i, "tone_source"]).strip().lower() == "manual"
        ]
    raise ValueError(f"Unknown export mode: {mode}")


def export_dataframe(df: pd.DataFrame, mode: str = "full") -> pd.DataFrame:
    if mode not in EXPORT_MODES:
        raise ValueError(f"mode must be one of: {', '.join(sorted(EXPORT_MODES))}")
    indices = export_row_indices(df, mode)
    if not indices:
        return df.iloc[0:0].copy()
    return df.iloc[indices].copy()


def export_counts(df: pd.DataFrame) -> dict[str, int]:
    from queue_engine import _lang_codes_fast

    total = len(df)
    langs = _lang_codes_fast(df)
    labeled = int(langs.notna().sum())
    manual = 0
    if "label_source" in df.columns:
        manual = int((df["label_source"].astype(str).str.strip().str.lower() == "manual").sum())
    tone_labeled = sum(
        1 for i in range(total) if canonical_tone(df.at[i, "label"]) in ("positive", "negative")
    )
    tone_manual = 0
    if "tone_source" in df.columns:
        tone_manual = int((df["tone_source"].astype(str).str.strip().str.lower() == "manual").sum())
    tone_skip = sum(1 for i in range(total) if canonical_tone(df.at[i, "label"]) == "skip")
    tone_unlabeled = sum(1 for i in range(total) if is_empty_tone(df.at[i, "label"]))
    return {
        "total": total,
        "full": total,
        "labeled": labeled,
        "manual": manual,
        "unlabeled": total - labeled,
        "tone_labeled": tone_labeled,
        "tone_manual": tone_manual,
        "tone_skip": tone_skip,
        "tone_unlabeled": tone_unlabeled,
    }


def init_job(content: bytes, filename: str) -> tuple[str, dict]:
    validate_upload(content, filename)
    job_id = new_job_id()
    d = job_dir(job_id)
    input_path = d / "input.csv"
    input_path.write_bytes(content)
    df = load_dataframe(input_path)
    df = ensure_output_columns(df.copy())
    prepare_manual_review(df)
    save_output(df, job_id)
    stats = analyze_dataframe(df)
    save_state(
        job_id,
        {
            "filename": filename,
            "done": False,
            "processed": 0,
            "total_to_process": len(df),
            "only_empty": False,
            "stats": {"ru": 0, "kz": 0, "mixed": 0},
            "labeled_indices": [],
            "manual_session": {"labeled": 0, "started_at": None, "by_class": {"ru": 0, "kz": 0, "mixed": 0}},
            "sentiment_session": {
                "labeled": 0,
                "started_at": None,
                "by_tone": {"positive": 0, "negative": 0, "skip": 0},
            },
            "manual_undo": [],
        },
    )
    return job_id, stats
