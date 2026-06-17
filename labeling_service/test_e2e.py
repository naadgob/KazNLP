"""Quick end-to-end test for language labeler API."""

import json
import sys
from pathlib import Path

import httpx
import pandas as pd

BASE = "http://127.0.0.1:8000"
SAMPLE = Path(__file__).parent / "test_sample_100.csv"
SMALL = Path(__file__).parent / "test_sample_5.csv"


def make_small():
    df = pd.read_csv(SAMPLE, nrows=5)
    df.to_csv(SMALL, index=False, encoding="utf-8-sig")


def upload(path: Path) -> str:
    with path.open("rb") as f:
        r = httpx.post(f"{BASE}/api/upload", files={"file": (path.name, f, "text/csv")}, timeout=60)
    r.raise_for_status()
    data = r.json()
    print("upload:", data["job_id"], data["total_rows"], "rows")
    return data["job_id"]


def label(job_id: str, only_empty: bool = False, resume: bool = False) -> None:
    params = f"only_empty={'true' if only_empty else 'false'}&resume={'true' if resume else 'false'}"
    url = f"{BASE}/api/jobs/{job_id}/label?{params}"
    events = {"batch_start": 0, "llm_chunk": 0, "done": 0, "label_error": 0}
    with httpx.stream("GET", url, timeout=600) as resp:
        resp.raise_for_status()
        event = None
        for line in resp.iter_lines():
            if line.startswith("event:"):
                event = line.split(":", 1)[1].strip()
            elif line.startswith("data:") and event:
                events[event] = events.get(event, 0) + 1
                if event in ("done", "label_error"):
                    print(event, line.split(":", 1)[1].strip()[:200])
                event = None
    print("events:", events)


def validate(job_id: str, nrows: int) -> None:
    out = httpx.get(f"{BASE}/api/jobs/{job_id}/download", timeout=60)
    out.raise_for_status()
    path = Path(__file__).parent / "uploads" / job_id / "output.csv"
    df = pd.read_csv(path)
    assert len(df) == nrows
    langs = set(str(x).strip().lower() for x in df["language"].dropna())
    assert langs <= {"ru", "kz", "mixed"}, langs
    orig = pd.read_csv(SAMPLE if nrows == 100 else SMALL)
    if "label" in orig.columns:
        assert (df["label"].fillna("") == orig["label"].fillna("")).all()
    print("OK:", len(df), "rows, languages:", langs, "counts:", df["language"].value_counts().to_dict())


if __name__ == "__main__":
    make_small()
    print("=== 5-row smoke test ===")
    jid = upload(SMALL)
    label(jid)
    validate(jid, 5)
    if "--full" in sys.argv:
        print("\n=== 100-row test ===")
        jid2 = upload(SAMPLE)
        label(jid2)
        validate(jid2, 100)
