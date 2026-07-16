# Research context: KazNLP (Bogdan Savelyev)

Generated: 2026-07-16  
Sources: `docs/capstone/Final_Report.md`, `STORY.md`, `README.md`  
Note: `main.ipynb` (270 cells) referenced in docs but not present in workspace at scan time.

## Overview

Solo Samsung Innovation Campus capstone. Core claim: auto LID on Kazakhstani social/reviews massively over-labels “mixed”; real code-switching (шала-казахский) must be separated from Kazakh with Russian loanwords before sentiment or corpus stats make sense.

Pipeline: collect → diagnose false mixed → gold LID 3 076 → XLM-R LID v2 → score corpus → tone on mixed 2GIS → demo API.

## Key numbers

| Artifact | Value |
|----------|------:|
| Telegram | 422 141 |
| Gold LID | 3 076 (ru/kz/mixed) |
| XLM-R LID v2 macro-F1 (test n=461) | 96.56% |
| FastText v2 / Lingua v2 on same test | 70.92% / 88.63% |
| Master corpus after LID | 331 468 |
| Model-predicted mixed | 16 364 (not human-audited) |
| Tone gold / Tone v1 acc | 3 529 / 97.33% (mostly LLM labels) |

## Publication angles

1. Document-level LID for kk–ru with loanword vs true switch distinction  
2. Evidence that synthetic/heuristic LID fails on real KZ UGC  
3. Filter-first cascade for code-switched sentiment  
4. Resource paper: gold + weights + labeler (if cleaned for release)

## Naming collision

Nazarbayev University / NLA already published a toolkit named **KazNLP** (Makazhanov, Yessenbayev, Kozhirbayev). Outreach and paper titles should use a distinct name (e.g. “ShalaLID”, “kk-ru SwitchFilter”) or “KazNLP Capstone / Savelyev” to avoid confusion.

## Risks for publication

- Tone metrics largely measure agreement with LLM drafts  
- Corpus mixed not fully audited  
- Solo undergrad/capstone without faculty co-author → workshop + advisor path more realistic than ACL main
