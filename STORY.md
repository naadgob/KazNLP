> **Russian version:** [STORY_RU.md](STORY_RU.md)

# KazNLP — project story

**Author:** Bogdan Savelyev  
**Project:** Samsung Innovation Campus capstone · Deep Learning / NLP  
**Date:** 15.06.2026  
**Artifacts:** `main.ipynb` · `docs/capstone/Final_Report.md` · `docs/capstone/presentation.pptx` · `web/story.html` · `run_demo.py`

*All numbers cross-checked with the report, notebook, and CSV/JSON on disk (15.06.2026). Disputed metrics are flagged explicitly.*

---

## Main idea

Automatic language ID in Kazakhstani social media and reviews tags almost everything as “mixed.” KazNLP measured that noise on **422,141** Telegram comments, built a manual gold set of **3,076** rows, and on a single gold test (**n = 461**) showed that XLM-RoBERTa v2 reaches **96.56%** macro-F1 where FastText stops at **70.92%** and Lingua is not safe for corpus filtering without manual review. Tone, the **331,468**-row corpus, and the demo are built around that result — not the other way around.

---

# I. The problem in the real world

## Where it shows up

In Telegram channels, on Kaspi, and in 2GIS, people write the way they speak: a Russian phrase, then Kazakh, sometimes the reverse. Shala-Kazakh is normal for millions of users, not a keyboard glitch. For a system that needs language and tone, that is a separate class of tasks.

The project corpus comes from real sources: **422,141** Telegram comments, **39,129** Kaspi reviews, tens of thousands of 2GIS reviews. This is not a textbook dataset — it is KZ digital as it is.

## Symptom, cause, root

**Symptom.** A report on “the share of mixed in social media” paints mass bilingualism. A marketer builds a dashboard. A researcher adds texts to a sentiment corpus. A product team decides from numbers that were already corrupted at collection time.

**Cause.** FastText at scrape time and heuristics like “Kazakh letters + Cyrillic” do not separate code-switch from a Kazakh sentence with a Russian loanword. The report estimates false mixed at up to **~98%** for such rules. In the notebook on a concrete slice: of **27,628** FT-mixed rows, the `is_real_mixed()` heuristic kept **460** (~**1.66%**). After FT v2, mixed precision on the same heuristic is **2.32%** (1,542 of 66,462).

**Root.** Kazakhstani NLP has long conflated two different phenomena: monolingual Kazakh with Russian loans and real language switching in one message. Until that boundary is drawn, mixed statistics, tone filters, and any “bilingual analysis” rest on noise.

### Two examples you cannot explain the project without

| Text | What it is | What naive LID does |
|------|------------|---------------------|
| «Курьер молодец, уақытында әкелді» | **mixed** — two language phrases | Often correct |
| «Качествосы жақсы, арзан» | **kz** — Kazakh grammar, Russian word | Often wrongly **mixed** |

The second line drives false hits at scale. Naive LID sees Cyrillic plus “Kazakh” letters and tags mixed; a loan in Kazakh looks like a switch.

Without honest ru / kz / mixed separation, you cannot answer simple questions: how much real bilingualism is in the corpus, can you train tone on “mixed” texts without kz-with-loans, and if LID lies, analytics lie too.

**Target state:** a three-class filter on real KZ text, then tone only where language is truly mixed.

**Cost of inaction:** **422,141** comments with `language` from FastText at scrape (that is **not** ground truth). Same on **39,129** Kaspi reviews. Models and reports trained on auto-labels learn noise.

## What KazNLP solves

Not “language ID in general,” but a narrow KZ task:

- Precise **ru / kz / mixed** filter with measurable quality on manual gold.
- Honest estimate of code-switching scale: how much mixed is real, not what FastText wrote at scrape.
- Basis for tone on mixed reviews (stretch goal, 2GIS mixed domain).
- Reproducible pipeline from corpus to demo API.

## Pain it closes

