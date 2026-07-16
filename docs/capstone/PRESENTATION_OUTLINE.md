> **Russian version:** [PRESENTATION_OUTLINE_RU.md](PRESENTATION_OUTLINE_RU.md)

# KazNLP — presentation plan and outline (self-contained)

**Narrative source:** `STORY.md`  
**Purpose:** documentary presentation for reading without a speaker  
**Format:** 20 slides · 16:9 · ~40–50 s reading per slide → **15–18 min**  
**Date:** 15.06.2026  
**Author:** Bogdan Savelyev

---

## Plan (how the deck is structured)

### Goal

A reader without access to the author understands: which KZ digital problem the project solves, what was done, why each step was needed, which numbers are proven, where the limits are, and how to reproduce.

### Audience

Future you, a colleague, a report reviewer, jury in async mode. Not live defense: each slide needs enough prose, not headline + three bullets.

### ONE BIG THING

Auto-LID in KZ social media tags almost everything as mixed. KazNLP measured the noise, built gold **3,076**, proved XLM-R v2 **96.56%** macro-F1 on a single gold test, and assembled a filter-first pipeline through demo.

### Story architecture (4 acts)

| Act | Slides | Content | Source in STORY.md |
|-----|--------|------------|---------------------|
| **I — Problem** | 01–05 | KZ world, pain, examples, noise measurement | Part I |
| **II — Dead ends** | 06–09 | synthetic, FT, Lingua, “need gold” conclusion | Chapters 1–4 |
| **III — Proof** | 10–15 | gold, XLM-R, ladder, corpus, caveats | Chapters 5–7 |
| **IV — Product** | 16–20 | tone, cascade, demo, limits, conclusion | Chapters 8–10, III |

### Slide contract (self-contained)

Each slide has four blocks:

1. **Question** — what the reader should understand  
2. **Story** — 2–5 prose sentences on the slide  
3. **Evidence** — number, table, diagram, quote  
4. **Therefore** — one line, bridge to next slide  

### Visual spine

Persistent **chapter rail** on the left: Act I → II → III → IV + slide number. Reader always sees where they are in `main.ipynb` chronology.

### Story guard (forbidden wording)

- “confirmed / honest mixed” for **16,364**
- LID **97%** (round **96.56%** correctly)
- Tone **97.33%** without LLM-label caveat
- “16k human-audited”

### Deliverable (next step after outline)

HTML (rebuild): `python scripts/build_self_deck.py` → `docs/capstone/kaznlp-story-deck-self.html`  
PPTX (SIC): `docs/capstone/presentation.pptx`  
Export pptx: `python scripts/html_deck_to_pptx.py docs/capstone/kaznlp-story-deck-self.html -o docs/capstone/presentation.pptx`  
Live defense: `web/story.html` (`python scripts/build_story_landing.py`)

---

## Outline: 20 slides with text

---

### Slide 01 · Act I · Opening

**Layout:** `splitScene` — prose left, pipeline diagram right  
**Question:** Why a separate LID project in Kazakhstan?

**Story (on slide):**  
In Telegram, on Kaspi, and in 2GIS people write shala-Kazakh: Russian and Kazakh in one message. To count bilingual share or train tone, you first separate ru, kz, and mixed. KazNLP is a “language first, then tone” pipeline on a real **422k+** corpus, not a toy sample.

**Evidence:** diagram `TEXT → LID → ROUTE → TONE`  
**Therefore:** Without accurate LID, any mixed analytics rests on noise.

**Footer:** KazNLP · Bogdan Savelyev · SIC capstone · June 2026

---

### Slide 02 · Act I · Where the problem lives

**Layout:** `ucScene` — data source cards  
**Question:** Lab task or real text?

**Story:**  
Corpus from KZ digital: **422,141** Telegram comments (Telethon), **39,129** Kaspi reviews, 2GIS reviews for tone. Telegram `language` at scrape is FastText v1 — collector label, not ground truth. The project works on what people actually write, not synthetic in a vacuum.

**Evidence:** three sources + row counts  
**Therefore:** The problem scales with data volume.

---

### Slide 03 · Act I · What breaks without a filter

**Layout:** `editorialStack`  
**Question:** Who is hurt by bad LID?

