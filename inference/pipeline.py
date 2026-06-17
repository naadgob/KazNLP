from __future__ import annotations

from dataclasses import dataclass, field

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from inference.config import (
    BASE_MODEL,
    KZ_TONE_DIR,
    LID_ID2LABEL,
    LID_WEIGHTS,
    MAX_LENGTH,
    RU_TONE_DIR,
    TONE_MIXED_ID2LABEL,
    TONE_MIXED_WEIGHTS,
)


@dataclass
class PipelineStatus:
    device: str = "cpu"
    models_loaded: list[str] = field(default_factory=list)
    errors: dict[str, str] = field(default_factory=dict)
    loading: bool = False

    @property
    def ready(self) -> bool:
        return (
            not self.loading
            and not self.errors
            and len(self.models_loaded) == 4
        )


class InferencePipeline:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.status = PipelineStatus(device=str(self.device))
        self._lid_tokenizer = None
        self._lid_model = None
        self._tone_mixed_tokenizer = None
        self._tone_mixed_model = None
        self._ru_tokenizer = None
        self._ru_model = None
        self._kz_tokenizer = None
        self._kz_model = None

    def load_all(self) -> PipelineStatus:
        self.status = PipelineStatus(device=str(self.device), loading=True)
        loaders = (
            ("lid_v2", self._load_lid),
            ("tone_v1", self._load_tone_mixed),
            ("ru_tone", self._load_ru_tone),
            ("kz_tone", self._load_kz_tone),
        )
        for name, loader in loaders:
            try:
                loader()
                self.status.models_loaded.append(name)
            except Exception as exc:  # noqa: BLE001 — surface per-model load errors in /health
                self.status.errors[name] = str(exc)
        self.status.loading = False
        return self.status

    def _load_lid(self) -> None:
        if not LID_WEIGHTS.is_file():
            raise FileNotFoundError(
                f"Положите веса LID в {LID_WEIGHTS}"
            )
        self._lid_tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        self._lid_model = AutoModelForSequenceClassification.from_pretrained(
            BASE_MODEL,
            num_labels=3,
            id2label=LID_ID2LABEL,
            label2id={v: k for k, v in LID_ID2LABEL.items()},
        )
        state = torch.load(LID_WEIGHTS, map_location=self.device, weights_only=True)
        self._lid_model.load_state_dict(state)
        self._lid_model.to(self.device).eval()

    def _load_tone_mixed(self) -> None:
        if not TONE_MIXED_WEIGHTS.is_file():
            raise FileNotFoundError(
                f"Положите веса mixed tone в {TONE_MIXED_WEIGHTS}"
            )
        self._tone_mixed_tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        self._tone_mixed_model = AutoModelForSequenceClassification.from_pretrained(
            BASE_MODEL,
            num_labels=2,
            id2label=TONE_MIXED_ID2LABEL,
            label2id={v: k for k, v in TONE_MIXED_ID2LABEL.items()},
        )
        state = torch.load(TONE_MIXED_WEIGHTS, map_location=self.device, weights_only=True)
        self._tone_mixed_model.load_state_dict(state)
        self._tone_mixed_model.to(self.device).eval()

    def _load_ru_tone(self) -> None:
        if not RU_TONE_DIR.is_dir():
            raise FileNotFoundError(f"RU tone model not found: {RU_TONE_DIR}")
        self._ru_tokenizer = AutoTokenizer.from_pretrained(RU_TONE_DIR)
        self._ru_model = AutoModelForSequenceClassification.from_pretrained(RU_TONE_DIR)
        self._ru_model.to(self.device).eval()

    def _load_kz_tone(self) -> None:
        if not KZ_TONE_DIR.is_dir():
            raise FileNotFoundError(f"KZ tone model not found: {KZ_TONE_DIR}")
        self._kz_tokenizer = AutoTokenizer.from_pretrained(KZ_TONE_DIR)
        self._kz_model = AutoModelForSequenceClassification.from_pretrained(KZ_TONE_DIR)
        self._kz_model.to(self.device).eval()

    def _encode(self, tokenizer, text: str) -> dict[str, torch.Tensor]:
        enc = tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )
        return {k: v.to(self.device) for k, v in enc.items()}

    @torch.no_grad()
    def predict_lid(self, text: str) -> tuple[str, float, dict[str, float]]:
        if self._lid_model is None or self._lid_tokenizer is None:
            raise RuntimeError("LID model not loaded")
        batch = self._encode(self._lid_tokenizer, text)
        logits = self._lid_model(**batch).logits
        probs_t = torch.softmax(logits, dim=-1)[0]
        idx = int(probs_t.argmax())
        lid = LID_ID2LABEL[idx]
        probs = {LID_ID2LABEL[i]: float(probs_t[i]) for i in range(3)}
        return lid, float(probs_t[idx]), probs

    @torch.no_grad()
    def predict_tone_mixed(self, text: str) -> tuple[str, float]:
        if self._tone_mixed_model is None or self._tone_mixed_tokenizer is None:
            raise RuntimeError("Mixed tone model not loaded")
        batch = self._encode(self._tone_mixed_tokenizer, text)
        logits = self._tone_mixed_model(**batch).logits
        probs_t = torch.softmax(logits, dim=-1)[0]
        idx = int(probs_t.argmax())
        tone = TONE_MIXED_ID2LABEL[idx]
        return tone, float(probs_t[idx])

    @torch.no_grad()
    def predict_tone_ru(self, text: str) -> str:
        if self._ru_model is None or self._ru_tokenizer is None:
            raise RuntimeError("RU tone model not loaded")
        batch = self._encode(self._ru_tokenizer, text)
        logits = self._ru_model(**batch).logits
        probs_t = torch.softmax(logits, dim=-1)[0]
        id2label = self._ru_model.config.id2label
        neg_idx = next(i for i, lbl in id2label.items() if lbl == "LABEL_1")
        pos_idx = next(i for i, lbl in id2label.items() if lbl == "LABEL_2")
        neg_p = float(probs_t[int(neg_idx)])
        pos_p = float(probs_t[int(pos_idx)])
        return "positive" if pos_p >= neg_p else "negative"

    @torch.no_grad()
    def predict_tone_kz(self, text: str) -> str:
        if self._kz_model is None or self._kz_tokenizer is None:
            raise RuntimeError("KZ tone model not loaded")
        batch = self._encode(self._kz_tokenizer, text)
        logits = self._kz_model(**batch).logits
        probs_t = torch.softmax(logits, dim=-1)[0]
        id2label = self._kz_model.config.id2label
        neg_idx = next(i for i, lbl in id2label.items() if str(lbl).lower() == "negative")
        pos_idx = next(i for i, lbl in id2label.items() if str(lbl).lower() == "positive")
        neg_p = float(probs_t[int(neg_idx)])
        pos_p = float(probs_t[int(pos_idx)])
        return "positive" if pos_p >= neg_p else "negative"

    def analyze(self, text: str, tone_model: str = "auto") -> dict:
        lid, lid_conf, probs = self.predict_lid(text)
        route = lid if tone_model == "auto" else tone_model
        routing = "auto" if tone_model == "auto" else ("manual" if tone_model != lid else "auto")

        tone_conf: float | None = None
        if route == "mixed":
            tone, tone_conf = self.predict_tone_mixed(text)
            model_used = "mixed_tone_v1"
        elif route == "ru":
            tone = self.predict_tone_ru(text)
            model_used = "ru_rubert_rureviews"
        elif route == "kz":
            tone = self.predict_tone_kz(text)
            model_used = "kz_kazakh_sentiment_bert"
        else:
            raise ValueError(f"Unknown route: {route}")

        return {
            "lid": lid,
            "lid_conf": lid_conf,
            "probs": probs,
            "tone": tone,
            "tone_conf": tone_conf,
            "route": route,
            "model_used": model_used,
            "routing": routing,
        }
