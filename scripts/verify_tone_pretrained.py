"""Smoke-test RU/KZ pretrained tone models in models/tone_pretrained/."""

from __future__ import annotations

from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "models" / "tone_pretrained"

SAMPLES = {
    "ru_rubert_rureviews": (
        "Отличное обслуживание, всем советую!",
        "Ужасный сервис, больше не приду.",
    ),
    "kz_kazakh_sentiment_bert": (
        "Өте жақсы орын, қызмет керемет.",
        "Қызмет нашар, ұнамады.",
    ),
}


def predict(folder: str, text: str) -> tuple[str, float]:
    path = BASE / folder
    if not path.is_dir():
        raise FileNotFoundError(path)
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForSequenceClassification.from_pretrained(path)
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]
        idx = int(probs.argmax())
    id2label = model.config.id2label
    label = id2label[idx] if id2label else str(idx)
    return str(label), float(probs[idx])


def main() -> None:
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    for folder, (pos_text, neg_text) in SAMPLES.items():
        print(f"\n{folder}")
        for text in (pos_text, neg_text):
            label, conf = predict(folder, text)
            snippet = text[:50].replace("\n", " ")
            print(f"  {label} ({conf:.2f}) | {snippet}...")


if __name__ == "__main__":
    main()
