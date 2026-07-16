> **English version:** [README.md](README.md)

# KazNLP Labeler

Локальный веб-сервис для разметки **языка** (`ru` | `kz` | `mixed`) и **тона** (`positive` | `negative` | `skip`) на CSV.

```
labeling_service/
├── main.py                 # FastAPI entry
├── manual_labeling.py      # ручной режим
├── llm_provider.py         # Ollama / Gemini
├── text_heuristics.py      # QC для tone merge / weak bilingual
├── templates/index.html
├── static/                 # app.js · manual.js · style.css
├── uploads/                # job cache (gitignored, ~1 GB)
└── README.md
```

Запуск из корня: `python run_labeler.py` (не из этой папки).

- **Language:** ручной режим + опциональный LLM-batch (Ollama).
- **Sentiment:** только ручной gold; LLM-batch тон не размечает.
- На capstone через labeler собраны **3 076** gold LID и большая часть **3 529** tone gold (`llm_composer` + manual fixes).

**Провайдер по умолчанию:** [Ollama](https://ollama.com) (локально, без лимитов API). Опционально: Google Gemini (`LABELER_PROVIDER=gemini`).

## Setup

1. Ollama и модель (8 GB RAM, CPU):

```bash
ollama pull qwen2.5:3b
```

2. `.env` в корне проекта (см. `.env.example`):

```
LABELER_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_NUM_CTX=8192
```

3. Зависимости:

```bash
pip install -r requirements-labeler.txt
```

### Модели Ollama (8 GB RAM)

| Model | RAM | ru/kz/mixed |
|-------|-----|-------------|
| **qwen2.5:3b** | ~2.5 GB | рекомендуется |
| qwen2.5-coder:1.5b | ~1 GB | быстрее, слабее на mixed |
| llama3.2:3b | ~2 GB | альтернатива |
| 7B+ | 5+ GB | не рекомендуется на 8 GB |

### Режимы качества LLM (`LABELER_QUALITY`)

| Mode | Batch | Few-shot | Verify mixed |
|------|-------|----------|--------------|
| `fast` | 50 | no | no |
| `balanced` | 25 | yes | no |
| `high` | 10 | yes | yes |
| `max` | 3 | yes | yes |

`OLLAMA_BATCH_SIZE` переопределяет batch. На 8 GB: `high` или `max` + `precision_filter.py` после batch.

## Run

Из **корня проекта**:

```bash
python run_labeler.py
```

http://localhost:8000 (или следующий свободный порт, если 8000 занят demo).

Вкладки UI: **Manual review** · **LLM batch** · **Upload**.

## CSV format

Обязательные колонки: `text`, `language`, `label`

| Режим | Что пишет |
|-------|-----------|
| LLM batch | только `language` (ru/kz/mixed), draft |
| Manual Language | gold `language` |
| Manual Sentiment | `label` (positive/negative/skip), `tone_source=manual` |

Опционально: `confidence`, `needs_review`, `label_source`.

Экспорт: manual gold / tone_labeled / full dataset (dropdown в LLM batch).

## Manual review: перевод

Чекбокс **«Авто-перевод RU»**, клавиша **`T`**.

- [MyMemory](https://mymemory.translated.net/) `kk|ru`, не LLM.
- `MYMEMORY_EMAIL` в `.env` → лимит ~10 000 слов/день.
- Подсказка для разметчика; gold-метка по оригиналу.

## Features

- Ollama или Gemini (`LABELER_PROVIDER`)
- SSE: прогресс batch в реальном времени
- Resume после каждого batch
- «Only empty language» для LLM batch
- Метрики сессии и баланс классов в sidebar

## Warning

LLM-метки языка — **draft**. Gold LID и tone для capstone проверялись вручную. Не использовать LLM-batch как единственный источник gold без аудита.
