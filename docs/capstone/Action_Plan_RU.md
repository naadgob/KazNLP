> **English version:** [Action_Plan.md](Action_Plan.md)

# Action Plan — Capstone AI Project

**Название проекта:** KazNLP — детекция шала-казахского (code-switching ru+kz) в соцмедиа Казахстана

**Автор:** Bogdan Savelyev

**Трек:** Deep Learning / NLP (transfer learning, трансформеры)

**Дата:** 1 июня 2026

---

## Стартовый план (из задания)

| Поле | Заполнение |
|------|------------|
| **Какую проблему решаем** | В комментариях Telegram и отзывах Kaspi.kz часто встречается **шала-казахский**: в одном сообщении смешаны **отдельные русские и казахские фразы/предложения**. Автоматические LID-модели (FastText, эвристики) дают много ложных срабатываний на «mixed». Нужен **высокоточный фильтр** ru / kz / mixed, чтобы дальше анализировать только настоящий code-switching (в т.ч. тональность). |
| **Кто пользователь результата** | Исследователи NLP и социолингвистики (low-resource + code-switching); аналитики маркетплейсов и медиа, которым важны **казахоязычные и смешанные** отзывы; разработчики, которым нужен открытый датасет и инструмент разметки. |
| **Какие данные используем (источник)** | 1) **Собственный корпус:** Telegram-каналы/чаты KZ (~422k строк, `data/raw/telegram_code-switch_dataset.csv`), отзывы Kaspi (~39k, `data/processed/kaspi_reviews.csv`), объединённый пул ~269k (`data/processed/kaspi-telegram_dataset.csv`). 2) **Gold LID (ручная разметка):** `data/processed/gold_v1.csv` — **3076** примеров (mixed 1077, ru 1000, kz 999), источники: Kaspi, Telegram, Lingua-кандидаты; разметка через `labeling_service/`. 3) **Синтетика LID (только train):** `data/processed/synthetic/synthetic_all.csv` — 538 строк (`scripts/merge_synthetic.py`; папка появляется после прогона) |
| **Что будет входом модели** | Текст комментария/отзыва после нормализации (`text_norm`): lowercasing, удаление URL/упоминаний, сжатие повторяющейся пунктуации. |
| **Что будет выходом** | Класс **ru** \| **kz** \| **mixed** + уверенность; для **mixed** — бинарный тон pos/neg (Mixed Tone v1, 97,33% на test n=525, 2GIS). RU/KZ — pretrained routing. |
| **Baseline (самое простое возможное решение)** | 1) **FastText** supervised LID (`models/fasttext/fasttext_v1.bin`, `models/fasttext/fasttext_v2.bin`) на синтетике + сидах. 2) **Эвристика** «казахские буквы + кириллица» (`data/processed/mixed_heuristic_seed.csv`). 3) **Lingua** language detector на подвыборке. 4) **HeLI/heliport** (Tommi Jauhiainen): список заимствований + strip → re-ID, затем overlapping windows с коротким grid (`scripts/heli_lid.py`; best окна 2+3, min_count=1 → 86.92% macro-F1). 5) **char-триграм NB** (`main.ipynb` §10.2): сглаженный char 3-gram + Laplace NB → 88.00% macro-F1. Сравнение на **gold_v1** (hold-out test). |
| **Какую метрику будем использовать** | Многоклассовая классификация: **macro-F1**, **per-class precision/recall**, **confusion matrix**. Для фильтра mixed — **precision на классе mixed** (цель ≥0.85 на ручном аудите 100 случайных предсказаний из корпуса). Accuracy — вспомогательная (классы сбалансированы в gold). |
| **Что считаем успешным результатом** | Рабочий **proof of concept**: (1) открытый gold-датасет LID ≥3k примеров; (2) fine-tuned **XLM-R-base** 3-class, превосходящий FastText на test; (3) скрипт скоринга корпуса → `mixed_candidates.csv`; (4) демо (Gradio / labeler); (5) честный разбор ошибок и ограничений в Final Report. |

---

## Цель проекта

Построить воспроизводимый NLP-pipeline для **надёжного отделения настоящего ru+kz code-switching** от монолингвального русского/казахского с заёмами в соцмедиа Казахстана и подготовить открытые артефакты для дальнейшего анализа тональности.

---

## Метод

**CRISP-DM:** постановка → данные/EDA → baseline → основная модель → оценка → оформление.

