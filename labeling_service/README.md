> **Russian version:** [README_RU.md](README_RU.md)

# KazNLP Labeler

Local web service for labeling **language** (`ru` | `kz` | `mixed`) and **tone** (`positive` | `negative` | `skip`) on CSV files.

```
labeling_service/
├── main.py                 # FastAPI entry
├── manual_labeling.py      # manual mode
├── llm_provider.py         # Ollama / Gemini
├── text_heuristics.py      # QC for tone merge / weak bilingual
├── templates/index.html
├── static/                 # app.js · manual.js · style.css
├── uploads/                # job cache (gitignored, ~1 GB)
└── README.md
```

Run from repo root: `python run_labeler.py` (not from this folder).

- **Language:** manual mode + optional LLM batch (Ollama).
- **Sentiment:** manual gold only; LLM batch does not label tone.
- For capstone, the labeler produced **3,076** gold LID rows and most of the **3,529** tone gold rows (`llm_composer` + manual fixes).

**Default provider:** [Ollama](https://ollama.com) (local, no API limits). Optional: Google Gemini (`LABELER_PROVIDER=gemini`).

## Setup

1. Ollama and a model (8 GB RAM, CPU):

```bash
ollama pull qwen2.5:3b
```

2. `.env` in project root (see `.env.example`):

```
LABELER_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_NUM_CTX=8192
```

3. Dependencies:

```bash
pip install -r requirements-labeler.txt
```

### Ollama models (8 GB RAM)

| Model | RAM | ru/kz/mixed |
|-------|-----|-------------|
| **qwen2.5:3b** | ~2.5 GB | recommended |
| qwen2.5-coder:1.5b | ~1 GB | faster, weaker on mixed |
| llama3.2:3b | ~2 GB | alternative |
| 7B+ | 5+ GB | not recommended on 8 GB |

### LLM quality modes (`LABELER_QUALITY`)

| Mode | Batch | Few-shot | Verify mixed |
|------|-------|----------|--------------|
| `fast` | 50 | no | no |
| `balanced` | 25 | yes | no |
| `high` | 10 | yes | yes |
| `max` | 3 | yes | yes |

`OLLAMA_BATCH_SIZE` overrides batch size. On 8 GB: use `high` or `max` + `precision_filter.py` after batch.

## Run

From **project root**:

```bash
python run_labeler.py
```

http://localhost:8000 (or next free port if 8000 is taken by demo).

UI tabs: **Manual review** · **LLM batch** · **Upload**.

## CSV format

Required columns: `text`, `language`, `label`

| Mode | Writes |
|------|--------|
| LLM batch | `language` only (ru/kz/mixed), draft |
| Manual Language | gold `language` |
| Manual Sentiment | `label` (positive/negative/skip), `tone_source=manual` |

Optional: `confidence`, `needs_review`, `label_source`.

Export: manual gold / tone_labeled / full dataset (dropdown in LLM batch).

## Manual review: translation

Checkbox **“Auto-translate RU”**, hotkey **`T`**.

- [MyMemory](https://mymemory.translated.net/) `kk|ru`, not an LLM.
- `MYMEMORY_EMAIL` in `.env` → ~10,000 words/day limit.
- Hint for the annotator; gold label is on the original text.

## Features

- Ollama or Gemini (`LABELER_PROVIDER`)
- SSE: live batch progress
- Resume after each batch
- “Only empty language” for LLM batch
- Session metrics and class balance in sidebar

## Warning

LLM language labels are **drafts**. Gold LID and tone for capstone were checked manually. Do not use LLM batch as the sole gold source without audit.