| Pain | Without KazNLP | With KazNLP |
|------|----------------|-------------|
| “How much mixed do we have?” | Answer from auto-labels, ~**98%** noise | Diagnostics **1.66% / 2.32%** + gold test **96.56%** |
| Training on “mixed” | kz with loanword enters the sample | Filter-first: LID v2, then tone |
| Comparing approaches | Each model on its own eval | One ladder, test **n = 461** |
| Reproducibility | “Open the notebook and trust” | `eval_tone_v1.py`, weights on disk, `run_demo.py` |
| Low-resource labeling | Manual work in CSV | `labeling_service`: queue, gold export |

It closes a specific gap: you cannot work honestly with mixed KZ text while LID is wrong.

## Before, after, path

**Before the project**

- Telegram **422k**, `language` column from FastText at scrape, not gold.
- FastText v1: F1 **84.96%** on **96k** synthetic. Task looked solved.
- Real Telegram: almost all FT-“mixed” were false.
- Lingua v2: **95.97%** on seeds, on gold test recall mixed **98.76%**, precision **76.81%** — dangerous for corpus filter.
- No gold for shala-Kazakh at project scale.
- Tone on mixed: unclear which texts to train on.

**Path (how we got here)**

Measure noise → reject shortcuts (synthetic, FT v2 on corpus, Lingua) → build gold **3,076** → train XLM-R on raw `text` → prove on single test §10 → apply to corpus → add tone and product.

```
BEFORE: auto-LID → “everything mixed” → analytics and models on noise
          ↓
PATH:   diagnostics → gold → XLM-R v2 → ladder §10
          ↓
AFTER:  filter-first cascade, 331k with LID v2 labels
```

**After the project**

- Gold LID **3,076**; val/test gold-only; synthetic train-only.
- XLM-R LID v2: **96.56%** macro-F1; mixed P/R ~**95%** on test **n = 461**.
- Baseline ladder: FT v2 **70.92%** → Lingua v2 **88.63%** → XLM-R **96.56%**.
- `main.csv` **331,468** rows; **16,364** model-predicted mixed (not human-audited).
- Tone v1: **97.33%** on test **n = 525** (see LLM-label caveat below).
- Cascade TEXT → LID → route → tone; demo and labeler run locally.

## Who suffers without a fix

An NLP researcher cannot publish an honest code-switching rate on KZ corpora. A social analyst gets language dashboards wrong by orders of magnitude. A team training sentiment on mixed gets kz-with-loanword instead of code-switch. At defense, without a measured problem, the project looks like “another BERT at 97%.” KazNLP closes a research and methods gap; others can reuse the filter and open pipeline.

## Why now

XLM-R sees whole-phrase context; FastText and rules on **422k** real texts hit a ceiling. KZ digital grew (Telegram, marketplaces, geo services). Without gold you cannot prove a strong model to reviewers: **3,076** manual labels and one test beat another **100k** auto-labels.

---

# II. Research chronology (`main.ipynb`)

Notebook chronology is project logic. Chapters below follow execution order.

## Chapter 1. False confidence from synthetic (cells 0–21)

Start: Hugging Face (KazSAnDRA **180,064**, clapAI ru **164,148**), **480,000** synthetic ru/kz/mixed with `popular_ru_kaz` and `essential_ru_kaz` vocabularies, FastText v1 training.

On hold-out **96,000** rows F1 **84.96%**. On paper LID was almost done. Next — real Telegram.

## Chapter 2. Real corpus breaks the picture (cells 22–44)

Telethon collection from KZ channels; FastText v1 sets `language` at scrape. Dataset grew: **146,206** → **241,576** → **422,141** on disk.

Visually almost everything tagged “mixed” looks like Russian or Kazakh with a loan. Key question: how much of auto-mixed is real code-switch?

## Chapter 3. Diagnostics (cells 45–64)

We measured noise first, not transformers.

`is_real_mixed()` on FT-mixed: **460** of **27,628** (~**1.66%**). **411** hidden mixed in `language=ru`. Pool **868** seeds (not gold; misses shala-Kazakh without ә/ң).

