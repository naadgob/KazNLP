"""Evaluate Mixed Tone v1/v2 on data/training/tone/v1/test.csv (reproducible metrics)."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE_MODEL = "FacebookAI/xlm-roberta-base"
MAX_LENGTH = 256
LABEL2ID = {"negative": 0, "positive": 1}
ID2LABEL = {0: "negative", 1: "positive"}

WEIGHTS = {
    "v1": ROOT / "models" / "xlm-roberta" / "tone_v1.pt",
    "v2": ROOT / "models" / "xlm-roberta" / "tone" / "xlm-r_v2.pt",
}
TEST_CSV = ROOT / "data" / "training" / "tone" / "v1" / "test.csv"


class ToneDataset(Dataset):
    def __init__(self, df: pd.DataFrame, tokenizer, max_length: int = MAX_LENGTH):
        self.df = df.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, index: int):
        row = self.df.iloc[index]
        enc = self.tokenizer(
            str(row["text"]),
            truncation=True,
            padding=False,
            max_length=self.max_length,
        )
        item = {k: torch.tensor(v) for k, v in enc.items()}
        item["labels"] = torch.tensor(int(row["label_id"]), dtype=torch.long)
        return item


def collate(batch, tokenizer):
    labels = torch.stack([b.pop("labels") for b in batch])
    texts = [{k: v for k, v in b.items()} for b in batch]
    padded = tokenizer.pad(texts, padding=True, return_tensors="pt")
    padded["labels"] = labels
    return padded


def evaluate(version: str, device: torch.device) -> dict:
    path = WEIGHTS[version]
    if not path.is_file():
        raise FileNotFoundError(path)

    df = pd.read_csv(TEST_CSV)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL,
        num_labels=2,
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )
    state = torch.load(path, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model.to(device).eval()

    loader = DataLoader(
        ToneDataset(df, tokenizer),
        batch_size=32,
        shuffle=False,
        collate_fn=lambda b: collate(b, tokenizer),
    )

    y_true, y_pred = [], []
    with torch.no_grad():
        for batch in tqdm(loader, desc=f"tone {version}"):
            labels = batch.pop("labels").to(device)
            batch = {k: v.to(device) for k, v in batch.items()}
            pred = model(**batch).logits.argmax(dim=1)
            y_true.extend(labels.cpu().tolist())
            y_pred.extend(pred.cpu().tolist())

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    return {
        "version": version,
        "n": len(y_true),
        "acc": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "confusion_matrix": cm.tolist(),
    }


def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    print(f"test: {TEST_CSV} ({len(pd.read_csv(TEST_CSV))} rows)\n")

    rows = []
    for ver in ("v1", "v2"):
        try:
            r = evaluate(ver, device)
        except FileNotFoundError as exc:
            print(f"SKIP {ver}: {exc}")
            continue
        rows.append(r)
        print(f"=== Mixed Tone {ver} ===")
        print(f"accuracy:     {r['acc']:.6f}")
        print(f"macro-F1:     {r['f1_macro']:.6f}")
        print(f"macro-P:      {r['precision_macro']:.6f}")
        print(f"macro-R:      {r['recall_macro']:.6f}")
        print(f"CM [neg,pos] x [neg,pos]:\n{r['confusion_matrix']}\n")

    if rows:
        out = ROOT / "data" / "processed" / "metrics_tone_test.json"
        import json

        out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(f"saved: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
