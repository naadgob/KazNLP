# Notebook: main.ipynb

Generated: 2026-07-16
Path: `main.ipynb` (repo root)
Kernel: python3 / Python 3.11.9 · nbformat 4.5 · 274 cells
Reload helper: `python scripts/_nb_inventory.py` regenerates a compact cell+metrics dump.

> Read THIS file first in later chats. Re-scan `main.ipynb` only if the user says it changed.

## Overview

Solo Samsung Innovation Campus capstone. One research question drives the whole notebook: on Kazakh–Russian social/review text, automatic language ID and keyword heuristics wildly over-label "mixed" (code-switching), because Kazakh-with-Russian-loanwords looks mixed but isn't. The notebook builds a human-labeled gold set, benchmarks four LID approaches, fine-tunes XLM-R as a code-switch filter, runs it over a ~331k corpus, then trains a tone/sentiment head on the filtered code-switched slice.

Data flow: HF Kazakh/Russian corpora + scraped Telegram/Kaspi/2GIS → synthetic mixed generation → FastText v1/v2 → Lingua v1/v2 → gold LID (3,076) → XLM-R LID v1/v2 → score full corpus → tone gold (audited) → XLM-R tone v1/v2 → LID model comparison (incl. HeLI raw / neutral / windows-grid).

## Section map (cell ranges)

- 0–2: setup, dataset-on-disk map
- 3–21 (§1 FastText v1): synthetic mixed generator (480k lines, 160k/class), 80/20 split (384k/96k), FastText v1 → **F1 0.8496 on synthetic test (n=96,000)**
- 22–26 (§2.1 YouTube): `KazakhDataCollector`, raw sentiment CSV
- 27–49 (§2.2 Telegram + false-mixed diagnosis): Telethon scrape → 241,576 msgs; narrow heuristic tags **27,628 "mixed", only 460 true positive**; builds 868-row real-mixed seed (460 tp + 411 from ru)
- 50–64 (§3 FastText v2): real+synthetic mix (10k mixed = 868 real + 9,132 synth); v2 precision on real mixed 95.51% vs v1 43.09%; on corpus heuristic precision still only 2.32% (cell 63)
- 65–85 (§4 Lingua v1/v2): token-level detector; v1 71.66% / v2 95.97% precision on the 868 seed
- 86–112 (§5 Telegram chats + Kaspi scrape): corpus grows to 411,746; Kaspi reviews scraped (39,129)
- 113–177 (§6 XLM-R LID filter): merge Kaspi+Telegram (461,270→388,748 dedup→254,601 clean); **gold LID 3,076** (cell 144); split train 2,691 / test 461 / val 462; XLM-R v1 & v2 trained (10 epochs, ~7.5 min each)
- 178–187 (§7): run XLM-R over kaspi-telegram corpus
- 188–237 (§8 2GIS): scrape negatives (41,972) + positives (46,865+13,417); build final `main.csv` → **331,468 rows** (ru 281,409 / kz 33,695 / mixed 16,364)
- 238–264 (§9 tone): tone gold audited 3,503 + synthetic 882; split 3,334/525/526; XLM-R tone v1 & v2
- 265–275 (§10): head-to-head LID comparison on gold test (n=461): §10.1 FastText/Lingua, **§10.2 char-trigram NB** (added 2026-07-17), §10.3 HeLI raw/neutral, §10.3.1 HeLI+windows, Block 2 aggregation (cell 274) + §10.4 tables (cell 275)

## Findings & results (authoritative numbers)

### LID — gold test, n=461 (cell 268, macro-F1)

| Model | accuracy | macro-F1 | recall_mixed | precision_mixed |
|---|--:|--:|--:|--:|
| FastText v1 | 0.6486 | 0.6324 | 0.3354 | 0.5567 |
| FastText v2 | 0.7158 | 0.7092 | 0.4907 | 0.6583 |
| HeLI raw (heliport) | 0.7028 | 0.6973 | 0.5342 | 0.5890 |
| HeLI+neutral | 0.6898 | 0.6826 | 0.4907 | 0.5725 |
| HeLI+windows (best 2+3, min1) | 0.8720 | 0.8692 | 0.6894 | 0.9250 |
| Char-3gram NB (§10.2, char 3-gram + Laplace) | 0.8829 | 0.8800 | 0.7081 | 0.9421 |
| Lingua v1 | 0.8460 | 0.8496 | 0.8634 | 0.7394 |
| Lingua v2 | 0.8894 | 0.8863 | **0.9876** | 0.7681 |
| XLM-R v1 | 0.9588 | 0.9592 | 0.9441 | 0.9383 |
| **XLM-R v2** | **0.9653** | **0.9656** | 0.9503 | 0.9503 |

Best model = XLM-R v2: macro-F1 96.56%, acc 96.53%. Lingua v2 has the highest mixed recall (98.76%) but low precision (76.81%) — over-tags mixed. HeLI+windows grid best = sizes **(2,3)** min_count=1 → 86.92% macro-F1 (69/80 residual flip); tied with 2+3+4 etc.; raw/neutral stay ~0.70 next to FastText.

