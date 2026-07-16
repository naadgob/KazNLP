> **Russian version:** [README_RU.md](README_RU.md)

# KazNLP

**Capstone:** Samsung Innovation Campus · Deep Learning / NLP  
**Author:** Bogdan Savelyev  
**Task:** polarity (pos/neg) on **mixed** 2GIS reviews that switch between Russian and Kazakh in one text. You can't build that sample honestly without a reliable **ru / kz / mixed** filter: auto-LID on Telegram tags almost everything as mixed, while most of those lines are Kazakh with a Russian loanword.

Full narrative and numbers for reviewers: [`STORY.md`](STORY.md) · web version [`web/story.html`](web/story.html) (build: `python scripts/build_story_landing.py`).

> **Name note:** Nazarbayev University already ships an open toolkit also called KazNLP. This repo is a separate student/capstone project. For papers and outreach, prefer a distinct short name (e.g. ShalaLID / kk-ru SwitchFilter) so the two are not confused.

---

## Key numbers (defense canon)

Sources: `main.ipynb` (cells 45, 173, 237, 255, 268), `docs/capstone/Final_Report.md`, `data/processed/metrics_tone_test.json`.

| What | Value | File / cell |
|------|-------|-------------|
| Telegram (LID context) | 422,141 | `data/raw/telegram_code-switch_dataset.csv` |
| Kaspi | 39,129 | `data/processed/kaspi_reviews.csv` |
| Gold LID (ru/kz/mixed) | 3,076 (1000 / 999 / 1077) | `data/processed/gold_v1.csv` · cell 144 |
| LID test | n = 461 | `data/training/filter/v1/test.csv` |
| **XLM-R LID v2** | macro-F1 **96.56%** | `models/xlm-roberta/xlm-r_v2.pt` · cells 173, 268 |
| `main.csv` | 331,468 rows | cell 237 |
| `main_mixed.csv` | 16,364 (model-predicted, not audited) | cell 237 |
| Gold tone (2GIS mixed) | 3,529 | `data/processed/tone_mixed_balanced_audited.csv` |
| Synthetic tone (train only) | 882 (~20% of train) | `data/processed/tone_synthetic.csv` |
| Tone train | 4,411 | `data/processed/tone_train_mixed.csv` |
| Tone test | n = 525 | `data/training/tone/v1/test.csv` |
| **Mixed Tone v1** | accuracy **97.33%** | `data/processed/metrics_tone_test.json` · `scripts/eval_tone_v1.py` |
| Mixed Tone v2 (not in prod) | 96.19% | same JSON |
| FT-mixed diagnostic | ~1.66% true positive | cells 45–46 |

**Tone 97.33% caveat:** ~94% of tone gold comes from `llm_composer`; the hold-out metric is agreement with LLM drafts, not a blind human eval. Details in Final Report §3.3.3.

**On-disk counts:** if CSVs were rebuilt after cell 237, disk row counts can drift (e.g. `main.csv` >331k). For defense and papers, trust **cell 237** and the table above.

---

## Quick start

### Model weights (~8.2 GB)

Not in git (GitHub size limits). **Hugging Face:**

**https://huggingface.co/datasets/naadgob/kaznlp-weights**

```bash
pip install huggingface_hub
python scripts/download_kaznlp_weights.py   # download models.zip and unpack
python scripts/setup_demo_models.py         # symlink RU/KZ + path checks
```

Locally: unpack `models/models.zip` into the repo root (next to `README.md`).

### Demo (site + inference API)

```bash
pip install -r inference/requirements.txt
python run_demo.py
```

Windows: `start_demo.bat`. Open http://127.0.0.1:8000/ (`web/index.html` + `POST /analyze`).

The first request may return **503** for 30–60 s while four models (~8.5 GB) load. Download weights first (above) or drop `models.zip` in place by hand.

### Labeler (gold LID and tone)

```bash
pip install -r requirements-labeler.txt
ollama pull qwen2.5:3b    # for LLM-batch language drafts
python run_labeler.py
```

Default port 8000 (next free port if busy). See [`labeling_service/README.md`](labeling_service/README.md).

### Tone metrics (no notebook)

```bash
python scripts/eval_tone_v1.py
```

---

## Repo layout

