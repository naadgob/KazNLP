# KazNLP

**Capstone:** Samsung Innovation Campus · Deep Learning / NLP  
**Автор:** Bogdan Savelyev  
**Задача:** тональность (pos/neg) на **смешанных** отзывах 2GIS, где в одном тексте русский и казахский. Без честного фильтра **ru / kz / mixed** такую выборку не собрать: auto-LID на Telegram помечает почти всё как mixed, хотя большая часть строк — kz с русским заёмным словом.

Полная история и цифры для жюри: [`STORY.md`](STORY.md) · веб-версия [`web/story.html`](web/story.html) (генерация: `python scripts/build_story_landing.py`).

---

## Ключевые числа (канон защиты)

Источник: `main.ipynb` (cells 45, 173, 237, 255, 268), `docs/capstone/Final_Report.md`, `data/processed/metrics_tone_test.json`.

| Что | Значение | Файл / ячейка |
|-----|----------|----------------|
| Telegram (контекст LID) | 422 141 | `data/raw/telegram_code-switch_dataset.csv` |
| Kaspi | 39 129 | `data/processed/kaspi_reviews.csv` |
| Gold LID (ru/kz/mixed) | 3 076 (1000 / 999 / 1077) | `data/processed/gold_v1.csv` · cell 144 |
| LID test | n = 461 | `data/training/filter/v1/test.csv` |
| **XLM-R LID v2** | macro-F1 **96,56%** | `models/xlm-roberta/xlm-r_v2.pt` · cells 173, 268 |
| `main.csv` | 331 468 строк | cell 237 |
| `main_mixed.csv` | 16 364 (model-predicted, не audited) | cell 237 |
| Gold tone (2GIS mixed) | 3 529 | `data/processed/tone_mixed_balanced_audited.csv` |
| Synthetic tone (train only) | 882 (~20% от train) | `data/processed/tone_synthetic.csv` |
| Tone train | 4 411 | `data/processed/tone_train_mixed.csv` |
| Tone test | n = 525 | `data/training/tone/v1/test.csv` |
| **Mixed Tone v1** | accuracy **97,33%** | `data/processed/metrics_tone_test.json` · `scripts/eval_tone_v1.py` |
| Mixed Tone v2 (не в prod) | 96,19% | тот же JSON |
| Диагностика FT-mixed | ~1,66% true positive | cells 45–46 |

**Оговорка по tone 97,33%:** ~94% gold от `llm_composer`; метрика на hold-out = agreement с LLM-разметкой, не blind human eval. Подробнее в Final Report §3.3.3.

**О диске:** если пересчитывали CSV после cell 237, счётчики на диске могут отличаться (например `main.csv` >331k). На защите опирайтесь на **cell 237** и таблицу выше.

---

## Быстрый старт

### Веса моделей (~8,2 GB)

Не в git (лимит GitHub). **Hugging Face:**

**https://huggingface.co/datasets/naadgob/kaznlp-weights**

```bash
pip install huggingface_hub
python scripts/download_kaznlp_weights.py   # скачать models.zip и распаковать
python scripts/setup_demo_models.py         # symlink RU/KZ + проверка путей
```

Локально: распакуйте `models/models.zip` в корень репо (рядом с `README.md`).

### Demo (сайт + inference API)

```bash
pip install -r inference/requirements.txt
python run_demo.py
```

Windows: `start_demo.bat`. Открыть http://127.0.0.1:8000/ (`web/index.html` + `POST /analyze`).

Первый запрос может вернуть **503** 30–60 с, пока грузятся четыре модели (~8,5 GB). Сначала скачайте веса (см. выше) или положите `models.zip` вручную.

### Labeler (gold LID и tone)

```bash
pip install -r requirements-labeler.txt
ollama pull qwen2.5:3b    # для LLM-batch языка
python run_labeler.py
```

Порт по умолчанию 8000 (если занят — следующий свободный). См. [`labeling_service/README.md`](labeling_service/README.md).

### Метрики tone (без ноутбука)

```bash
python scripts/eval_tone_v1.py
```

---

## Структура репозитория

