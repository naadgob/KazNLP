# KazNLP web

```
web/
├── index.html              # лендинг + live demo (через run_demo.py)
├── story.html              # нарратив capstone (build_story_landing.py)
├── README.md
└── assets/
    ├── labeler/            # 01-manual-language.png … 03-llm-batch.png
    └── _verify-sources.png
```

| Файл | Назначение |
|------|------------|
| `index.html` | Продуктовый лендинг: исследовательский путь, метрики, live demo (`POST /analyze`) |
| `story.html` | История capstone для жюри (генерируется, не править вручную) |
| `assets/labeler/*.png` | Скриншоты labeler для карусели в `story.html` (на диске: `01`–`03`; обновить после смены UI → `build_story_landing.py`) |

Генерация story:

```bash
python scripts/build_story_landing.py
```

Источник разметки: `scripts/build_story_landing.py` (дизайн и CSS наследуются из `index.html`).

---

## Demo (рекомендуется)

Из корня репозитория:

```bash
pip install -r inference/requirements.txt
python run_demo.py
```

Windows: `start_demo.bat`.

Открыть http://127.0.0.1:8000/ — FastAPI отдаёт `index.html` и API на том же origin.

`setup_demo_models.py` вызывается автоматически при старте `run_demo.py`.

Первый `/analyze` на CPU: ожидайте **503** 30–60 с, пока загрузятся LID + tone + RU/KZ pretrained (~8,5 GB).

### API с другого хоста (статический preview)

```html
<script>window.KAZNLP_API_BASE = 'http://127.0.0.1:8000';</script>
```

---

## Веса моделей

| Модель | Путь |
|--------|------|
| LID v2 | `models/xlm-roberta/xlm-r_v2.pt` или `models/xlm-roberta/lid/xlm-r_v2.pt` |
| Mixed tone v1 | `models/xlm-roberta/tone/tone_v1.pt` или `models/xlm-roberta/tone_v1.pt` |
| RU / KZ tone | `models/tone_pretrained/` — `python scripts/download_tone_pretrained.py` |

---

## Только статика (без API)

```bash
python -m http.server 8877 --directory web
```

- http://127.0.0.1:8877/index.html — лендинг без live inference (demo-кнопки не сработают)
- http://127.0.0.1:8877/story.html — история capstone
