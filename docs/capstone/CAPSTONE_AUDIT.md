> **Russian version:** [CAPSTONE_AUDIT_RU.md](CAPSTONE_AUDIT_RU.md)

# KazNLP audit — Capstone AI Project

**Date:** 12 June 2026  
**Reference:** Samsung Innovation Campus Capstone rubric (100 points)  
**Status:** project **complete** (code + models + demo); paperwork hand-in in progress

---

## 1. Required artifacts

| # | Requirement | Status | Path |
|---|-------------|--------|------|
| 1 | Action Plan | 🟢 | `docs/capstone/Action_Plan.md` · `Action_Plan.docx` |
| 2 | WBS | 🟡 | `docs/capstone/WBS.csv` on disk · `WBS.xlsx` via `export_capstone_docs.py` |
| 3 | Code / Jupyter | 🟢 | `main.ipynb`, `labeling_service/`, `scripts/` |
| 4 | Data | 🟢 | gold 3076, corpus 422k+, README |
| 5 | Final Report | 🟢 | `Final_Report.md` · `Final_Report.docx` |
| 6 | Presentation | 🟢 | `docs/capstone/presentation.pptx` (live: `web/story.html`) |
| 7 | Defense | ⏳ | Rehearsal + live demo |

---

## 2. Models and weights (verified on disk)

| Model | File | Status |
|-------|------|--------|
| FastText v1/v2 | `models/fasttext/*.bin` | ✅ |
| XLM-R LID v2 | `models/xlm-roberta/xlm-r_v2.pt` | ✅ |
| Mixed Tone v1 | `models/xlm-roberta/tone_v1.pt` | ✅ |
| RU tone pretrained | `models/tone_pretrained/ru_rubert_rureviews/` | ✅ |
| KZ tone pretrained | `models/tone_pretrained/kz_kazakh_sentiment_bert/` | ✅ |

**Inference:** `python run_demo.py` → 4 models, live `/analyze`.

---

## 3. Metrics (reproducible)

| Task | Metric | Source |
|------|--------|--------|
| LID XLM-R v2 | macro-F1 **96.56%**, test n=461 | `main.ipynb` executed |
| LID CM v2 | ru 150/150, kz↔mixed 14 err | `main.ipynb` |
| FastText v1 synthetic | F1 **84.96%** | `main.ipynb` ch.1 |
| FastText v2 seeds | P(mixed) **95.51%**, n=868 | `main.ipynb` ch.4 |
| Mixed Tone v1 | acc **97.33%**, CM `[[257,6],[8,254]]` | `scripts/eval_tone_v1.py` · §7.3 |
| Mixed Tone v2 | acc **96.19%** | `scripts/eval_tone_v1.py` |

Saved: `data/processed/metrics_tone_test.json`

---

## 4. SIC rubric score

| Category | Max | Score | Comment |
|----------|-----|------:|---------|
| **IDEA** | 10 | **9** | Strong local problem; +1 for related work |
| **APPLICATION** | 30 | **27** | Full stack; −3 for no corpus audit 100 / Colab |
| **RESULT** | 30 | **26** | Strong metrics; gold test ladder in `main.ipynb` §10 |
| **PROJECT MANAGEMENT** | 10 | **9** | WBS updated, docx/xlsx present |
| **PRESENTATION & REPORT** | 20 | **17** | Report + `presentation.pptx`; −3 for video/screenshots in docx |
| **TOTAL** | 100 | **87** | FT gold ladder in §10; video + docx screenshots remain |

---

## 5. Remaining gaps (priority)

| P | Task | Owner |
|---|------|-------|
| P1 | Demo video 2–5 min | Author |
| P1 | Corpus audit 100 mixed | Optional |
| P2 | Colab inference notebook | Optional |
| P2 | UI screenshots in Final Report.docx | Author |

---

## 6. Anti-patterns (check)

| Anti-pattern | Verdict |
|--------------|---------|
| “94% accuracy and done” | ✅ No — macro-F1, CM, per-class |
| Broken baseline | ✅ FastText actually trained |
| Tutorial disguised as project | ✅ Own corpus, gold, labeler |
| API without metrics | ✅ Metrics + eval scripts |
| Fake pretrained passed off as own train | ✅ RU/KZ explicitly pretrained |

---

## 7. Commands before defense

```bash
python scripts/eval_tone_v1.py          # tone metrics
python scripts/verify_tone_pretrained.py
python run_demo.py                      # warm-up ~60s CPU
python scripts/export_capstone_docs.py  # refresh docx/xlsx
```

**Defense-day checklist:** weights in place · demo warmed up · pptx · name in docx · answer ready for “mixed vs kz loanword”.
