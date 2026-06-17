"""Download open-source RU/KZ tone models into models/tone_pretrained/."""

from __future__ import annotations

import sys
from pathlib import Path

from huggingface_hub import snapshot_download

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "models" / "tone_pretrained"

MODELS = {
    "ru_rubert_rureviews": {
        "repo_id": "sismetanin/rubert_conversational-ru-sentiment-rureviews",
        "description": "RuBERT-Conversational, RuReviews e-commerce (neu/pos/neg)",
    },
    "kz_kazakh_sentiment_bert": {
        "repo_id": "R3iwan/kazakh-sentiment-bert",
        "description": "BERT multilingual, Kazakh entertainment reviews (pos/neu/neg)",
    },
}


def download_all() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    failed = 0
    for folder, meta in MODELS.items():
        dest = OUT / folder
        print(f"\n=== {folder} ===")
        print(f"    {meta['description']}")
        print(f"    {meta['repo_id']} -> {dest}")
        try:
            snapshot_download(repo_id=meta["repo_id"], local_dir=str(dest))
            print("    OK")
        except Exception as exc:
            failed += 1
            print(f"    FAILED: {exc}", file=sys.stderr)
            print("    Re-run after fixing network or HF access.", file=sys.stderr)
    return failed


if __name__ == "__main__":
    raise SystemExit(download_all())