```
KazNLP/
├── main.ipynb                      # main pipeline (270 cells)
├── README.md · README_RU.md · STORY.md · STORY_RU.md
├── run_demo.py · run_labeler.py · start_demo.bat
├── collect_2gis_reviews.py         # 2GIS scraper (CLI)
├── essential_ru_kaz.py · popular_ru_kaz.py
├── requirements.txt · requirements-labeler.txt
├── .env.example                    # secrets template (do not commit .env)
│
├── data/
│   ├── raw/                        # telegram_code-switch_dataset.csv, 2gis_*.csv
│   ├── processed/                  # gold_v1, main.csv, tone_*, metrics_tone_test.json
│   │   └── synthetic_tone/         # tone synthetic batches (after generate_tone_synthetic.py)
│   ├── manual labeling/            # history of manual LID labeling
│   │   └── language/               # kaspi-telegram_part, lingua_candidates_*, mixed-heuristic-seed
│   └── training/
│       ├── filter/v1/              # LID train · val · test (gold)
│       └── tone/v1/                # tone splits
│
├── models/
│   ├── fasttext/                   # fasttext_v1.bin · fasttext_v2.bin
│   ├── xlm-roberta/                # xlm-r_v2.pt · tone_v1.pt · lid/ · tone/
│   └── tone_pretrained/            # ru_rubert_rureviews · kz_kazakh_sentiment_bert
│
├── training/                       # fasttext_synthetic.txt · train_v2.txt · test_v2.txt · …
├── inference/                      # FastAPI: app.py · pipeline.py · config.py · test_api.py
├── labeling_service/               # labeler UI + LLM batch (see README inside)
│   ├── main.py · manual_labeling.py · text_heuristics.py
│   ├── templates/index.html
│   └── static/                     # app.js · manual.js · style.css
│
├── web/
│   ├── index.html                  # landing + live demo
│   ├── story.html                  # jury narrative (build_story_landing.py)
│   ├── assets/
│   │   ├── labeler/                # 01–03 PNG for story carousel
│   │   └── _verify-sources.png
│   └── README.md
│
├── scripts/                        # eval · export · deck · synthetic (see table)
│   └── archive/                    # old LID synthetic/EDA (not defense path)
│
├── docs/
│   ├── README.md
│   ├── tone_dataset_overview.md
│   ├── outreach/                   # professor outreach drafts
│   └── capstone/                   # SIC paperwork (below)
│
└── sessions/                       # Telethon *.session (gitignored)
```

### `docs/capstone/` (Samsung hand-in)

| File | Role |
|------|------|
| `Action_Plan.md` / `.docx` | kickoff plan |
| `Final_Report.md` / `.docx` | final report |
| `WBS.csv` | WBS (`.xlsx` via `export_capstone_docs.py`) |
| `presentation.pptx` | **only** SIC presentation |
| `kaznlp-story-deck-self.html` | HTML source for pptx (`build_self_deck.py`; may be missing until rebuild) |
| `PRESENTATION_OUTLINE.md` | 20-slide outline |
| `CAPSTONE_AUDIT.md` | pre-defense checklist |

Live defense narrative: [`web/story.html`](web/story.html) (does not replace `presentation.pptx` in paperwork).

---

## Pipelines

### 1. Language ID (`main.ipynb`, chapters 1–6)

| Stage | Artifact |
|-------|----------|
| Synthetic 480k | `training/fasttext_synthetic.txt` |
| FastText v1/v2 | `models/fasttext/fasttext_v1.bin`, `models/fasttext/fasttext_v2.bin` |
| Telegram collect | `data/raw/telegram_code-switch_dataset.csv` |
| Kaspi collect | `data/processed/kaspi_reviews.csv` |
| Hand gold | `data/processed/gold_v1.csv` |
| XLM-R LID v2 | `models/xlm-roberta/xlm-r_v2.pt` |
| Master corpus | `data/processed/main.csv`, `main_mixed.csv` |

Baseline ladder on one shared test (n=461): §10 (cells 267–268).

### 2. Mixed tone (`main.ipynb`, chapter 8)

| File | Rows | Role |
|------|-----:|------|
| `tone_mixed_balanced_audited.csv` | 3,529 | `data/processed/` — gold pos/neg, 2GIS mixed |
| `tone_synthetic.csv` | 882 | `data/processed/` — synthetic in train only |
| `tone_train_mixed.csv` | 4,411 | `data/processed/` — merged train |
| `data/training/tone/v1/test.csv` | 525 | Gold-only hold-out |

Regenerate synthetic:

```bash
python scripts/generate_tone_synthetic.py
python scripts/merge_tone_synthetic.py
```

Gold tone path: 2GIS → LID v2 → `language == mixed` → `run_labeler.py` (manual mode + `llm_composer` draft) → balance pos/neg.

