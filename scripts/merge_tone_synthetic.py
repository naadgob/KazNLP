"""Merge tone synthetic batches with audited gold. QC + dedup."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "labeling_service"))
sys.path.insert(0, str(ROOT / "scripts"))

from merge_synthetic import normalize_text, qc_row  # noqa: E402
from text_heuristics import text_signals  # noqa: E402

GOLD = ROOT / "data/processed/tone_mixed_balanced_audited.csv"
SYNTH = ROOT / "data/processed/tone_synthetic.csv"
OUT_MERGED = ROOT / "data/processed/tone_train_mixed.csv"


def load_synthetic() -> pd.DataFrame:
    if not SYNTH.is_file():
        raise SystemExit(f"Missing {SYNTH} — run scripts/generate_tone_synthetic.py first")
    return pd.read_csv(SYNTH)


def tone_qc(text: str, label: str) -> list[str]:
    issues = list(qc_row(text, "mixed"))
    sig = text_signals(text)
    if not sig["potential_real_mixed"]:
        issues.append("weak_bilingual")
    if label not in ("positive", "negative"):
        issues.append("bad_label")
    return issues


def main() -> None:
    gold = pd.read_csv(GOLD)
    gold["text_norm"] = gold["text"].map(normalize_text)
    gold_norms = set(gold["text_norm"])

    synth = load_synthetic()
    synth["label"] = synth["label"].astype(str).str.strip().str.lower()
    synth = synth[synth["label"].isin(["positive", "negative"])].copy()
    synth["text_norm"] = synth["text"].map(normalize_text)

    dup_gold = synth["text_norm"].isin(gold_norms)
    dup_self = synth["text_norm"].duplicated(keep="first")

    flags: list[str] = []
    for _, r in synth.iterrows():
        iss = tone_qc(str(r["text"]), str(r["label"]))
        flags.append(",".join(iss) if iss else "")

    synth["qc_flags"] = flags
    bad_qc = synth["qc_flags"] != ""
    synth_clean = synth[~dup_gold & ~dup_self & ~bad_qc].copy()

    gold_out = gold.drop(columns=["text_norm"], errors="ignore")
    merged = pd.concat([gold_out, synth_clean.drop(columns=["text_norm"], errors="ignore")], ignore_index=True)
    merged["text_norm"] = merged["text"].map(normalize_text)
    merged = merged.drop_duplicates(subset=["text_norm"], keep="first").drop(columns=["text_norm"])
    merged.to_csv(OUT_MERGED, index=False, encoding="utf-8-sig")

    manifest = {
        "gold_rows": len(gold),
        "synth_raw": len(synth),
        "synth_after_qc_dedup": len(synth_clean),
        "merged_total": len(merged),
        "merged_positive": int((merged["label"] == "positive").sum()),
        "merged_negative": int((merged["label"] == "negative").sum()),
        "removed_dup_gold": int(dup_gold.sum()),
        "removed_dup_self": int(dup_self.sum()),
        "removed_qc": int(bad_qc.sum()),
        "pct_synthetic": round(100 * len(synth_clean) / len(merged), 1),
        "batches": synth_clean.groupby("batch").size().to_dict() if "batch" in synth_clean.columns else {},
    }
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Wrote {OUT_MERGED}")


if __name__ == "__main__":
    main()