**Story:**  
A researcher adds “mixed” to a sentiment corpus and mixes in kz with Russian loans. An analyst builds language dashboards. A product team sees “mass bilingualism” in comments. Same failure mode: auto-LID confuses code-switch with a loanword in Kazakh grammar. Until the boundary is drawn, numbers and models train on noise.

**Evidence:** short table “role → what breaks”  
**Therefore:** Need a measurable filter, not another heuristic.

---

### Slide 04 · Act I · Class boundary

**Layout:** `compareDuet` — two quote columns  
**Question:** Where is the mixed vs kz line?

**Story:**  
«Курьер молодец, уақытында әкелді» — two language phrases, **mixed**. «Качествосы жақсы, арзан» — Kazakh grammar with Russian loan, **kz**, not code-switch. Naive LID sees Cyrillic and Kazakh letters and often tags mixed on the second example. Those rows drive false hits at corpus scale.

**Evidence:** two quotes side-by-side + ru/kz/mixed labels  
**Therefore:** Task is not “are there Kazakh letters” but “are there switched language phrases.”

---

### Slide 05 · Act I · Pivot — measured noise

**Layout:** `evidenceWall` — 10×10 grid + metrics  
**Question:** How wrong is auto-LID?

**Story:**  
Instead of arguing “everyone is mixed,” the project measured noise. On **27,628** FT-mixed rows, `is_real_mixed()` kept **460** (~**1.66%**). After FT v2 on corpus **66,462** mixed, precision on same heuristic — **2.32%** (1,542/66,462). Heuristic is not gold (misses shala-Kazakh without ә/ң), but noise magnitude is fixed. Of ~100 auto-mixed, real code-switches are single digits.

**Evidence:** 1.66% · 2.32% · 460/27,628 · 1,542/66,462  
**Therefore:** Synthetic and rules won't save without manual gold — what we tried next.

---

### Slide 06 · Act II · Synthetic

**Layout:** `editorialStack`  
**Question:** Why didn't 480k synthetic solve it?

**Story:**  
Start in `main.ipynb` (cells 0–21): Hugging Face KazSAnDRA **180,064** + clapAI ru **164,148**, **480,000** ru/kz/mixed rows with loanword vocabularies, FastText v1. Hold-out **96,000** rows F1 **84.96%**. On paper LID looked solved. Real Telegram showed the opposite: pretty synthetic F1 does not transfer to KZ social media.

**Evidence:** 480k · F1 84.96% · cells 0–21  
**Therefore:** Synthetic is baseline, not production.

---

### Slide 07 · Act II · Real corpus

**Layout:** `timelineStrip`  
**Question:** What happened when Telegram was added?

**Story:**  
Telethon collection from KZ channels (cells 22–44). FastText v1 sets `language` at scrape. Dataset grew: **146,206** → **241,576** → **422,141** on disk. Visual check: almost everything tagged mixed looks like plain ru or kz with a loan. The project's key question appeared here: how much of auto-mixed is real code-switch?

**Evidence:** corpus growth waves  
**Therefore:** Diagnostics first, not transformers immediately.

---

### Slide 08 · Act II · Four dead ends

**Layout:** `timelineStrip`  
**Question:** What was tried before gold and why it stopped?

**Story:**  
**FT v2** (cells 45–64): recall **95.51%** on **868** seeds, but precision **2.32%** on corpus. **Lingua v2**: **95.97%** on seeds; on gold test recall mixed **98.76%**, precision **76.81%** — high recall, low precision is dangerous for filtering. **LLM for gold LID** rejected (high FP on mixed). **YouTube** (~4.7k) not finished. Kaspi **39,129** added a second domain with the same auto-label noise.

**Evidence:** four branches with numbers  
**Therefore:** Need manual gold and a model with full-phrase context.

---

### Slide 09 · Act II · Bridge to solution

**Layout:** `manifesto` — large text on dark background  
**Question:** What replaces rules?

**Story:**  
Shortcuts exhausted: synthetic, retrained FastText, token-level Lingua. Next: gold LID with auditable split protocol and XLM-RoBERTa that sees the full phrase. Principle: filter-first — accurate LID on gold, then corpus scoring, then tone on mixed only.

**Evidence:** BEFORE → PATH → AFTER diagram (from STORY.md)  
**Therefore:** Act III — how gold was built and quality proved.

---

### Slide 10 · Act III · Gold LID

**Layout:** `evidenceWall`  
**Question:** How was gold built?

