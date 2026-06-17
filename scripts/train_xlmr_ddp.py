"""XLM-R LID DDP training. Launch: accelerate launch --num_processes=2 scripts/train_xlmr_ddp.py --train-csv ... --val-csv ..."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from accelerate import Accelerator
from accelerate.utils import set_seed
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from torch.nn import CrossEntropyLoss
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding


class LidDataset(Dataset):
    def __init__(self, df, tokenizer, max_length=256):
        super().__init__()
        self.df = df.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        row = self.df.iloc[index]
        enc = self.tokenizer(
            str(row["text"]),
            truncation=True,
            padding=False,
            max_length=self.max_length,
        )
        item = {k: torch.tensor(v) for k, v in enc.items()}
        item["labels"] = torch.tensor(row["label_id"], dtype=torch.long)
        item["weight"] = torch.tensor(row["weight"], dtype=torch.float)
        return item


class WeightedCollator(DataCollatorWithPadding):
    def __init__(self, tokenizer, **kwargs):
        super().__init__(tokenizer=tokenizer, **kwargs)

    def __call__(self, features):
        weights = torch.stack([f.pop("weight") for f in features])
        batch = super().__call__(features)
        batch["weight"] = weights
        return batch


def _epoch_metrics(all_y_true, all_y_pred, total_loss, n_batches, device, accelerator):
    y_true = np.concatenate(all_y_true)
    y_pred = np.concatenate(all_y_pred)

    loss_t = torch.tensor(total_loss / n_batches, device=device, dtype=torch.float32)
    loss_t = accelerator.reduce(loss_t, reduction="mean")

    return (
        loss_t.item(),
        accuracy_score(y_true, y_pred),
        f1_score(y_true, y_pred, average="macro", zero_division=0),
        f1_score(y_true, y_pred, average="weighted", zero_division=0),
        precision_score(y_true, y_pred, average="macro", zero_division=0),
        recall_score(y_true, y_pred, average="macro", zero_division=0),
    )


def train_epoch(model, train_ldr, optim, loss_fn, device, accelerator):
    model.train()
    n_batches = len(train_ldr)
    total_loss = 0.0
    all_y_true, all_y_pred = [], []

    pbar = tqdm(train_ldr, disable=not accelerator.is_local_main_process)

    for batch in pbar:
        weights = batch.pop("weight").to(device)
        y_true = batch.pop("labels").to(device)
        batch = {k: v.to(device) for k, v in batch.items()}

        pred = model(**batch).logits
        loss_per_sample = loss_fn(pred, y_true)
        loss = (loss_per_sample * weights).sum() / weights.sum()

        y_pred = pred.argmax(dim=1)
        total_loss += loss.detach().float()

        all_y_true.append(accelerator.gather(y_true).detach().cpu().numpy())
        all_y_pred.append(accelerator.gather(y_pred).detach().cpu().numpy())

        optim.zero_grad(set_to_none=True)
        accelerator.backward(loss)
        optim.step()

    return _epoch_metrics(all_y_true, all_y_pred, total_loss, n_batches, device, accelerator)


def val_epoch(model, val_ldr, loss_fn, device, accelerator):
    model.eval()
    n_batches = len(val_ldr)
    total_loss = 0.0
    all_y_true, all_y_pred = [], []

    pbar = tqdm(val_ldr, disable=not accelerator.is_local_main_process)

    with torch.no_grad():
        for batch in pbar:
            y_true = batch.pop("labels").to(device)
            batch = {k: v.to(device) for k, v in batch.items()}

            pred = model(**batch).logits
            loss = loss_fn(pred, y_true).mean()

            y_pred = pred.argmax(dim=1)
            total_loss += loss.detach().float()

            all_y_true.append(accelerator.gather(y_true).detach().cpu().numpy())
            all_y_pred.append(accelerator.gather(y_pred).detach().cpu().numpy())

    return _epoch_metrics(all_y_true, all_y_pred, total_loss, n_batches, device, accelerator)


def run(args):
    id2label = {0: "ru", 1: "kz", 2: "mixed"}
    label2id = {"ru": 0, "kz": 1, "mixed": 2}

    set_seed(args.seed)
    accelerator = Accelerator()
    device = accelerator.device
    save_dir = Path(args.save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    if accelerator.is_main_process:
        print(f"Accelerate: processes={accelerator.num_processes}, device={device}")

    train_df = pd.read_csv(args.train_csv)
    val_df = pd.read_csv(args.val_csv)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=args.num_labels,
        id2label=id2label,
        label2id=label2id,
    )

    collator = WeightedCollator(tokenizer=tokenizer)
    train_ldr = DataLoader(
        LidDataset(train_df, tokenizer, args.max_length),
        batch_size=args.batch_size,
        shuffle=True,
        collate_fn=collator,
    )
    val_ldr = DataLoader(
        LidDataset(val_df, tokenizer, args.max_length),
        batch_size=args.val_batch_size,
        shuffle=False,
        collate_fn=collator,
    )

    optim = AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    loss_fn = CrossEntropyLoss(reduction="none")

    model, optim, train_ldr, val_ldr = accelerator.prepare(model, optim, train_ldr, val_ldr)

    best_val_f1_macro = 0.0

    for epoch in range(args.epochs):
        tr = train_epoch(model, train_ldr, optim, loss_fn, device, accelerator)
        va = val_epoch(model, val_ldr, loss_fn, device, accelerator)
        accelerator.wait_for_everyone()

        if accelerator.is_main_process:
            print(
                f"Epoch {epoch + 1}/{args.epochs} | "
                f"train_loss={tr[0]:.4f} val_loss={va[0]:.4f} "
                f"val_acc={va[1]:.4f} val_f1_macro={va[2]:.4f}"
            )

            if va[2] > best_val_f1_macro:
                best_val_f1_macro = va[2]
                save_path = save_dir / f"{args.run_name}.pt"
                torch.save(accelerator.unwrap_model(model).state_dict(), save_path)
                print(f"saved → {save_path}")

        accelerator.wait_for_everyone()

    if accelerator.is_main_process:
        print(f"best val macro-F1: {best_val_f1_macro:.4f}")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--train-csv", required=True)
    p.add_argument("--val-csv", required=True)
    p.add_argument("--save-dir", required=True)
    p.add_argument("--model-name", default="xlm-roberta-base")
    p.add_argument("--num-labels", type=int, default=3)
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--batch-size", type=int, default=8)
    p.add_argument("--val-batch-size", type=int, default=16)
    p.add_argument("--epochs", type=int, default=4)
    p.add_argument("--lr", type=float, default=2e-5)
    p.add_argument("--weight-decay", type=float, default=0.01)
    p.add_argument("--run-name", default="xlm-r_v1")
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


if __name__ == "__main__":
    run(parse_args())
