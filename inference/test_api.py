"""API smoke tests. Skips inference tests when XLM-R weights are missing."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from inference.app import app
from inference.config import LID_WEIGHTS, TONE_MIXED_WEIGHTS
from inference.pipeline import InferencePipeline


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    body = res.json()
    assert "status" in body
    assert "device" in body
    assert "models_loaded" in body


def test_analyze_empty_text_422(client):
    res = client.post("/analyze", json={"text": ""})
    assert res.status_code == 422


@pytest.mark.skipif(
    not LID_WEIGHTS.is_file() or not TONE_MIXED_WEIGHTS.is_file(),
    reason="XLM-R weights not present",
)
def test_analyze_end_to_end(client):
    res = client.post(
        "/analyze",
        json={
            "text": "Доставка кеш жүрді, но заказ пришёл холодный, очень разочарован.",
            "tone_model": "auto",
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["lid"] in ("ru", "kz", "mixed")
    assert body["tone"] in ("positive", "negative")
    assert "probs" in body


@pytest.mark.skipif(
    not LID_WEIGHTS.is_file() or not TONE_MIXED_WEIGHTS.is_file(),
    reason="XLM-R weights not present",
)
def test_manual_routing_override():
    pipe = InferencePipeline()
    pipe.load_all()
    if not pipe.status.ready:
        pytest.skip("models failed to load")
    result = pipe.analyze("Очередь 40 минут, персонал грубый.", tone_model="mixed")
    assert result["route"] == "mixed"
    if result["lid"] != "mixed":
        assert result["routing"] == "manual"
