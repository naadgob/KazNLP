"""Prepare all model paths for the demo (verify, download RU/KZ, link XLM-R weights)."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XLM = ROOT / "models" / "xlm-roberta"
LID_DIR = XLM / "lid"
TONE_DIR = XLM / "tone"
PRETRAINED = ROOT / "models" / "tone_pretrained"

CANONICAL = {
    XLM / "xlm-r_v2.pt": [
        LID_DIR / "xlm-r_v2.pt",
        Path.home() / "Downloads" / "xlm-r_v2.pt",
    ],
    XLM / "tone_v1.pt": [
        TONE_DIR / "tone_v1.pt",
        TONE_DIR / "xlm-r_v1.pt",
        TONE_DIR / "xlm-r_v2.pt",
        Path.home() / "Downloads" / "tone_v1.pt",
    ],
}

PRETRAINED_DIRS = (
    PRETRAINED / "ru_rubert_rureviews",
    PRETRAINED / "kz_kazakh_sentiment_bert",
)


def _first_existing(candidates: list[Path]) -> Path | None:
    for path in candidates:
        if path.is_file():
            return path
    return None


def _link_or_copy(src: Path, dst: Path) -> str:
    if dst.exists():
        if dst.resolve() == src.resolve():
            return "ok"
        return "ok"
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(src, dst)
        return "linked"
    except OSError:
        shutil.copy2(src, dst)
        return "copied"


def ensure_xlm_weights() -> list[str]:
    actions: list[str] = []
    LID_DIR.mkdir(parents=True, exist_ok=True)
    TONE_DIR.mkdir(parents=True, exist_ok=True)

    for dest, sources in CANONICAL.items():
        if dest.is_file():
            actions.append(f"OK  {dest.relative_to(ROOT)}")
            continue
        src = _first_existing(sources)
        if src is None:
            raise FileNotFoundError(
                f"Не найден файл для {dest.name}. Положите вручную в {dest.parent}/ "
                f"или в Downloads."
            )
        how = _link_or_copy(src, dest)
        src_disp = src.relative_to(ROOT) if src.is_relative_to(ROOT) else src
        actions.append(f"{how:6} {dest.relative_to(ROOT)} <- {src_disp}")
    return actions


def pretrained_ok(path: Path) -> bool:
    if not path.is_dir():
        return False
    weights = list(path.glob("*.bin")) + list(path.glob("*.safetensors"))
    return bool(weights)


def ensure_pretrained() -> None:
    missing = [p for p in PRETRAINED_DIRS if not pretrained_ok(p)]
    if not missing:
        return
    print("Скачиваю RU/KZ pretrained tone…")
    import subprocess

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "download_tone_pretrained.py")],
        cwd=ROOT,
    )
    failed = proc.returncode
    if failed:
        raise RuntimeError("Не удалось скачать tone_pretrained — проверьте сеть.")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("KazNLP · setup demo models\n")

    if not all(
        p.is_file()
        for p in (
            XLM / "xlm-r_v2.pt",
            XLM / "tone_v1.pt",
            ROOT / "models" / "fasttext" / "fasttext_v2.bin",
        )
    ):
        print("Веса не найдены — пробую Hugging Face…")
        import subprocess

        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "download_kaznlp_weights.py")],
            cwd=ROOT,
        )
        if proc.returncode != 0:
            print(
                "Скачайте веса: python scripts/download_kaznlp_weights.py\n"
                "https://huggingface.co/datasets/naadgob/kaznlp-weights",
                file=sys.stderr,
            )
            return 1

    ensure_pretrained()
    for line in ensure_xlm_weights():
        print(line)

    checks = [
        ("LID v2", XLM / "xlm-r_v2.pt"),
        ("Mixed tone v1", XLM / "tone_v1.pt"),
        ("RU tone", PRETRAINED / "ru_rubert_rureviews"),
        ("KZ tone", PRETRAINED / "kz_kazakh_sentiment_bert"),
    ]
    print()
    all_ok = True
    for name, path in checks:
        ok = path.is_file() or pretrained_ok(path)
        mark = "OK" if ok else "MISSING"
        print(f"  [{mark}] {name}: {path.relative_to(ROOT)}")
        all_ok = all_ok and ok

    if not all_ok:
        print("\nНе все модели на месте.", file=sys.stderr)
        return 1
    print("\nГотово — можно запускать: python run_demo.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