**Story:**  
Kaspi + Telegram, `cheap_clean`: **388,748** → **254,601** rows. Gold in batches: manual labeling, heuristic-batch (mixed only), Lingua candidate queue. After dedup **3,076** rows: ru **1,000**, kz **999**, mixed **1,077** → `gold_v1.csv`. LLM not used in gold LID.

**Evidence:** bar ru/kz/mixed + 3,076  
**Therefore:** Gold exists; need honest training protocol.

---

### Slide 11 · Act III · Split protocol

**Layout:** `editorialStack`  
**Question:** Why can we trust the metrics?

**Story:**  
Stratified split 80/10/10, `random_state=42`: train **2,691**, val **462**, test **461** (gold-only). **538** synthetic hard patterns train-only. Gold : synthetic weight **3:1**. XLM-R trains on raw **`text`**, not `text_norm`: normalization cuts bilingual signal (~219/1077 mixed lose features). Val and test — gold only.

**Evidence:** split table + two rules (synth train-only, raw text)  
**Therefore:** Can train and compare models on one test.

---

### Slide 12 · Act III · XLM-R LID v2

**Layout:** `evidenceWall` + CM  
**Question:** What result did the model give?

**Story:**  
XLM-RoBERTa-base, Kaggle 2× T4, AdamW lr 2e-5. v1: **95.92%** macro-F1; **v2: 96.56%** on gold test **n = 461**. CM v2: ru **150/150**, kz **142/150**, mixed **153/161**. **14 of 16** errors — kz ↔ mixed, the hardest boundary to label.

**Evidence:** 96.56% + CM + cells 173  
**Therefore:** LID v2 is production model; compare to baselines on same test.

---

### Slide 13 · Act III · Baseline ladder

**Layout:** `ladderArena` — bars + footnote  
**Question:** Why not stop at FastText or Lingua?

**Story:**  
§10 `main.ipynb` (cells 267–268): all LID models on one `test.csv` (**n = 461**). FastText v1 **63.24%** → v2 **70.92%** → Lingua v2 **88.63%** → XLM-R v2 **96.56%** macro-F1. Only XLM-R v2 gives balanced mixed P/R ~**95%**. Lingua v2 catches almost all mixed (recall 98.76%) but precision 76.81% — unsuitable for corpus filter without review.

**Evidence:** ladder bars + footnote “one test.csv”  
**Therefore:** Main scientific result is LID; apply to corpus.

---

### Slide 14 · Act III · 331k corpus

**Layout:** `funnelStage`  
**Question:** What happened on the full pool?

**Story:**  
XLM-R v2 rescored Kaspi+Telegram → `kaspi-telegram_dataset_v2.csv` (**254,652**). Added 2GIS negative/positive. Final assembly in **cell 237**: **`main.csv` — 331,468** (ru **281,409** · kz **33,695** · mixed **16,364**). Intermediate cells 203/221 have stale counts; canonical number is cell 237 only.

**Evidence:** funnel 331,468 → 16,364  
**Therefore:** 16k — next slide explains what that means and what it does not.

---

### Slide 15 · Act III · Qualifier 16k

**Layout:** `editorialStack` + badge «model-predicted»  
**Question:** What does 16,364 mixed NOT mean?

**Story:**  
`main_mixed.csv` — XLM-R v2 predictions, not manual audit. Corpus audit of 100 random mixed from Action Plan not done. Gold test mixed P/R ~**95%** on **n = 461** does not automatically transfer to **16,364** corpus rows. Correct: “filtered 16,364 candidates by LID v2”; incorrect: “confirmed mixed.”

**Evidence:** badge + comparison n=461 vs n=16364  
**Therefore:** Corpus is model application; tone is a separate branch.

---

### Slide 16 · Act IV · Tone stretch

**Layout:** `evidenceWall` — two numbers with task labels  
**Question:** Is tone 97.33% the same as LID 96.56%?

**Story:**  
No. Tone is a separate task on mixed 2GIS reviews. Gold **3,529** (pos **1,771**, neg **1,758**); **~94%** labels from LLM draft (`llm_composer`), manual **217**. Tone v1: **97.33%** on test **n = 525**, CM `[[257,6],[8,254]]`. Metric reflects agreement with LLM labels on hold-out, not independent human validation. v2 worse (**96.19%**), v1 chosen.

