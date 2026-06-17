"""Download and unpack KazNLP model weights from Hugging Face."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ID = "naadgob/kaznlp-weights"
ZIP_NAME = "models.zip"
MARKER = ROOT / "models" / "xlm-roberta" / "xlm-r_v2.pt"


def weights_present() -> bool:
    checks = (
        ROOT / "models" / "xlm-roberta" / "xlm-r_v2.pt",
        ROOT / "models" / "xlm-roberta" / "tone_v1.pt",
        ROOT / "models" / "fasttext" / "fasttext_v2.bin",
    )
    return all(p.is_file() for p in checks)


def download_and_extract(force: bool = False) -> Path:
    if weights_present() and not force:
        print("Веса уже на месте — пропуск HF download.")
        return MARKER

    from huggingface_hub import hf_hub_download

    print(f"Скачиваю {REPO_ID}/{ZIP_NAME} (~8.2 GB)…")
    archive = hf_hub_download(
        repo_id=REPO_ID,
        filename=ZIP_NAME,
        repo_type="dataset",
        local_dir=str(ROOT / "models" / "_hf_cache"),
        local_dir_use_symlinks=False,
    )
    archive_path = Path(archive)
    print(f"Распаковка {archive_path.name} → {ROOT}…")
    with zipfile.ZipFile(archive_path, "r") as zf:
        zf.extractall(ROOT)
    if not weights_present():
        raise RuntimeError("После распаковки не найдены xlm-r_v2.pt / tone_v1.pt / fasttext_v2.bin")
    print("Веса установлены.")
    return MARKER


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    force = "--force" in sys.argv
    try:
        download_and_extract(force=force)
    except Exception as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        print(
            f"Репозиторий: https://huggingface.co/datasets/{REPO_ID}\n"
            "Или распакуйте models/models.zip вручную в корень проекта.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