FT v2 on synthetic + seeds: recall **95.51%** (829/868) on seeds. On corpus after relabel **66,462** mixed, precision **2.32%** (1,542/66,462).

Shortcuts fail. Synthetic gives pretty F1 and does not transfer to real text.

## Chapter 4. Rules do not save (cells 65–113)

Lingua v1 on 868 seeds: **71.66%**. Lingua v2: **95.97%** on seeds; full pass **411k** Telegram → **6,517** candidates, manual check still needed.

On gold test (**n = 461**, §10): Lingua v2 macro-F1 **88.63%**, recall mixed **98.76%**, precision **76.81%**. High recall, low precision: corpus filter without review floods false mixed again.

In parallel Kaspi **39,129**. YouTube (~4.7k) not finished; Telegram + Kaspi + 2GIS were enough.

Need manual gold and a model that sees the full phrase.

## Chapter 5. Gold (cells 114–153)

Kaspi + Telegram, `cheap_clean`: **388,748** → **254,601** rows.

Gold in batches: manual labeling, heuristic-batch (mixed only), Lingua queue. After dedup **3,076**: ru **1,000**, kz **999**, mixed **1,077** → `gold_v1.csv`.

Training protocol:

- stratified split 80/10/10, `random_state=42`: train **2,691**, val **462**, test **461**;
- **538** synthetic hard patterns train-only;
- gold : synthetic weight **3:1**;
- XLM-R on raw **`text`**, not `text_norm` (~219/1077 mixed lose signal after normalization);
- LLM not used in gold LID (high false positive on mixed).

## Chapter 6. Proof: XLM-R LID v2 (cells 154–176, §10)

Training: Kaggle 2× T4, AdamW lr 2e-5, XLM-RoBERTa-base.

| Version | macro-F1 (gold test n = 461) |
|--------|----------------------------:|
| v1 | 95.92% |
| **v2** | **96.56%** |

Confusion matrix v2 (rows = true, cols = pred):

| | pred ru | pred kz | pred mixed |
|--|--------:|--------:|-----------:|
| true ru | 150 | 0 | 0 |
| true kz | 0 | 142 | 8 |
| true mixed | 2 | 6 | 153 |

**14 of 16** errors: kz ↔ mixed confusion.

§10 (cells 267–268), one `test.csv`:

| Model | macro-F1 |
|--------|--------:|
| FastText v1 | 63.24% |
| FastText v2 | 70.92% |
| Lingua v1 | 84.96% |
| Lingua v2 | 88.63% |
| **XLM-R v2** | **96.56%** |

Only XLM-R v2 gives balanced mixed P/R ~**95%** on hold-out. That is the main capstone scientific result.

## Chapter 7. Corpus application (cells 177–237)

XLM-R v2 rescored Kaspi+Telegram → `kaspi-telegram_dataset_v2.csv` (**254,652** on disk).

2GIS: negative **29,479**, positive **35,928** after cleaning. Final assembly only in **cell 237** (intermediate cells 203/221 have stale counts):

**`main.csv` — 331,468** (ru **281,409** · kz **33,695** · mixed **16,364**).

`main_mixed.csv` — model predictions, not manual audit. Corpus audit of 100 random mixed from Action Plan was not done. “16 thousand confirmed mixed” is wrong; correct: “16,364 candidates by LID v2, corpus precision not measured.”

## Chapter 8. Stretch goal: tone (cells 238–264)

Separate task, 2GIS domain. Gold tone: **3,529** mixed (pos **1,771**, neg **1,758**); `llm_composer` **3,312**, manual **217**. + **882** synthetic in train → **4,411** merged; test **525** gold-only.

Tone v1: accuracy **97.33%**, CM `[[257, 6], [8, 254]]` — matches `metrics_tone_test.json` and `scripts/eval_tone_v1.py`. v2 worse (**96.19%**), v1 in production.

**Caveat:** ~**94%** of tone gold used LLM draft; on test **488 of 525** rows are also `llm_composer`. **97.33%** reflects agreement with LLM labels on hold-out, not independent human validation. Manual subset (**217** rows) not evaluated separately.