**Основное решение:** transfer learning — **XLM-RoBERTa-base** (`xlm-roberta-base`), 3 класса, fine-tune на `gold_v1` (+ синтетика только в train). Обучение: PyTorch + Hugging Face Trainer, 2× T4 (DDP), batch 8/GPU, 3–4 эпохи, stratified split 80/10/10.

**Почему XLM-R, а не только FastText:** мультиязычный контекст, устойчивость к коротким соцмедиа-текстам и смешанным границам фраз; FastText остаётся честным baseline.

**Инструменты:** Python, pandas, Hugging Face, FastText, собственный **labeling_service** (ручная разметка + Ollama draft).

---

## Данные — детали

| Набор | Объём | Роль |
|-------|-------|------|
| gold_v1 | 3076 | Единственный **gold** для обучения/оценки LID |
| synthetic_all | 538 | Дополнение train (hard patterns), не в val/test |
| telegram raw | ~422k | Корпус для скоринга после обучения |
| kaspi reviews | ~39k | Источник gold + корпус |
| lingua_candidates | ~6.5k | Кандидаты в очередь разметки, **не gold** |

**Правила меток:**
- `mixed` — в одном комментарии есть **и русская, и казахская фраза/предложение**.
- `kz` — казахская грамматика; русские **заёмные слова** (качество, чехол) ≠ mixed.
- `ru` — монолингвальный русский.

**Предобработка:** `normalize_text()` → колонка `text_norm` (см. `data/processed/gold_v1.csv`).

---

## План работы по этапам (4 недели)

| Этап | Срок | Содержание | Статус |
|------|------|------------|--------|
| **1. Постановка** | нед. 1 | Тема, трек, Action Plan, сбор корпуса | ✅ |
| **2. Данные и baseline** | нед. 1–2 | EDA gold, guidelines, FastText/Lingua/HeLI baseline | ✅ (EDA + gold + §10 ladder вкл. heliport windows grid) |
| **3. Решение** | нед. 2–3 | Fine-tune XLM-R LID v2 + Mixed Tone v1, labeler, demo | ✅ |
| **4. Оценка** | нед. 3 | LID/tone metrics, CM, ошибки; audit 100 — отложено | ✅ частично |
| **5. Оформление** | нед. 4 | Final Report.docx, WBS.xlsx, презентация, защита | 🔄 pptx / video |

---

## Риски и митигация

| Риск | Митигация |
|------|-----------|
| Путаница kz vs mixed (заёмные слова) | Чёткие guidelines; hard negatives в синтетике; аудит граничных случаев |
| Синтетика короче gold | Использовать только в train; spot-check 10%; доработать ru-синтетику (аудит: 50% strict на ru) |
| Нет GPU локально | Kaggle / Colab 2×T4, фиксированный seed и requirements |
| Недостаток времени на tone | Реализован Mixed Tone v1; ru/kz — pretrained routing |

---

## Артефакты сдачи

1. `docs/capstone/Action_Plan.md` (этот файл → **Action Plan.docx**)
2. `docs/capstone/WBS.csv` → **Work Breakdown Structure.xlsx**
3. `main.ipynb` + скрипты обучения/скоринга
4. `data/processed/gold_v1.csv` + README с источниками
5. `docs/capstone/Final_Report.md` → **Final Report.docx**
6. Презентация: `docs/capstone/presentation.pptx` (аутлайн `PRESENTATION_OUTLINE.md`; live `web/story.html`)
7. Демо: `run_demo.py` (сайт + API) + `run_labeler.py` + запись 2–5 мин

---

## Ссылки на репозиторий

```
KazNLP/
├── main.ipynb · run_demo.py · run_labeler.py
├── data/processed/gold_v1.csv · main.csv · tone_*
├── data/training/filter/v1/ · data/training/tone/v1/
├── models/fasttext/ · models/xlm-roberta/ · models/tone_pretrained/
├── inference/ · labeling_service/ · web/ · scripts/
└── docs/capstone/                  # Action_Plan · Final_Report · presentation.pptx
```

- Корень: `KazNLP/`
- Gold: `data/processed/gold_v1.csv`
- Labeler: `labeling_service/`, `run_labeler.py`
- LID synthetic merge: `scripts/merge_synthetic.py` → `data/processed/synthetic/synthetic_all.csv` (после прогона)
- Live презентация: `web/story.html` · SIC pptx: `docs/capstone/presentation.pptx`
