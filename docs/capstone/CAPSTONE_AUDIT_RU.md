> **English version:** [CAPSTONE_AUDIT.md](CAPSTONE_AUDIT.md)

# Аудит KazNLP — Capstone AI Project

**Дата:** 12 июня 2026  
**Эталон:** Samsung Innovation Campus Capstone rubric (100 баллов)  
**Состояние:** проект **завершён** (код + модели + demo); сдача paperwork в процессе

---

## 1. Обязательные артефакты

| # | Требование | Статус | Путь |
|---|------------|--------|------|
| 1 | Action Plan | 🟢 | `docs/capstone/Action_Plan.md` · `Action_Plan.docx` |
| 2 | WBS | 🟡 | `docs/capstone/WBS.csv` на диске · `WBS.xlsx` через `export_capstone_docs.py` |
| 3 | Код / Jupyter | 🟢 | `main.ipynb`, `labeling_service/`, `scripts/` |
| 4 | Данные | 🟢 | gold 3076, корпус 422k+, README |
| 5 | Final Report | 🟢 | `Final_Report.md` · `Final_Report.docx` |
| 6 | Презентация | 🟢 | `docs/capstone/presentation.pptx` (live: `web/story.html`) |
| 7 | Защита | ⏳ | Репетиция + live demo |

---

## 2. Модели и веса (проверено на диске)

| Модель | Файл | Статус |
|--------|------|--------|
| FastText v1/v2 | `models/fasttext/*.bin` | ✅ |
| XLM-R LID v2 | `models/xlm-roberta/xlm-r_v2.pt` | ✅ |
| Mixed Tone v1 | `models/xlm-roberta/tone_v1.pt` | ✅ |
| RU tone pretrained | `models/tone_pretrained/ru_rubert_rureviews/` | ✅ |
| KZ tone pretrained | `models/tone_pretrained/kz_kazakh_sentiment_bert/` | ✅ |

**Inference:** `python run_demo.py` → 4 модели, live `/analyze`.

---

## 3. Метрики (воспроизводимые)

| Задача | Метрика | Источник |
|--------|---------|----------|
| LID XLM-R v2 | macro-F1 **96.56%**, test n=461 | `main.ipynb` executed |
| LID CM v2 | ru 150/150, kz↔mixed 14 err | `main.ipynb` |
| FastText v1 synthetic | F1 **84.96%** | `main.ipynb` гл.1 |
| FastText v2 seeds | P(mixed) **95.51%**, n=868 | `main.ipynb` гл.4 |
| Mixed Tone v1 | acc **97.33%**, CM `[[257,6],[8,254]]` | `scripts/eval_tone_v1.py` · §7.3 |
| Mixed Tone v2 | acc **96.19%** | `scripts/eval_tone_v1.py` |

Сохранено: `data/processed/metrics_tone_test.json`

---

## 4. Оценка по рубрике SIC

| Категория | Макс | Балл | Комментарий |
|-----------|------|-----:|-------------|
| **IDEA** | 10 | **9** | Сильная локальная задача; +1 за related work |
| **APPLICATION** | 30 | **27** | Full stack; −3 за нет corpus audit 100 / Colab |
| **RESULT** | 30 | **26** | Сильные метрики; gold test ladder в `main.ipynb` §10 |
| **PROJECT MANAGEMENT** | 10 | **9** | WBS обновлён, docx/xlsx есть |
| **PRESENTATION & REPORT** | 20 | **17** | Отчёт + `presentation.pptx`; −3 за video/скрины в docx |
| **ИТОГО** | 100 | **87** | FT gold ladder в §10; осталось video + скрины docx |

---

## 5. Оставшиеся пробелы (приоритет)

| P | Задача | Кто |
|---|--------|-----|
| P1 | Demo video 2–5 мин | Автор |
| P1 | Corpus audit 100 mixed | Опционально |
| P2 | Colab inference notebook | Опционально |
| P2 | Скриншоты UI в Final Report.docx | Автор |

---

## 6. Антипаттерны (проверка)

| Антипаттерн | Вердикт |
|-------------|---------|
| «94% accuracy и всё» | ✅ Нет — macro-F1, CM, per-class |
| Сломанный baseline | ✅ FastText реально обучен |
| Туториал под видом проекта | ✅ Свой корпус, gold, labeler |
| API без метрик | ✅ Метрики + eval scripts |
| Fake pretrained как свой train | ✅ RU/KZ явно pretrained |

---

## 7. Команды перед защитой

```bash
python scripts/eval_tone_v1.py          # tone metrics
python scripts/verify_tone_pretrained.py
python run_demo.py                      # warm-up ~60s CPU
python scripts/export_capstone_docs.py  # обновить docx/xlsx
```

**Чеклист дня защиты:** веса на месте · demo прогрет · pptx · ФИО в docx · ответ «mixed vs kz заём» готов.