## Chapter 9. Product

Filter-first architecture (`inference/pipeline.py`):

```
raw text → XLM-R LID v2 (ru | kz | mixed)
                    ↓
              auto-route
       ┌──────────┼──────────┐
       ru         kz        mixed
       ↓          ↓           ↓
   RuBERT      Kazakh BERT   Tone v1 (XLM-R)
  (pretrained) (pretrained)  (fine-tuned)
```

For ru/kz, tone goes through pretrained models; for mixed — fine-tuned XLM-R tone v1.

Reproduce:

```bash
python scripts/setup_demo_models.py
python run_demo.py              # http://127.0.0.1:8000/
python run_labeler.py           # gold labeling
python scripts/eval_tone_v1.py  # tone metrics
```

First API request may return 503 for 30–60 s (loading four models, ~8.56 GB).

## Chapter 10. Timeline (CRISP-DM)

| Week | Content |
|--------|------------|
| 1 | Action Plan, WBS, corpus collection |
| 1–2 | EDA, FastText/Lingua baselines, gold guidelines |
| 2–3 | XLM-R LID v2, Mixed Tone v1, labeler, demo |
| 3 | LID/tone metrics, CM, gold test ladder |
| 4 | Final Report, presentation, defense |

---

# III. Limits and conclusion

## Honest boundaries

- Single gold LID annotator; inter-annotator agreement not measured.
- `main.ipynb` (270 cells) does not replay via Run All; do not re-run Telethon cells **31, 35, 41, 88**.
- Defense path: artifacts on disk, cells **45, 173, 237, 268**, `eval_tone_v1.py`, `run_demo.py`.
- Tone and LID evaluated on different domains (Telegram/Kaspi vs 2GIS).
- **16,364** mixed in `main.csv` not manually audited on corpus.

These are student-scale research limits; details in `Final_Report.md` §3.5, §4.2.

## Conclusion

The project started with “why does everyone write mixed.” The answer was measurement: **~1.66%** on a diagnostic slice, **~2.32%** precision on corpus after FT v2, gold **3,076**, XLM-R v2 **96.56%** on test **n = 461**. Tone **97.33%** on mixed 2GIS is a stretch goal, secondary to LID. Demo and labeler show the pipeline left the notebook.

**30-second pitch:**

> In KZ social media, auto-LID tags almost everything as mixed. KazNLP measured noise on 422k Telegram, built gold 3,076, pushed XLM-R v2 to 96.56% macro-F1 on an honest test, and assembled an LID → tone cascade with a local demo.

**Before:** statistics and models on noise. **After:** filter-first pipeline with proven LID and explicit limits.

---

## Data sources

| Claim | Source | Verified |
|-------------|----------|-----------|
| Telegram 422,141 | `data/raw/telegram_code-switch_dataset.csv` | ✅ |
| Kaspi 39,129 | `data/processed/kaspi_reviews.csv` | ✅ |
| Gold LID 3,076 | `main.ipynb` cell 144, `gold_v1.csv` | ✅ |
| LID test 461 | `data/training/filter/v1/test.csv` | ✅ |
| XLM-R v2 96.56% | cells 173, 268 | ✅ |
| Ladder FT/Lingua/XLM-R | §10, n = 461 | ✅ |
| main.csv 331,468 | cell 237, disk | ✅ |
| main_mixed 16,364 | cell 237, model-predicted | ✅ + caveat |
| Tone v1 97.33% n = 525 | cell 255, `metrics_tone_test.json` | ✅ |
| 94% tone gold = LLM | `tone_mixed_balanced_audited.csv` | ✅ |
| 1.66% TP | cells 45–46 (460/27,628) | ✅, heuristic |
| 2.32% corpus precision | cell 61 (1,542/66,462) | ✅ |
| 16k human-audited | — | ❌ |
| Corpus audit 100 random | Action Plan | ❌ not done |

---

*Related docs: `docs/capstone/Final_Report.md` · `web/story.html` · `web/index.html` · `docs/capstone/presentation.pptx`*
