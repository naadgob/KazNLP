> **Russian version:** [Action_Plan_RU.md](Action_Plan_RU.md)

# Action Plan — Capstone AI Project

**Project title:** KazNLP — detecting shala-Kazakh (ru+kz code-switching) in Kazakhstan social media

**Author:** Bogdan Savelyev

**Track:** Deep Learning / NLP (transfer learning, transformers)

**Date:** 1 June 2026

---

## Kickoff plan (from assignment)

| Field | Answer |
|------|--------|
| **Problem** | Telegram comments and Kaspi.kz reviews often contain **shala-Kazakh**: separate Russian and Kazakh phrases/sentences in one message. Automatic LID models (FastText, heuristics) produce many false “mixed” hits. We need a **high-precision filter** for ru / kz / mixed so we can analyze real code-switching (including tone). |
| **Who uses the result** | NLP and sociolinguistics researchers (low-resource + code-switching); marketplace and media analysts who care about **Kazakh and mixed** reviews; developers who need an open dataset and labeling tool. |
| **Data sources** | 1) **Own corpus:** KZ Telegram channels/chats (~422k rows, `data/raw/telegram_code-switch_dataset.csv`), Kaspi reviews (~39k, `data/processed/kaspi_reviews.csv`), combined pool ~269k (`data/processed/kaspi-telegram_dataset.csv`). 2) **Gold LID (manual):** `data/processed/gold_v1.csv` — **3076** examples (mixed 1077, ru 1000, kz 999), sources: Kaspi, Telegram, Lingua candidates; labeled via `labeling_service/`. 3) **LID synthetic (train only):** `data/processed/synthetic/synthetic_all.csv` — 538 rows (`scripts/merge_synthetic.py`; folder appears after run) |
| **Model input** | Comment/review text after normalization (`text_norm`): lowercasing, URL/@mention removal, collapsed repeated punctuation. |
| **Model output** | Class **ru** \| **kz** \| **mixed** + confidence; for **mixed** — binary tone pos/neg (Mixed Tone v1, 97.33% on test n=525, 2GIS). RU/KZ — pretrained routing. |
| **Baseline (simplest solution)** | 1) **FastText** supervised LID (`models/fasttext/fasttext_v1.bin`, `models/fasttext/fasttext_v2.bin`) on synthetic + seeds. 2) **Heuristic** “Kazakh letters + Cyrillic” (`data/processed/mixed_heuristic_seed.csv`). 3) **Lingua** language detector on a subset. Compare precision/recall/F1 on **gold_v1** (hold-out test). |
| **Metrics** | Multiclass: **macro-F1**, **per-class precision/recall**, **confusion matrix**. For mixed filter — **precision on mixed class** (target ≥0.85 on manual audit of 100 random corpus predictions). Accuracy is secondary (classes balanced in gold). |
| **Success criteria** | Working **proof of concept**: (1) open gold LID dataset ≥3k examples; (2) fine-tuned **XLM-R-base** 3-class beating FastText on test; (3) corpus scoring script → `mixed_candidates.csv`; (4) demo (Gradio / labeler); (5) honest error analysis and limits in Final Report. |

---

## Project goal

Build a reproducible NLP pipeline to **reliably separate real ru+kz code-switching** from monolingual Russian/Kazakh with loanwords in Kazakhstan social media, and publish open artifacts for downstream tone analysis.

---

## Method

**CRISP-DM:** problem definition → data/EDA → baseline → main model → evaluation → documentation.

**Main solution:** transfer learning — **XLM-RoBERTa-base** (`xlm-roberta-base`), 3 classes, fine-tune on `gold_v1` (+ synthetic in train only). Training: PyTorch + Hugging Face Trainer, 2× T4 (DDP), batch 8/GPU, 3–4 epochs, stratified split 80/10/10.

**Why XLM-R, not just FastText:** multilingual context, robustness on short social text and mixed phrase boundaries; FastText stays an honest baseline.

**Tools:** Python, pandas, Hugging Face, FastText, custom **labeling_service** (manual labeling + Ollama draft).

---

## Data — details

| Set | Size | Role |
|-----|------|------|
| gold_v1 | 3076 | Sole **gold** for LID train/eval |
| synthetic_all | 538 | Train supplement (hard patterns), not in val/test |
| telegram raw | ~422k | Corpus for scoring after training |
| kaspi reviews | ~39k | Gold source + corpus |
| lingua_candidates | ~6.5k | Labeling queue candidates, **not gold** |

**Label rules:**
- `mixed` — one comment contains **both a Russian and a Kazakh phrase/sentence**.
- `kz` — Kazakh grammar; Russian **loanwords** (качество, чехол) ≠ mixed.
- `ru` — monolingual Russian.

**Preprocessing:** `normalize_text()` → column `text_norm` (see `data/processed/gold_v1.csv`).

---

## Work plan by stage (4 weeks)

| Stage | When | Content | Status |
|-------|------|---------|--------|
| **1. Problem definition** | week 1 | Topic, track, Action Plan, corpus collection | ✅ |
| **2. Data and baseline** | weeks 1–2 | Gold EDA, guidelines, FastText/Lingua baseline | ✅ partial (EDA + gold done; baseline on gold in notebook) |
| **3. Solution** | weeks 2–3 | Fine-tune XLM-R LID v2 + Mixed Tone v1, labeler, demo | ✅ |
| **4. Evaluation** | week 3 | LID/tone metrics, CM, errors; audit 100 — deferred | ✅ partial |
| **5. Documentation** | week 4 | Final Report.docx, WBS.xlsx, presentation, defense | 🔄 pptx / video |

---

## Risks and mitigation

| Risk | Mitigation |
|------|------------|
| kz vs mixed confusion (loanwords) | Clear guidelines; hard negatives in synthetic; audit borderline cases |
| Synthetic shorter than gold | Train only; spot-check 10%; improve ru synthetic (audit: 50% strict on ru) |
| No local GPU | Kaggle / Colab 2×T4, fixed seed and requirements |
| Not enough time for tone | Mixed Tone v1 implemented; ru/kz — pretrained routing |

---

## Hand-in artifacts

1. `docs/capstone/Action_Plan.md` (this file → **Action Plan.docx**)
2. `docs/capstone/WBS.csv` → **Work Breakdown Structure.xlsx**
3. `main.ipynb` + training/scoring scripts
4. `data/processed/gold_v1.csv` + README with sources
5. `docs/capstone/Final_Report.md` → **Final Report.docx**
6. Presentation: `docs/capstone/presentation.pptx` (outline `PRESENTATION_OUTLINE.md`; live `web/story.html`)
7. Demo: `run_demo.py` (site + API) + `run_labeler.py` + 2–5 min recording

---

## Repo links

```
KazNLP/
├── main.ipynb · run_demo.py · run_labeler.py
├── data/processed/gold_v1.csv · main.csv · tone_*
├── data/training/filter/v1/ · data/training/tone/v1/
├── models/fasttext/ · models/xlm-roberta/ · models/tone_pretrained/
├── inference/ · labeling_service/ · web/ · scripts/
└── docs/capstone/                  # Action_Plan · Final_Report · presentation.pptx
```

- Root: `KazNLP/`
- Gold: `data/processed/gold_v1.csv`
- Labeler: `labeling_service/`, `run_labeler.py`
- LID synthetic merge: `scripts/merge_synthetic.py` → `data/processed/synthetic/synthetic_all.csv` (after run)
- Live presentation: `web/story.html` · SIC pptx: `docs/capstone/presentation.pptx`
