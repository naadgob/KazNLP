# Research context: KazNLP (Bogdan Savelyev)

Generated: 2026-07-17 (numbers reconciled against `main.ipynb`; HeLI/heliport + windows grid best 2026-07-17)  
Sources: `main.ipynb` (274 cells, authoritative), `docs/capstone/Final_Report.md`, `STORY.md`, `README.md`  
Per-notebook deep dive lives in `.notebook-context/main.md`.

## Overview

Solo Samsung Innovation Campus capstone. Core claim: auto LID on Kazakhstani social/reviews massively over-labels “mixed”; real code-switching (шала-казахский) must be separated from Kazakh with Russian loanwords before sentiment or corpus stats make sense.

Pipeline: collect → diagnose false mixed → gold LID 3,076 → baselines (FastText, Lingua, HeLI raw/neutral/windows-grid, char-3gram NB) → XLM-R LID v2 → score corpus → tone on code-switched slice → demo API.

## Key numbers

| Artifact | Value |
|----------|------:|
| Telegram raw collected | 411,746 |
| Kaspi+Telegram merged / dedup / cleaned | 461,270 / 388,748 / 254,601 |
| Gold LID | 3,076 (mixed 1077 / ru 1000 / kz 999); split 2691/461/462 |
| XLM-R LID v2 macro-F1 (test n=461) | 96.56% (acc 96.53%) |
| FastText v2 / HeLI+windows / Char-3gram NB / Lingua v2 | 70.92% / 86.92% / 88.00% / 88.63% macro-F1 |
| Char-3gram NB (§10.2, char 3-gram + Laplace NB) | 88.00% macro-F1; mixed recall 0.708 (misses switch boundary) |
| HeLI+neutral / HeLI+windows (grid best 2+3, min1) | 68.26% / 86.92% macro-F1; best windows flips 69/80 residual mixed-as-rus |
| Heuristic over-labeling | 27,628 tagged mixed, 460 real (~1.7%) |
| Master corpus after LID | 331,468 (ru 281409 / kz 33695 / mixed 16364) |
| Model-predicted mixed | 16,364 (~4.9%, not human-audited) |
| Tone gold / v1 test acc | 3,503 audited + 882 synth / 97.33% (n=525) |

## Publication angles

1. Document-level LID for kk–ru with loanword vs true switch distinction  
2. Evidence that synthetic/heuristic LID fails on real KZ UGC  
3. Filter-first cascade for code-switched sentiment  
4. Resource paper: gold + weights + labeler (if cleaned for release)

## Naming collision

Nazarbayev University / NLA already published a toolkit named **KazNLP** (Makazhanov, Yessenbayev, Kozhirbayev). Outreach and paper titles should use a distinct name (e.g. “ShalaLID”, “kk-ru SwitchFilter”) or “KazNLP Capstone / Savelyev” to avoid confusion.

## Risks for publication

- Tone labels LLM-assisted then audited; 97% partly measures agreement with the labeling process  
- Corpus mixed (16,364) model-predicted, not fully audited  
- Notebook has many <UNRUN> cells (outputs kept across sessions, not one clean run) — reproducibility caveat  
- Solo undergrad/capstone without faculty co-author → workshop + advisor path more realistic than ACL main