```
KazNLP/
├── main.ipynb                      # основной пайплайн (270 ячеек)
├── README.md · STORY.md
├── run_demo.py · run_labeler.py · start_demo.bat
├── collect_2gis_reviews.py         # скрапер 2GIS (CLI)
├── essential_ru_kaz.py · popular_ru_kaz.py
├── requirements.txt · requirements-labeler.txt
├── .env.example                    # шаблон секретов (не коммитить .env)
│
├── data/
│   ├── raw/                        # telegram_code-switch_dataset.csv, 2gis_*.csv
│   ├── processed/                  # gold_v1, main.csv, tone_*, metrics_tone_test.json
│   │   └── synthetic_tone/         # батчи tone synthetic (после generate_tone_synthetic.py)
│   ├── manual labeling/            # история ручной LID-разметки
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
├── labeling_service/               # labeler UI + LLM batch (см. README внутри)
│   ├── main.py · manual_labeling.py · text_heuristics.py
│   ├── templates/index.html
│   └── static/                     # app.js · manual.js · style.css
│
├── web/
│   ├── index.html                  # лендинг + live demo
│   ├── story.html                  # нарратив для жюри (build_story_landing.py)
│   ├── assets/
│   │   ├── labeler/                # 01–03 PNG для карусели story
│   │   └── _verify-sources.png
│   └── README.md
│
├── scripts/                        # eval · export · deck · synthetic (см. таблицу)
│   └── archive/                    # старые LID synthetic/EDA (не defense path)
│
├── docs/
│   ├── README.md
│   ├── tone_dataset_overview.md
│   └── capstone/                   # SIC paperwork (ниже)
│
└── sessions/                       # Telethon *.session (gitignored)
```

### `docs/capstone/` (сдача Samsung)

| Файл | Назначение |
|------|------------|
| `Action_Plan.md` / `.docx` | стартовый план |
| `Final_Report.md` / `.docx` | финальный отчёт |
| `WBS.csv` | WBS (`.xlsx`: `export_capstone_docs.py`) |
| `presentation.pptx` | **единственная презентация** для SIC |
| `kaznlp-story-deck-self.html` | HTML-источник pptx (`build_self_deck.py`, может отсутствовать до пересборки) |
| `PRESENTATION_OUTLINE.md` | аутлайн 20 слайдов |
| `CAPSTONE_AUDIT.md` | чеклист перед защитой |

Live на защите: [`web/story.html`](web/story.html) (не заменяет `presentation.pptx` в paperwork).

---

## Пайплайны

### 1. Language ID (`main.ipynb`, главы 1–6)

| Этап | Артефакт |
|------|----------|
| Synthetic 480k | `training/fasttext_synthetic.txt` |
| FastText v1/v2 | `models/fasttext/fasttext_v1.bin`, `models/fasttext/fasttext_v2.bin` |
| Сбор Telegram | `data/raw/telegram_code-switch_dataset.csv` |
| Сбор Kaspi | `data/processed/kaspi_reviews.csv` |
| Ручной gold | `data/processed/gold_v1.csv` |
| XLM-R LID v2 | `models/xlm-roberta/xlm-r_v2.pt` |
| Мастер-корпус | `data/processed/main.csv`, `main_mixed.csv` |

Baseline ladder на одном test n=461: §10 (cells 267–268).

### 2. Mixed tone (`main.ipynb`, глава 8)

| Файл | Строк | Роль |
|------|------:|------|
| `tone_mixed_balanced_audited.csv` | 3 529 | `data/processed/` — gold pos/neg, 2GIS mixed |
| `tone_synthetic.csv` | 882 | `data/processed/` — synthetic только в train |
| `tone_train_mixed.csv` | 4 411 | `data/processed/` — итоговый train |
| `data/training/tone/v1/test.csv` | 525 | Gold-only hold-out |

Регенерация synthetic:

```bash
python scripts/generate_tone_synthetic.py
python scripts/merge_tone_synthetic.py
```

Gold tone: 2GIS → LID v2 → `language == mixed` → `run_labeler.py` (ручной режим + `llm_composer` draft) → баланс pos/neg.

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

См. [`models/tone_pretrained/README.md`](models/tone_pretrained/README.md).