**Char-3gram NB** (§10.2, added 2026-07-17): char 3-gram CountVectorizer + Laplace-smoothed (alpha=1) MultinomialNB, trained on same `train.csv`, scored on same gold test → macro-F1 **88.00%** (acc 88.29%). Strongest simple character baseline (near-perfect monolingual: ru recall 0.973, kz 0.980; mixed precision 0.942) but mixed recall only **0.708** (47/161 true mixed read as monolingual) — sub-word signal separates the two languages yet misses the borrowing-vs-switch boundary that XLM-R closes. A heavier char 2–4 TF-IDF + LinearSVC scored lower (0.811). Reviewer-requested (kk/ru share Cyrillic).

### The over-labeling evidence (the paper's hook)

- Narrow keyword heuristic on 241,576 Telegram msgs: 27,628 flagged "mixed", manual check → 460 real (~1.7% precision). (cells 45–46)
- FastText v2 over the corpus: 66,462 predicted mixed, heuristic-verified precision 2.32% (cell 63).
- Synthetic-trained FastText v1: 84.96% F1 on its own synthetic test, collapses to 63.24% macro-F1 on real gold → synthetic/heuristic LID doesn't transfer to real UGC.

### Corpus after XLM-R filtering

Final `main.csv` = 331,468 texts; only **16,364 (~4.9%) are real code-switching**; ru 281,409, kz 33,695.

### Tone (secondary) — test n=525

XLM-R tone v1: macro-F1 / acc 0.9733; v2: 0.9619. Binary pos/neg on the code-switched review slice. Gold = 3,503 audited (neg 1,754 / pos 1,749) + 882 synthetic; splits 3,334 / 525 / 526.

## Data dependencies

- HF: Kazakh/Russian source corpora (login via `HF_TOKEN` env, cell 7); kaz_data 180,064 & 164,148 rows
- Scraped: `data/raw/telegram_code-switch_dataset.csv`, `data/processed/kaspi_reviews.csv`, `data/raw/2gis_reviews_{negative,positive}.csv`
- Gold/labeled: `data/manual labeling/language/{kaspi-telegram_part-labeled,mixed-heuristic-seed_labeled,lingua_candidates_labeled}.csv`; `data/processed/gold_v1.csv`
- Tone: `data/processed/tone_mixed_balanced_audited.csv`, `data/processed/tone_synthetic.csv`
- Models: `models/xlm-roberta/xlm-r_v{1,2}.pt`, `models/xlm-roberta/tone/xlm-r_v{1,2}.pt`; base `xlm-roberta-base`
- External scripts: `collect_2gis_reviews.py`

## Key variables & objects

- `gold_df` → gold LID (3,076, cols text/language/label), cell 144
- `main_dataset` / `main_mixed` → full scored corpus (331,468) + mixed slice (16,364), cells 203/237
- XLM-R LID: `LidDataset`, `WeightedCollator` (sample_weight gold=3.0, synth=1.0), `fit(...)`; `MixedSearchingDataset` for inference (cell 180)
- Labels: LID `{ru:0, kz:1, mixed:2}`; tone `{negative:0, positive:1}`

## Risks & gaps

- Many code cells show `execution_count: null` (<UNRUN>) yet carry outputs — results captured across sessions, not a single clean top-to-bottom run. Reproducibility caveat for a paper.
- Corpus "mixed" (16,364) is model-predicted, not human-audited end to end.
- Tone labels are LLM-assisted then audited; small test (525); 97% partly measures agreement with the labeling process.
- Hardcoded Windows paths (`r'data\...'`), a couple of typo'd save paths (cell 186 `processedkaspi-telegram...` missing separator).
- Naming collision: NU/NLA already published a toolkit called **KazNLP** — use a distinct paper/name (e.g. ShalaLID / kk-ru SwitchFilter).
- Leakage handled correctly: train = gold+synthetic, val/test = gold only.

## Open questions

- Which XLM-R version ships as the released weights — v2 for LID (best) and v1 for tone (best)? Notebook keeps both.
- Is the 16,364 mixed slice going to be human-audited before any resource-paper release?

## HeLI / heliport integration (done 2026-07-17)

Hook: Tommi Jauhiainen → [heliport](https://github.com/ZJaume/heliport) as non-neural baseline + loanword neutralization.

**Where:** §10.3 in `main.ipynb` (cells 268–269 raw/neutral; 270–271 HeLI+windows grid); Block 2 + §10.4 in cells 272–273. Helper: `scripts/heli_lid.py` (`grid_search_windows`). Loanwords: `data/processed/heli_loanwords_v1.txt` (1494).

**Gold test n=461 results:**
| Model | accuracy | macro-F1 | R(mixed) | P(mixed) |
|---|--:|--:|--:|--:|
| HeLI raw | 0.7028 | 0.6973 | 0.5342 | 0.5890 |
| HeLI+neutral | 0.6898 | 0.6826 | 0.4907 | 0.5725 |
| HeLI+windows (best 2+3, min1) | 0.8720 | 0.8692 | 0.6894 | 0.9250 |

Residuals: gold_kz rus→kaz after strip=0; gold_mixed still rus=80 (**69/80** flip under best windows sizes=(2,3) min_count=1; same F1 as 2+3+4). Dep: `heliport` in `requirements.txt`. `grid_search_windows` / `predict_windows` in `scripts/heli_lid.py`.
