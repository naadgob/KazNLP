---
license: apache-2.0
task_categories:
  - text-classification
language:
  - ru
  - kk
tags:
  - kaznlp
  - code-switching
  - sentiment-analysis
  - language-identification
---

# KazNLP model weights

Weights for the [KazNLP](https://github.com/naadgob/KazNLP) Samsung Innovation Campus capstone (Bogdan Savelyev).

## Contents (`models.zip`, ~8.2 GB)

| Path | Role |
|------|------|
| `models/fasttext/fasttext_v1.bin`, `fasttext_v2.bin` | LID baselines |
| `models/xlm-roberta/xlm-r_v2.pt` | XLM-R LID v2 (96.56% macro-F1, gold test n=461) |
| `models/xlm-roberta/tone_v1.pt` | Mixed tone v1 (2GIS) |
| `models/tone_pretrained/ru_rubert_rureviews/` | RU sentiment routing |
| `models/tone_pretrained/kz_kazakh_sentiment_bert/` | KZ sentiment routing |

## Install

```bash
pip install huggingface_hub
python scripts/download_kaznlp_weights.py
python scripts/setup_demo_models.py
python run_demo.py
```

Or download `models.zip` from this dataset and unzip into the project root (folder `models/` must appear next to `README.md`).

## Citation

Capstone report: `docs/capstone/Final_Report.md` in the GitHub repo.
