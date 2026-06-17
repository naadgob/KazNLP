"""Heuristic text domain tags for sentiment labeling queues."""

from __future__ import annotations

import re

import pandas as pd

VALID_DOMAINS = frozenset({"review", "logistics", "other"})

REVIEW_RE = re.compile(
    r"магазин|доставк|заказ|товар|ластик|айфон|iphone|чехол|салфетк|kaspi|каспи|"
    r"сатуш|jetk|сапа|ұнады|ұнамады|тапсырыс|рақмет|рахмет|рекоменд|не рекоменд|"
    r"брак|качеств|упаковк|курьер|получил|получила|пришл|келді|жеткіз|"
    r"понравил|ұнады|сатылды|дүкен",
    re.I,
)

LOGISTICS_RE = re.compile(
    r"доставк|курьер|жеткіз|жеткізді|келді|пришл|вовремя|быстро|медлен|"
    r"трекинг|отделени|посылк|забрать|курьер",
    re.I,
)

DOMAIN_LABELS = {
    "review": "Review / product",
    "logistics": "Logistics only",
    "other": "Other / off-topic",
}


def text_domain(text: str) -> str:
    """Classify text into review, logistics, or other."""
    if REVIEW_RE.search(text):
        return "review"
    if LOGISTICS_RE.search(text):
        return "logistics"
    return "other"


def domain_series(texts: pd.Series) -> pd.Series:
    review = texts.str.contains(REVIEW_RE, na=False)
    logistics = texts.str.contains(LOGISTICS_RE, na=False)
    domain = pd.Series("other", index=texts.index, dtype="object")
    domain[logistics] = "logistics"
    domain[review] = "review"
    return domain
