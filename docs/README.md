# Документация KazNLP

| Файл | Для кого | Содержание |
|------|----------|------------|
| [`../README.md`](../README.md) | Разработчик / жюри | Структура репо, цифры, quick start |
| [`../STORY.md`](../STORY.md) | Жюри, нарратив | Полная история capstone |
| [`tone_dataset_overview.md`](tone_dataset_overview.md) | ML / разметка | Gold tone, synthetic, QC |
| [`capstone/Final_Report.md`](capstone/Final_Report.md) | Сдача SIC | Финальный отчёт |
| [`capstone/Action_Plan.md`](capstone/Action_Plan.md) | Сдача SIC | Стартовый план |
| [`capstone/WBS.csv`](capstone/WBS.csv) | Сдача SIC | WBS (`.xlsx`: `python scripts/export_capstone_docs.py`) |
| [`capstone/CAPSTONE_AUDIT.md`](capstone/CAPSTONE_AUDIT.md) | Перед защитой | Чеклист рубрики |
| [`capstone/PRESENTATION_OUTLINE.md`](capstone/PRESENTATION_OUTLINE.md) | Презентация | Аутлайн 20 слайдов |
| [`capstone/presentation.pptx`](capstone/presentation.pptx) | Сдача SIC | Единственный pptx для Samsung |
| [`capstone/kaznlp-story-deck-self.html`](capstone/kaznlp-story-deck-self.html) | Презентация | HTML для пересборки pptx (`build_self_deck.py`; может отсутствовать) |

## `docs/capstone/` на диске

```
capstone/
├── Action_Plan.md · Action_Plan.docx
├── Final_Report.md · Final_Report.docx
├── WBS.csv                         # WBS.xlsx → export_capstone_docs.py
├── presentation.pptx               # сдача SIC
├── kaznlp-story-deck-self.html     # опционально, после build_self_deck.py
├── PRESENTATION_OUTLINE.md
└── CAPSTONE_AUDIT.md
```

Live на защите: [`../web/story.html`](../web/story.html) (не заменяет `presentation.pptx` в paperwork).

Веб: [`../web/README.md`](../web/README.md) · Labeler: [`../labeling_service/README.md`](../labeling_service/README.md).
