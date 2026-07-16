> **Russian version:** [README_RU.md](README_RU.md)

# KazNLP web

```
web/
├── index.html              # landing + live demo (via run_demo.py)
├── story.html              # capstone narrative (build_story_landing.py)
├── README.md
└── assets/
    ├── labeler/            # 01-manual-language.png … 03-llm-batch.png
    └── _verify-sources.png
```

| File | Role |
|------|------|
| `index.html` | Product landing: research path, metrics, live demo (`POST /analyze`) |
| `story.html` | Capstone story for jury (generated; do not edit by hand) |
| `assets/labeler/*.png` | Labeler screenshots for carousel in `story.html` (on disk: `01`–`03`; refresh after UI changes → `build_story_landing.py`) |

Generate story:

```bash
python scripts/build_story_landing.py
```

Markup source: `scripts/build_story_landing.py` (design and CSS inherit from `index.html`).

---

## Demo (recommended)

From repo root:

```bash
pip install -r inference/requirements.txt
python run_demo.py
```

Windows: `start_demo.bat`.

Open http://127.0.0.1:8000/ — FastAPI serves `index.html` and the API on the same origin.

`setup_demo_models.py` runs automatically when `run_demo.py` starts.

First `/analyze` on CPU: expect **503** for 30–60 s while LID + tone + RU/KZ pretrained load (~8.5 GB).

### API from another host (static preview)

```html
<script>window.KAZNLP_API_BASE = 'http://127.0.0.1:8000';</script>
```

---

## Model weights

| Model | Path |
|-------|------|
| LID v2 | `models/xlm-roberta/xlm-r_v2.pt` or `models/xlm-roberta/lid/xlm-r_v2.pt` |
| Mixed tone v1 | `models/xlm-roberta/tone/tone_v1.pt` or `models/xlm-roberta/tone_v1.pt` |
| RU / KZ tone | `models/tone_pretrained/` — `python scripts/download_tone_pretrained.py` |

---

## Static only (no API)

```bash
python -m http.server 8877 --directory web
```

- http://127.0.0.1:8877/index.html — landing without live inference (demo buttons won't work)
- http://127.0.0.1:8877/story.html — capstone story
