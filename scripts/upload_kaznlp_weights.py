"""Upload models/models.zip to Hugging Face Hub (one-time, author only).

Requires HF token with **write** access:
  https://huggingface.co/settings/tokens

  set HF_TOKEN=hf_...   # Windows cmd
  $env:HF_TOKEN="hf_..."  # PowerShell

  python scripts/upload_kaznlp_weights.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Faster large uploads when hf_transfer is installed: pip install hf_transfer
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "models" / "models.zip"
REPO_ID = "naadgob/kaznlp-weights"
README = ROOT / "models" / "HF_DATASET_README.md"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if not ZIP.is_file():
        print(f"Не найден {ZIP}", file=sys.stderr)
        return 1
    if not os.environ.get("HF_TOKEN"):
        print(
            "Задайте HF_TOKEN с правами write (Settings → Access Tokens → Write).",
            file=sys.stderr,
        )
        return 1

    from huggingface_hub import HfApi

    api = HfApi()
    me = api.whoami()
    print(f"HF user: {me.get('name')}")
    print(f"Создаю dataset {REPO_ID}…")
    api.create_repo(REPO_ID, repo_type="dataset", exist_ok=True)

    size_gb = ZIP.stat().st_size / (1024**3)
    print(f"Загрузка models.zip ({size_gb:.2f} GB) — может занять 20–60 мин…")
    api.upload_file(
        path_or_fileobj=str(ZIP),
        path_in_repo="models.zip",
        repo_id=REPO_ID,
        repo_type="dataset",
        commit_message="KazNLP demo weights (FastText, XLM-R LID/tone, RU/KZ pretrained)",
    )
    if README.is_file():
        api.upload_file(
            path_or_fileobj=str(README),
            path_in_repo="README.md",
            repo_id=REPO_ID,
            repo_type="dataset",
            commit_message="Dataset card",
        )

    url = f"https://huggingface.co/datasets/{REPO_ID}"
    print(f"\nГотово: {url}")
    print("Добавьте ссылку в README (уже есть, если вы на последней версии).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