**Evidence:** LID 96.56% | Tone 97.33% with eval set labels  
**Therefore:** LID is main result; tone is stretch goal with caveat.

---

### Slide 17 · Act IV · Cascade

**Layout:** `splitScene` — pipeline diagram  
**Question:** How do parts connect in the product?

**Story:**  
Filter-first (`inference/pipeline.py`): raw text → XLM-R LID v2 (ru|kz|mixed) → auto-route. Ru → RuBERT (pretrained). Kz → Kazakh sentiment BERT (pretrained). Mixed → Tone v1 (XLM-R fine-tuned). Mixed tone does not mix with monolingual paths.

**Evidence:** cascade diagram  
**Therefore:** Pipeline left the notebook — demo.

---

### Slide 18 · Act IV · Demo and reproduction

**Layout:** `demoTheater` — screenshot/wireframe + commands  
**Question:** How to verify without the author?

**Story:**  
`python scripts/setup_demo_models.py` → `python run_demo.py` (http://127.0.0.1:8000/). Labeler: `python run_labeler.py`. Tone metrics: `python scripts/eval_tone_v1.py` → `metrics_tone_test.json`. `main.ipynb` (270 cells) does not replay Run All; defense path — cells **45, 173, 237, 268** + scripts. First API request may return 503 for 30–60 s (~8.56 GB model load).

**Evidence:** command block + demo UI link  
**Therefore:** Runs locally; limits on final slide.

---

### Slide 19 · Act IV · Limits

**Layout:** `editorialStack`  
**Question:** Where are the project boundaries?

**Story:**  
Single gold LID annotator; κ not computed. Tone and LID on different domains (Telegram/Kaspi vs 2GIS). **16,364** mixed not corpus-audited. Tone 97.33% is mostly LLM-label agreement. Telethon cells **31, 35, 41, 88** in notebook must not be re-run. Student-scale research with explicit limits — not production NLP.

**Evidence:** four limit points (prose, not bullets-only)  
**Therefore:** Conclusion with three anchor numbers.

---

### Slide 20 · Act IV · Closing

**Layout:** `manifesto`  
**Question:** Main project takeaway?

**Story:**  
Project started with “why does everyone write mixed.” Answer was measuring noise and gold **3,076**, not another architecture for its own sake. Before: auto-LID → analytics and models on noise. After: filter-first pipeline with XLM-R v2 **96.56%** on honest test and local demo.

**Evidence (three anchors):**  
- **~1.66% / 2.32%** — noise diagnostics (heuristic, not prevalence)  
- **96.56%** — LID macro-F1, gold test n=461  
- **97.33%** — tone on mixed 2GIS, n=525, LLM-heavy gold  

**Therefore:** `STORY.md` · `main.ipynb` · `run_demo.py`

---

## Appendix (optional, not in main 20)

| Slide | Content |
|-------|------------|
| A1 | Table of all data sources (422k / 39k / 2GIS / gold) |
| A2 | CRISP-DM timeline 4 weeks |
| A3 | Labeler UI screenshot |
| A4 | Full source table from STORY.md §Data sources |

---

## Slide → STORY.md → main.ipynb mapping

| Slide | STORY.md | main.ipynb |
|-------|----------|------------|
| 01–05 | Part I | — |
| 06 | Chapter 1 | cells 0–21 |
| 07 | Chapter 2 | cells 22–44 |
| 08 | Chapters 3–4 | cells 45–113 |
| 09 | Before/after/path | — |
| 10–11 | Chapter 5 | cells 114–153 |
| 12–13 | Chapter 6, §10 | cells 154–176, 267–268 |
| 14–15 | Chapter 7 | cells 177–237 |
| 16 | Chapter 8 | cells 238–264 |
| 17–18 | Chapter 9 | inference/ |
| 19–20 | Part III | — |

---

## Pre-layout checklist

- [ ] Each slide reads without spoken explanation (has Therefore)
- [ ] All numbers cross-checked with `STORY.md` / disk
- [ ] No story guard violations
- [ ] Chapter rail on all 20 slides
- [ ] At least 5 layout families (no card-grid monotony)
- [ ] Slides 05 and 13 — visual peak
- [ ] Slide 15 required (qualifier 16k)

---

*Related files: `STORY.md` · `docs/capstone/presentation.pptx` · `web/story.html` · `docs/capstone/kaznlp-story-deck-self.html` (optional)*
