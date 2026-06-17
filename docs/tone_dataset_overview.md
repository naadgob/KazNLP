## Tone dataset overview (gold + synthetic)

> **Note:** This section is an overview prepared by **Cursor AI** following the KazNLP project audit (June 2026). It is not official annotation or peer review; spot-check conclusions manually before your defense.

### Pipeline (as in `main.ipynb`)

| Step | Where | Artifact |
|------|-------|----------|
| 1 | **Ch. 6** — collect 2GIS negative/positive, LID via XLM-R (`xlm-r_v2.pt`) | `2gis_reviews_negative.csv`, `2gis_reviews_positive.csv` |
| 2 | **§7.1** — filter `language == mixed` | `2gis_reviews_negative_mixed.csv` (~29.5k), `2gis_reviews_positive_mixed.csv` (~3.0k); plus overlap with `main_mixed.csv` (~15k mixed from Kaspi/TG+2GIS) |
| 3 | **Outside notebook** — `python run_labeler.py` (Sentiment mode): `llm_composer` draft + manual fixes | `label_source`: `llm_composer` (3312) + `manual` (217) |
| 4 | pos/neg balance, manual audit (cross-check with 2GIS rating, fix inversions) | **`tone_mixed_balanced_audited.csv`** — 3529 gold |
| 5 | ~20% synthetic supplement (train only) | `scripts/generate_tone_synthetic.py` → `data/processed/tone_synthetic.csv` (882) |
| 6 | Merge + QC + dedup | `scripts/merge_tone_synthetic.py` → **`tone_train_mixed.csv`** — 4411 |

---

### Source files (current)

| File | Rows | Description |
|------|-----:|-------------|
| `data/processed/tone_mixed_balanced_audited.csv` | 3529 | Gold: mixed 2GIS reviews (+ part of the shared mixed pool), labels `positive` / `negative` |
| `data/processed/tone_synthetic.csv` | 882 | Synthetic (~20% of merged train); `batch` column tags the 8 generation groups |
| **`data/processed/tone_train_mixed.csv`** | **4411** | Final train = gold + synth after QC and dedup |

**Gold composition:** 3312 rows with `label_source=llm_composer` (`language=mixed`) + 217 manual (`label_source=manual`). Balance: 1771 pos / 1758 neg.

**Train composition:** same 3529 gold + 882 synthetic (`label_source=synthetic`) → 2207 pos / 2204 neg (~20% synthetic in merged set).

---

### Issues in the original (gold) dataset

1. **Labeling errors (critical, rare).** Label inversions vs meaning and the original 2GIS rating. Example: pure praise with 5★ labeled `negative`, a scathing review with 1★ labeled `positive`. **2 rows** found and fixed during audit; at scale expect ~0.05–0.1% of such cases.

2. **Mixed tone without a clear dominant (~5–8%).** A review praises and criticizes at once (*"service жақсы, kitchen онша емес"*). For a binary classifier this is noise: the label is formally valid but debatable for humans.

3. **Weak code-switch (~13%).** Text is almost monolingual with 1–2 loanwords (*"Очень вкусно поели, сытно"*). For "tone of mixed utterances" the model sees little real language switching — not critical, but worth tracking in error analysis.

4. **Length bias.** Negative averages ~138 characters, positive ~95. Short positive vs long negative risks learning length instead of sentiment.

5. **Domain gaps.** Gold has little finance, housing, fitness; lots of food/restaurants. The model may overfit to the restaurant domain.

6. **Realistic noise (not a bug).** Typos, CAPS, profanity, fragments — normal for 2GIS; do not strip.

---

### Mitigations (what the project did)

| Issue | Mitigation |
|-------|------------|
| Label errors | Manual audit + 2GIS rating cross-check; fixes in `tone_mixed_balanced_audited.csv` |
| Weak mixed / domains / length | **~20% synthetic in train** — 8 targeted batches (`scripts/generate_tone_synthetic.py`) |
| Gold↔synth duplicates | `scripts/merge_tone_synthetic.py` — `normalize_text` + dedup against gold |
| QC (pure RU/KZ, weak bilingual) | `labeling_service/text_heuristics.py` + `scripts/merge_synthetic.qc_row` в `merge_tone_synthetic.py` |
| Label contamination in synth | `label_contamination()`, salt only with neutral context (city/time/price) |
| Source transparency | `label_source` column: `llm_composer` / `manual` / `synthetic` |

**Regenerate synthetic data and merge:**

```bash
python scripts/generate_tone_synthetic.py
python scripts/merge_tone_synthetic.py
```

---

### Why and how synthetic data was added

**Goal:** not to replace gold, but to **fill systematic gaps** — rare domains, short positive, long positive vs short negative, reviews with dominant tone despite mixed praise+complaint.

**8 batches (882 rows, 436 pos / 446 neg):**

| # | Batch | Rows | Purpose |
|---|-------|-----:|---------|
| P1 | `batch_01_clear_mixed` | 200 | Clear code-switch, unambiguous tone |
| P2 | `batch_02_split_dominant` | 120 | Praise + complaint, label = dominant side |
| P3 | `batch_03_delivery` | 80 | Delivery (55 pos / 25 neg) |
| P4 | `batch_04_med_finance_housing` | 100 | Healthcare, banking, utilities |
| P5 | `batch_05_beauty_negative` | 80 | Salons, negative-heavy |
| P6 | `batch_06_short_punchy` | 120 | 40–90 chars, mixed |
| P7 | `batch_07_length_balance` | 100 | Long pos / short neg |
| P8 | `batch_08_fitness_retail_auto` | 82 | Gym, supermarket, auto service |

**Synthetic limitations (honest):** templated openings, "textbook" mixed stronger than in gold; **≤20%** of merged train is the cap used in this project.

---

### Takeaways for training

- **Train:** `tone_train_mixed.csv` — 4411 rows, pos/neg balance ≈ 50/50, ~20% synthetic in merged set.
- **Gold left largely untouched** — 2GIS realism preserved; synthetic data covers gaps.
- **Before defense:** spot-check 50–100 random rows; report metrics separately on short positive and long negative subsets.
