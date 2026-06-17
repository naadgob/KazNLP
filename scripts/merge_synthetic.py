"""Merge synthetic CSV batches, QC, dedup vs gold. Usage: python scripts/merge_synthetic.py"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "labeling_service"))

from precision_filter import has_kazakh_signal, has_russian_signal, KAZAKH_CHARS
from text_heuristics import has_kazakh_letters

GOLD = ROOT / "data/processed/gold_v1.csv"
SYNTH_DIR = ROOT / "data/processed/synthetic"
OUT_ALL = SYNTH_DIR / "synthetic_all.csv"
OUT_QC = SYNTH_DIR / "synthetic_qc_report.txt"

WORD_RE = re.compile(r"[\w']+", re.UNICODE)
KAZAKH_SPECIAL = set("әіңғүұқөһ")


def normalize_text(text) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    t = str(text).strip().casefold()
    t = re.sub(r"https?://\S+|t\.me/\S+", " ", t, flags=re.I)
    t = re.sub(r"@[\w.]+", "[USER]", t)
    t = re.sub(r"#(\w+)", r"\1", t)
    t = re.sub(r"[^\w\s.,!?\-']", " ", t, flags=re.UNICODE)
    t = re.sub(r"([)\]}])\1{2,}", r"\1", t)
    t = re.sub(r"([:;])\1{2,}", r"\1", t)
    t = re.sub(r"!{2,}", "!", t)
    t = re.sub(r"\?{2,}", "?", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def word_count(text: str) -> int:
    return len(WORD_RE.findall(str(text)))


def ru_word_count(text: str) -> int:
    words = WORD_RE.findall(str(text).lower())
    ru = [w for w in words if re.search(r"[а-яё]", w) and not any(c in w for c in KAZAKH_SPECIAL)]
    return len(ru)


def kz_word_count(text: str) -> int:
    words = WORD_RE.findall(str(text).lower())
    kz = [w for w in words if any(c in w for c in KAZAKH_SPECIAL) or has_kazakh_signal(w)]
    # fallback: words with kazakh morphology markers in full text segments
    return len([w for w in words if any(c in w for c in KAZAKH_SPECIAL)])


def qc_row(text: str, lang: str) -> list[str]:
    issues: list[str] = []
    lang = lang.strip().lower()
    t = str(text)
    wc = word_count(t)
    sig_ru = has_russian_signal(t)
    sig_kz = has_kazakh_signal(t)
    has_spec = has_kazakh_letters(t)

    if lang == "mixed":
        if not (sig_ru and sig_kz):
            issues.append("mixed_missing_bilingual_signal")
        parts = re.split(r"[.!?]+", t)
        ru_parts = sum(1 for p in parts if len(p.strip()) >= 4 and has_russian_signal(p) and not has_kazakh_signal(p))
        kz_parts = sum(1 for p in parts if len(p.strip()) >= 4 and has_kazakh_signal(p) and not has_russian_signal(p))
        if wc <= 5 and not (ru_parts or kz_parts) and not (sig_ru and sig_kz):
            issues.append("mixed_short_weak")
    elif lang == "kz":
        if not sig_kz and not has_spec:
            issues.append("kz_no_kazakh_signal")
        if sig_ru and sig_kz and ru_word_count(t) >= 3 and kz_word_count(t) >= 2:
            # possible mislabel as kz when looks mixed
            sentences = [p.strip() for p in re.split(r"[.!?]+", t) if len(p.strip()) >= 8]
            ru_s = sum(1 for p in sentences if has_russian_signal(p) and not has_kazakh_signal(p))
            kz_s = sum(1 for p in sentences if has_kazakh_signal(p) and not has_russian_signal(p))
            if ru_s >= 1 and kz_s >= 1:
                issues.append("kz_looks_like_two_sentences_mixed")
    elif lang == "ru":
        if has_spec:
            issues.append("ru_has_kazakh_letters")
        if sig_kz and sig_ru:
            issues.append("ru_has_bilingual_signal")

    return issues


def load_batches() -> pd.DataFrame:
    frames = []
    for p in sorted(SYNTH_DIR.glob("synth_batch_*.csv")):
        df = pd.read_csv(p)
        df["batch_file"] = p.name
        frames.append(df)
    if not frames:
        raise SystemExit(f"No synth_batch_*.csv in {SYNTH_DIR}")
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    gold = pd.read_csv(GOLD)
    gold_norms = set(gold["text"].map(normalize_text))

    synth = load_batches()
    synth["text_norm"] = synth["text"].map(normalize_text)
    synth = synth[synth["text_norm"].str.len() > 0].copy()

    dup_gold = synth["text_norm"].isin(gold_norms)
    dup_self = synth["text_norm"].duplicated(keep="first")

    qc_lines: list[str] = []
    flags: list[list[str]] = []
    for _, r in synth.iterrows():
        iss = qc_row(r["text"], r["language"])
        flags.append(iss)
        if iss:
            qc_lines.append(f"[{r['language']}] {r['batch_file']}: {iss} | {r['text'][:100]}")

    synth["qc_flags"] = [",".join(x) if x else "" for x in flags]
    synth_out = synth[~dup_gold & ~dup_self].copy()
    synth_out.to_csv(OUT_ALL, index=False, encoding="utf-8-sig")

    by_lang = synth_out["language"].value_counts().to_dict()
    flagged = (synth_out["qc_flags"] != "").sum()
    train_cap = int(len(gold) * 0.7 * 0.25)

    manifest = [
        f"Total rows (after dedup): {len(synth_out)}",
        f"Train cap 25% (~): {train_cap}",
        f"Removed dup vs gold: {int(dup_gold.sum())}",
        f"Removed dup within synth: {int(dup_self.sum())}",
        f"By language: {by_lang}",
        f"QC flagged (heuristic only): {flagged}",
    ]
    if "batch_file" in synth_out.columns:
        manifest.append("Batches:")
        for bf, n in synth_out["batch_file"].value_counts().sort_index().items():
            manifest.append(f"  {bf}: {n}")

    report = manifest + ["", "=== QC sample ===", *qc_lines[:40]]
    OUT_QC.write_text("\n".join(report), encoding="utf-8")
    (SYNTH_DIR / "synthetic_manifest.txt").write_text("\n".join(manifest), encoding="utf-8")

    sample_n = max(1, len(synth_out) // 10)
    synth_out.sample(n=sample_n, random_state=42).to_csv(
        SYNTH_DIR / "synthetic_manual_review_10pct.csv", index=False, encoding="utf-8-sig"
    )

    print("\n".join(manifest))
    print(f"\nSaved: {OUT_ALL}")


if __name__ == "__main__":
    main()