### 3. Inference cascade

```
TEXT → XLM-R LID v2 → ru | kz | mixed
  ru    → RuReviews RuBERT (pretrained)
  kz    → Kazakh Sentiment BERT (pretrained)
  mixed → Mixed Tone v1 (fine-tuned XLM-R)
```

```bash
python scripts/download_tone_pretrained.py
python scripts/verify_tone_pretrained.py
```

See [`models/tone_pretrained/README.md`](models/tone_pretrained/README.md).

---

## Main scripts

| Script | Role |
|--------|------|
| `setup_demo_models.py` | HF download + RU/KZ symlinks + path checks |
| `download_kaznlp_weights.py` | Pull `models.zip` from Hugging Face |
| `upload_kaznlp_weights.py` | Push weights to HF (author, write token) |
| `eval_tone_v1.py` | Tone v1/v2 metrics → `metrics_tone_test.json` |
| `generate_tone_synthetic.py` | 8 synthetic tone batches (882) |
| `merge_tone_synthetic.py` | Build `tone_train_mixed.csv` |
| `download_tone_pretrained.py` | RU/KZ Hugging Face weights |
| `verify_tone_pretrained.py` | Smoke-test pretrained |
| `build_self_deck.py` | `kaznlp-story-deck-self.html` → `presentation.pptx` |
| `html_deck_to_pptx.py` | HTML deck → PowerPoint (screenshot export) |
| `export_capstone_docs.py` | md → docx/xlsx for hand-in |
| `build_story_landing.py` | `web/story.html` (live jury narrative) |
| `train_xlmr_ddp.py` | DDP XLM-R training (extracted from notebook) |
| `merge_synthetic.py` | LID synthetic → `data/processed/synthetic/synthetic_all.csv` (folder appears after run) |
| `insert_tone_eval_notebook.py` | One-shot helper to insert tone-eval cells |

Historical batch scripts: `scripts/archive/` (not needed for the defense path).

**Defense path (minimum):** cells **45, 173, 237, 268** + `eval_tone_v1.py` + `run_demo.py`.

---

## Documentation

| File | Content |
|------|---------|
| [`STORY.md`](STORY.md) | Full narrative, source table |
| [`web/story.html`](web/story.html) | Same story in the browser |
| [`docs/README.md`](docs/README.md) | Docs index |
| [`docs/capstone/Final_Report.md`](docs/capstone/Final_Report.md) | Final report |
| [`docs/tone_dataset_overview.md`](docs/tone_dataset_overview.md) | Gold tone, synthetic, QC |
| [`docs/capstone/PRESENTATION_OUTLINE.md`](docs/capstone/PRESENTATION_OUTLINE.md) | Presentation structure |
| [`docs/capstone/CAPSTONE_AUDIT.md`](docs/capstone/CAPSTONE_AUDIT.md) | SIC checklist |
| [`docs/capstone/presentation.pptx`](docs/capstone/presentation.pptx) | SIC deck (only pptx) |
| [`docs/outreach/professor-outreach.md`](docs/outreach/professor-outreach.md) | Outreach list + draft emails |
| [`labeling_service/README.md`](labeling_service/README.md) | Labeler setup |
| [`web/README.md`](web/README.md) | Demo site |

SIC presentation: [`docs/capstone/presentation.pptx`](docs/capstone/presentation.pptx) · live: [`web/story.html`](web/story.html) · rebuild HTML: `python scripts/build_self_deck.py`

---

## Caveats

- The `language` column in raw Telegram is the **collector** label (FastText), not ground truth. Under the `is_real_mixed()` heuristic only ~**1.66%** of FT-mixed lines are real code-switches.
- The **16,364** mixed rows in `main.csv` are LID v2 predictions, not a full human audit of the corpus.
- `main.ipynb` does **not** replay via Run All; do not re-run Telethon cells **31, 35, 41, 88**.
- Do not commit: `.env`, `sessions/`, `labeling_service/uploads/`.

---

## Secrets (`.env.example`)

| Variable | Why |
|----------|-----|
| `HF_TOKEN` | Hugging Face datasets / models; **write** only for `upload_kaznlp_weights.py` |
| `TELEGRAM_API_ID`, `TELEGRAM_API_HASH` | Telethon |
| `GEMINI_API_KEY` | Optional for labeler (`LABELER_PROVIDER=gemini`) |
| `YOUTUBE_API_KEY` | YouTube collect (partial in notebook) |
| `OLLAMA_*` | Labeler LLM-batch (default) |
