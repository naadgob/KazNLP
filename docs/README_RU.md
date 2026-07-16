> **English version:** [README.md](README.md)

# Документация KazNLP

| Файл | Для кого | Содержание |
|------|----------|------------|
| [`../README_RU.md`](../README_RU.md) | Разработчик / жюри | Структура репо, цифры, quick start |
| [`../STORY_RU.md`](../STORY_RU.md) | Жюри, нарратив | Полная история capstone |
| [`tone_dataset_overview.md`](tone_dataset_overview.md) | ML / разметка | Gold tone, synthetic, QC |
| [`capstone/Final_Report_RU.md`](capstone/Final_Report_RU.md) | Сдача SIC | Финальный отчёт |
| [`capstone/Action_Plan_RU.md`](capstone/Action_Plan_RU.md) | Сдача SIC | Стартовый план |
| [`capstone/WBS.csv`](capstone/WBS.csv) | Сдача SIC | WBS (`.xlsx`: `python scripts/export_capstone_docs.py`) |
| [`capstone/CAPSTONE_AUDIT_RU.md`](capstone/CAPSTONE_AUDIT_RU.md) | Перед защитой | Чеклист рубрики |
| [`capstone/PRESENTATION_OUTLINE_RU.md`](capstone/PRESENTATION_OUTLINE_RU.md) | Презентация | Аутлайн 20 слайдов |
| [`capstone/presentation.pptx`](capstone/presentation.pptx) | Сдача SIC | Единственный pptx для Samsung |
| [`capstone/kaznlp-story-deck-self.html`](capstone/kaznlp-story-deck-self.html) | Презентация | HTML для пересборки pptx (`build_self_deck.py`; может отсутствовать) |

## `docs/capstone/` на диске

```
capstone/
├── Action_Plan.md · Action_Plan_RU.md · Action_Plan.docx
├── Final_Report.md · Final_Report_RU.md · Final_Report.docx
├── WBS.csv                         # WBS.xlsx → export_capstone_docs.py
├── presentation.pptx               # сдача SIC
├── kaznlp-story-deck-self.html     # опционально, после build_self_deck.py
├── PRESENTATION_OUTLINE.md · PRESENTATION_OUTLINE_RU.md
└── CAPSTONE_AUDIT.md · CAPSTONE_AUDIT_RU.md
```

Live на защите: [`../web/story.html`](../web/story.html) (не заменяет `presentation.pptx` в paperwork).

Веб: [`../web/README_RU.md`](../web/README_RU.md) · Labeler: [`../labeling_service/README_RU.md`](../labeling_service/README_RU.md).
