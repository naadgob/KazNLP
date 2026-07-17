# Separating real Kazakh–Russian code-switching from loanwords

**A hand-labeled LID benchmark and an XLM-R filter for шала-қазақша in Kazakhstani user text**

Bogdan Savelyev · Samsung Innovation Campus (individual capstone) · bogsav999@gmail.com
Code: [github.com/naadgob/KazNLP](https://github.com/naadgob/KazNLP) · Weights & data: [huggingface.co/datasets/naadgob/kaznlp-weights](https://huggingface.co/datasets/naadgob/kaznlp-weights)

> PDF version: [`KazNLP_onepager.pdf`](KazNLP_onepager.pdf)

## The problem

Off-the-shelf detectors and keyword heuristics call a Kazakh sentence "code-switched" the moment it holds a common Russian loanword. On 241,576 Telegram comments, a narrow Kazakh-plus-Russian heuristic flagged **27,628 as mixed**; reading them by hand, only **460 were genuine code-switching** (about 1.7%). Kazakh written with everyday Russian loanwords swamps the real шала-қазақша, so any corpus count or sentiment number built on automatic LID comes out inflated.

## What I built

A document-level LID setup that treats *mixed* as its own class and gets scored against people, not synthetic text. The gold set has **3,076 messages** (1,077 mixed, 1,000 ru, 999 kz) pulled from Telegram news comments, Kaspi and 2GIS reviews, each labeled by hand. I fine-tuned `xlm-roberta-base` as a three-way filter and put it up against FastText, Lingua, and HeLI/heliport (Tommi Jauhiainen’s loanword strip, then a short windows grid) on the same held-out gold test (n = 461).

| LID model (gold test, n=461) | Macro-F1 | Recall_mixed | Prec_mixed |
|---|--:|--:|--:|
| FastText v2 (real + synthetic) | 70.9% | 49.1% | 65.8% |
| HeLI raw (heliport) | 69.7% | 53.4% | 58.9% |
| HeLI+neutral (strip loanwords → re-ID) | 68.3% | 49.1% | 57.3% |
| HeLI+windows (grid best: 2+3, min1) | 86.9% | 68.9% | 92.5% |
| Lingua v2 (token voting) | 88.6% | 98.8% | 76.8% |
| **XLM-R v2 (fine-tuned filter)** | **96.6%** | **95.0%** | **95.0%** |

> Synthetic data doesn't transfer: a FastText model trained on 480,000 generated "mixed" lines scores **85% F1 on its own synthetic test** but drops to **63% macro-F1 on the real gold set**. Lingua reaches high recall by over-tagging mixed (precision 76.8%). HeLI raw sits with FastText; **HeLI+windows** (grid best: overlapping 2+3-word votes after strip, min_count=1) jumps to **86.9%** macro-F1 with high mixed precision.

## At corpus scale

Run over a **331,468-message** corpus (Telegram, Kaspi, 2GIS across 10+ Kazakhstani cities), the filter keeps **16,364 (4.9%)** as real code-switching. That's roughly an order of magnitude below what the keyword heuristic claimed, which is the point: honest counts change what you can say about the corpus.

## Downstream tone

On the filtered code-switched review slice, a binary tone head (XLM-R) hits **97.3% macro-F1** on a 525-example test. The set is small and the labels were LLM-drafted then audited, so I read it as evidence the filtered data is usable rather than as the headline result.

## What's honest about it

- The 16,364 "mixed" corpus labels are model-predicted; only the 3,076 gold examples are fully hand-checked.
- Tone labels started as LLM drafts and were then audited, so 97% partly measures agreement with that process.
- Solo capstone. The notebook grew across many sessions, so a clean single-pass rerun is still on the to-do list.

## Where I'd like input

Two things I'm unsure about: whether the loanword-vs-switch distinction is framed the way the VarDial / CALCS communities would want, and which venue fits a single-author resource contribution (gold LID set, weights, and the labeling tool) best. Short reactions are welcome; a longer read of the repo is a bonus, not an ask.
