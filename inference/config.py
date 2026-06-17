from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
XLM_DIR = ROOT / "models" / "xlm-roberta"
RU_TONE_DIR = ROOT / "models" / "tone_pretrained" / "ru_rubert_rureviews"
KZ_TONE_DIR = ROOT / "models" / "tone_pretrained" / "kz_kazakh_sentiment_bert"

BASE_MODEL = "FacebookAI/xlm-roberta-base"
MAX_LENGTH = 256

LID_ID2LABEL = {0: "ru", 1: "kz", 2: "mixed"}
TONE_MIXED_ID2LABEL = {0: "negative", 1: "positive"}


def _resolve_weight(candidates: list[Path]) -> Path:
    for path in candidates:
        if path.is_file():
            return path
    return candidates[0]


LID_WEIGHTS = _resolve_weight(
    [
        XLM_DIR / "xlm-r_v2.pt",
        XLM_DIR / "lid" / "xlm-r_v2.pt",
    ]
)
TONE_MIXED_WEIGHTS = _resolve_weight(
    [
        XLM_DIR / "tone_v1.pt",
        XLM_DIR / "tone" / "tone_v1.pt",
        XLM_DIR / "tone" / "xlm-r_v1.pt",
        XLM_DIR / "tone" / "xlm-r_v2.pt",
    ]
)