---

## Скрипты (основные)

| Скрипт | Назначение |
|--------|------------|
| `setup_demo_models.py` | HF download + symlink RU/KZ + проверка путей |
| `download_kaznlp_weights.py` | Скачать `models.zip` с Hugging Face |
| `upload_kaznlp_weights.py` | Залить веса на HF (автор, token write) |
| `eval_tone_v1.py` | Метрики tone v1/v2 → `metrics_tone_test.json` |
| `generate_tone_synthetic.py` | 8 батчей synthetic tone (882) |
| `merge_tone_synthetic.py` | Сборка `tone_train_mixed.csv` |
| `download_tone_pretrained.py` | RU/KZ HuggingFace weights |
| `verify_tone_pretrained.py` | Smoke-test pretrained |
| `build_self_deck.py` | `kaznlp-story-deck-self.html` → `presentation.pptx` |
| `html_deck_to_pptx.py` | HTML deck → PowerPoint (screenshot export) |
| `export_capstone_docs.py` | md → docx/xlsx для сдачи |
| `build_story_landing.py` | `web/story.html` (live-нарратив для жюри) |
| `train_xlmr_ddp.py` | DDP-обучение XLM-R (вынесено из ноутбука) |
| `merge_synthetic.py` | LID synthetic → `data/processed/synthetic/synthetic_all.csv` (папка появляется после прогона) |
| `insert_tone_eval_notebook.py` | Вставка tone-eval ячеек в ноутбук (разовая утилита) |

Исторические batch-скрипты: `scripts/archive/` (не нужны для defense path).

**Defense path (минимум):** cells **45, 173, 237, 268** + `eval_tone_v1.py` + `run_demo.py`.

---

## Документация

| Файл | Содержание |
|------|------------|
| [`STORY.md`](STORY.md) | Полный нарратив, таблица источников |
| [`web/story.html`](web/story.html) | То же для жюри в браузере |
| [`docs/README.md`](docs/README.md) | Индекс всей документации |
| [`docs/capstone/Final_Report.md`](docs/capstone/Final_Report.md) | Финальный отчёт |
| [`docs/tone_dataset_overview.md`](docs/tone_dataset_overview.md) | Gold tone, synthetic, QC |
| [`docs/capstone/PRESENTATION_OUTLINE.md`](docs/capstone/PRESENTATION_OUTLINE.md) | Структура презентации |
| [`docs/capstone/CAPSTONE_AUDIT.md`](docs/capstone/CAPSTONE_AUDIT.md) | Чеклист SIC |
| [`docs/capstone/presentation.pptx`](docs/capstone/presentation.pptx) | Презентация SIC (единственный pptx) |
| [`labeling_service/README.md`](labeling_service/README.md) | Labeler setup |
| [`web/README.md`](web/README.md) | Demo site |

Презентация (SIC): [`docs/capstone/presentation.pptx`](docs/capstone/presentation.pptx) · live: [`web/story.html`](web/story.html) · пересборка HTML: `python scripts/build_self_deck.py`

---

## Важные замечания

- Колонка `language` в сыром Telegram — метка **сборщика** (FastText), не ground truth. По эвристике `is_real_mixed()` только ~**1,66%** FT-mixed — настоящий code-switch.
- **16 364** mixed в `main.csv` — предсказание LID v2, без выборочного аудита всего корпуса.
- `main.ipynb` **не** воспроизводится через Run All; не перезапускать Telethon cells **31, 35, 41, 88**.
- Не коммитить: `.env`, `sessions/`, `labeling_service/uploads/`.

---

## Секреты (`.env.example`)

| Переменная | Зачем |
|------------|--------|
| `HF_TOKEN` | HuggingFace datasets / models; **write** — только для `upload_kaznlp_weights.py` |
| `TELEGRAM_API_ID`, `TELEGRAM_API_HASH` | Telethon |
| `GEMINI_API_KEY` | Опционально для labeler (`LABELER_PROVIDER=gemini`) |
| `YOUTUBE_API_KEY` | YouTube-сбор (частично в ноутбуке) |
| `OLLAMA_*` | Labeler LLM-batch (по умолчанию) |
