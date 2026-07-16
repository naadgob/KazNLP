> **Russian version:** [README_RU.md](README_RU.md)

# KazNLP documentation

| File | Audience | Content |
|------|----------|---------|
| [`../README.md`](../README.md) | Developer / jury | Repo layout, numbers, quick start |
| [`../STORY.md`](../STORY.md) | Jury, narrative | Full capstone story |
| [`tone_dataset_overview.md`](tone_dataset_overview.md) | ML / labeling | Gold tone, synthetic, QC |
| [`capstone/Final_Report.md`](capstone/Final_Report.md) | SIC hand-in | Final report |
| [`capstone/Action_Plan.md`](capstone/Action_Plan.md) | SIC hand-in | Kickoff plan |
| [`capstone/WBS.csv`](capstone/WBS.csv) | SIC hand-in | WBS (`.xlsx`: `python scripts/export_capstone_docs.py`) |
| [`capstone/CAPSTONE_AUDIT.md`](capstone/CAPSTONE_AUDIT.md) | Pre-defense | Rubric checklist |
| [`capstone/PRESENTATION_OUTLINE.md`](capstone/PRESENTATION_OUTLINE.md) | Presentation | 20-slide outline |
| [`capstone/presentation.pptx`](capstone/presentation.pptx) | SIC hand-in | Only pptx for Samsung |
| [`capstone/kaznlp-story-deck-self.html`](capstone/kaznlp-story-deck-self.html) | Presentation | HTML to rebuild pptx (`build_self_deck.py`; may be missing) |

## `docs/capstone/` on disk

```
capstone/
├── Action_Plan.md · Action_Plan_RU.md · Action_Plan.docx
├── Final_Report.md · Final_Report_RU.md · Final_Report.docx
├── WBS.csv                         # WBS.xlsx → export_capstone_docs.py
├── presentation.pptx               # SIC hand-in
├── kaznlp-story-deck-self.html     # optional, after build_self_deck.py
├── PRESENTATION_OUTLINE.md · PRESENTATION_OUTLINE_RU.md
└── CAPSTONE_AUDIT.md · CAPSTONE_AUDIT_RU.md
```

Live defense: [`../web/story.html`](../web/story.html) (does not replace `presentation.pptx` in paperwork).

Web: [`../web/README.md`](../web/README.md) · Labeler: [`../labeling_service/README.md`](../labeling_service/README.md).
