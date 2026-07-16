# Professor outreach — KazNLP / kk–ru LID + mixed tone

**Author:** Bogdan Savelyev  
**Prepared:** 2026-07-16  
**Goal of wave 1:** get a reply and a short conversation — not a review, not co-authorship on day one.

Emails below are ready to copy. Replace `[GitHub]`, `[HF]`, `[1-pager]` with your real links before sending. Prefer a distinct project name in subject lines (your repo is also called KazNLP; NU already owns that name for a toolkit).

---

## 1. How this actually works

Cold-emailing a famous professor with “please evaluate my research / please publish with me” almost never works. What works for a solo student with a finished capstone:

1. **Soft contact.** One specific paper of theirs + what you built + one small ask (15 min / venue advice / “does this fit VarDial/CALCS?”).
2. **Local or already-kk–ru people first.** Reply rate is higher when the topic sits in their current pipeline (NU, IITU, KRCS authors).
3. **Workshop before journal.** Realistic venues for this work: CALCS (code-switching), VarDial (similar languages / LID), SIGUL / LREC resource track, NAACL/ACL Student Research Workshop, regional AICT-style venues. Main ACL/EMNLP is a later step after an advisor is on board.
4. **You need an academic “sponsor”.** Journals and many workshops expect a faculty affiliation or at least someone who knows the review process. Your real ask over 2–4 emails is: *would you consider advising a short resource/methods paper built on this gold set?*
5. **Name collision.** NU’s open toolkit is already called KazNLP. In email and paper titles, use something else (e.g. ShalaLID / kk-ru SwitchFilter) so you don’t look like you’re claiming their project.

**What you are selling in sentence form:**  
On 422k Telegram + gold 3 076, FastText-style “mixed” is mostly noise (~1–2% true by heuristic audit); XLM-R hits 96.56% macro-F1 on a shared gold test where FT is ~71% and Lingua trades recall for precision. Downstream: filter-first tone on true mixed.

**Honesty that helps you:** admit tone gold is mostly LLM-drafted; lead with LID + gold, not the 97% tone number.

---

## 2. Search strategy (reuse this)

| Lens | Query ideas | Why |
|------|-------------|-----|
| Direct kk–ru | `"Kazakh" "code-switching"`, `kk-ru CSW`, KRCS, Kozhirbayev | Same language pair |
| LID / varieties | VarDial, “language identification” social media, Jauhiainen, Zampieri | Your main scientific claim is LID |
| CS community | CALCS workshop organizers, LinCE, GLUECoS | They care about underrepresented pairs |
| Turkic NLP | TUMLU, Turkic UD, Kazakh BERT, Al-Farabi / NU / IITU faculty | Regional fit |
| Sentiment CS | “code-mixed sentiment”, bilingual reviews | Stretch goal of your pipeline |

**Sources:** ACL Anthology author pages → Google Scholar → faculty page email → recent workshop PC lists (CALCS, VarDial).

**Waves (send in this order):**

| Wave | Who | Cadence |
|------|-----|---------|
| A | KZ / already-kk–ru (Malykh, Kozhirbayev, Yessenbayev, Makazhanov if reachable) | week 1: 4–5 emails |
| B | LID / VarDial (Jauhiainen, Zampieri, Scherrer) | week 1–2 |
| C | Code-switching core (Solorio, Choudhury, Winata, Hamed, Sitaram/Bali) | week 2–3 |
| D | Turkic / low-resource adjacent + broader multilingual | week 3–4 |

Rules: max ~5–8 new emails per week; one polite bump after 10–14 days; stop after two emails with no reply; never mass-CC; never attach a 40-page report in email 1.

**Success metrics:** reply > meeting > “send a draft” > co-author discussion. A single engaged advisor beats twenty polite declines from ACL celebrities.

---

## 3. Relevance tiers (master list)

Score: **A** = write this week · **B** = strong fit · **C** = good secondary · **D** = long-shot / prestige only.

Emails marked `*` are inferred from institutional patterns — verify on the faculty page before send.

### Tier A — highest priority (same problem, reachable)

| # | Name | Affiliation | Focus (why you) | Contact | Score |
|---|------|-------------|-----------------|---------|-------|
| 1 | Valentin Malykh | IITU (Almaty); ITMO; MTS AI | Supervises student work; KRCS kk–ru CS MT (NAACL 2025 SRW) | val@maly.hk · valentin.malykh@phystech.edu | A |
| 2 | Zhanibek Kozhirbayev | Nazarbayev University / NLA | Kazakh NLP, LID, speech; co-author KRCS + historical KazNLP toolkit | zhanibek.kozhirbayev@nu.edu.kz * | A |
| 3 | Zhandos Yessenbayev | NU / NLA (hist.) | KazNLP pipeline, UGC, LID with Kozhirbayev/Makazhanov | check NU / Scholar | A |
| 4 | Aibek Makazhanov | formerly NU NLA; industry NLP | Built KazNLP LID (NB word/char); kk–ru code-switch preprocessing | LinkedIn / aibek.makazhanov@nu.edu.kz * (may be stale) | A |
| 5 | Maksim Borisov | ITMO (student author KRCS) | Peer path into Malykh/Kozhirbayev circle; dataset author | borisovmaksim@niuitmo.ru (from paper) | A |

### Tier B — LID / varieties (scientific home for your paper)

| # | Name | Affiliation | Focus | Contact | Score |
|---|------|-------------|-------|---------|-------|
| 6 | Tommi Jauhiainen | Univ. of Helsinki | Language ID surveys, books, Unseen Languages project | tommi.jauhiainen@helsinki.fi | A/B |
| 7 | Marcos Zampieri | George Mason Univ. | VarDial founder; LID; similar languages; NAACL SRW faculty advisor | mzampier@gmu.edu * · site: mzampieri.com | A/B |
| 8 | Yves Scherrer | Univ. of Oslo (assoc.); Helsinki docent | Closely related varieties, VarDial campaigns, multi-label LID | yves.scherrer@ifi.uio.no * · yves.scherrer@helsinki.fi | B |
| 9 | Timothy Baldwin | MBZUAI (hist. Melbourne) | Co-author *Automatic Language Identification in Texts* | MBZUAI faculty page | B |
| 10 | Krister Lindén | Univ. of Helsinki | Co-author LID book; Language Bank of Finland | Helsinki portal | B |
| 11 | Preslav Nakov | MBZUAI | VarDial co-editor; social media NLP | MBZUAI faculty page | B |
| 12 | Shervin Malmasi | industry / VarDial alum | DSL shared tasks, similar-language ID | Scholar / LinkedIn | C |

### Tier C — code-switching community (prestige + venue access)

| # | Name | Affiliation | Focus | Contact | Score |
|---|------|-------------|-------|---------|-------|
| 13 | Thamar Solorio | MBZUAI (also UH) | CS NLP pioneer; LinCE; CALCS; low-resource + mixed language | thamar.solorio@mbzuai.ac.ae | B |
| 14 | Monojit Choudhury | MBZUAI | CS, multilingual fairness, CALCS; ex-MSR India | monojit.choudhury@mbzuai.ac.ae * | B |
| 15 | Genta Indra Winata | Capital One AI Foundations | CS surveys; CALCS organizer; curated CS paper list | gentaindrawinata@gmail.com | B |
| 16 | Injy Hamed | MBZUAI | Arabic CS surveys; CALCS PC | MBZUAI | B |
| 17 | Sunayana Sitaram | Microsoft Research India | GLUECoS, CS benchmarks, multilingual eval | MSR contact form / Scholar | B/C |
| 18 | Kalika Bali | Microsoft Research India | Low-resource multilingual; CALCS | kalikab@microsoft.com * | B/C |
| 19 | Sudipta Kar | Oracle / CALCS PC | CALCS organizer | ACL / LinkedIn | C |
| 20 | Marina Zhukova | UC Santa Barbara | CALCS organizer | UCSB | C |
| 21 | Derry Tanti Wijaya | Monash Indonesia / BU | CALCS; multilingual | faculty page | C |
| 22 | Mona Diab | (check current) | Historical CALCS / CS workshops | Scholar | C |
| 23 | Barbara Bullock / A.J. Toribio | UT Austin (ling) | Linguistic CS theory; ACL survey co-authors | UT faculty pages | C |
| 24 | A. Seza Doğruöz | Ghent Univ. | CS survey (ACL 2021) with Sitaram et al. | Ghent | C |

### Tier D — Turkic / Central Asia / adjacent

| # | Name | Affiliation | Focus | Contact | Score |
|---|------|-------------|-------|---------|-------|
| 25 | Nilufar Abdurakhmonova | National Univ. of Uzbekistan | Turkic NLP, corpora, Turklang | NUU faculty page | B |
| 26 | Botir Elov | Tashkent State Univ. of Uzbek Language & Literature | Uzbek CL, sentiment, morphology | ORCID / faculty | C |
| 27 | Arofat Akhundjanova | (CL researcher) | Turkic UD, TUMLU benchmark | LinkedIn | C |
| 28 | Ilnar Salimzyanov | (Kazakh/Tatar resources) | Turkic linguistic resources | Scholar | C |
| 29 | Faculty @ Al-Farabi KazNU | Almaty | Historical Kazakh corpora (cited in KRCS) | kaznu.kz departments | B |
| 30 | Faculty @ KBTU / Satbayev / SDU | Almaty region | Applied NLP / student supervision | department sites | B |
| 31 | NU School of Engineering & Digital Sciences NLP faculty | Astana | Broader CS home if NLA path stalls | nu.edu.kz | B |

### Tier E — multilingual / low-resource (weaker topical fit, useful later)

| # | Name | Affiliation | Notes | Score |
|---|------|-------------|-------|-------|
| 32 | Graham Neubig | CMU | Low-resource MT/NLP; busy | D |
| 33 | David Adelani | (check) | Multilingual African NLP; CS panels | C/D |
| 34 | Alham Fikri Aji | MBZUAI | Multilingual; CS survey co-author | C |
| 35 | Zheng Xin Yong | (CS survey co-author) | CALCS ecosystem | C |
| 36 | Antonios Anastasopoulos | GMU | Works with Zampieri; multilingual | C |
| 37 | Barbara Plank | LMU / ITU | Multilingual NLP | D |
| 38 | Isabelle Augenstein | Copenhagen | Multilingual / social | D |
| 39 | Ivan Vulić | Cambridge | Multilingual representations | D |
| 40 | Anna Korhonen | Cambridge | Multilingual | D |
| 41 | Sebastian Ruder | industry | Multilingual surveys | D |
| 42 | Pascale Fung | HKUST / Meta | Multilingual dialogue | D |
| 43 | Nizar Habash | NYU Abu Dhabi | Dialectal Arabic; CS survey co-author | C |
| 44 | Ngoc Thang Vu | Stuttgart | Multilingual / CS (Arabic survey) | C |
| 45 | Caroline Sabty | (Arabic CS) | Survey co-author | C |

**Expand further:** scrape CALCS 2025 PC + VarDial 2025 PC + authors citing Kozhirbayev 2018 LID paper + authors of TUMLU (ACL 2025). That alone can push the list past 80 names; keep them in a spreadsheet with columns: name, email, paper cited, wave, status, date sent.

---

## 4. Personalized emails (wave A–C)

Tone: short, specific, human. English for international faculty; Russian OK for Malykh/Borisov if you prefer.

### 4.1 Valentin Malykh — send first

**Subject:** kk–ru document-level LID gold (related to KRCS)

```
Dear Professor Malykh,

I read your NAACL 2025 SRW paper with Borisov and Kozhirbayev on Kazakh–Russian code-switched MT and the KRCS eval set. I’m writing because I’ve been working on the step that sits just before translation for the same language pair: telling apart true code-switching from Kazakh with Russian loanwords in noisy social text.

I’m Bogdan Savelyev (Samsung Innovation Campus capstone, solo). On ~422k Telegram comments, FastText-style “mixed” labels are mostly false; after a hand-labeled gold set of 3,076 ru/kz/mixed examples, XLM-RoBERTa reaches 96.56% macro-F1 on a held-out gold test (n=461), against ~71% for FastText and ~89% for Lingua on the same split. I also built a small filter-first tone cascade for mixed 2GIS reviews.

I’m not asking you to review a draft yet. If you have 15 minutes in the next couple of weeks, I’d value your sense of whether a short resource/methods paper on this LID gold would be useful next to KRCS — and which venue you’d aim at first.

Links: [GitHub] · [HF weights/dataset] · [1-page PDF]

Best regards,
Bogdan Savelyev
[city] · [Telegram/email] · [LinkedIn optional]
```

### 4.2 Zhanibek Kozhirbayev

**Subject:** Document-level kk–ru LID on UGC (after your KazNLP / KRCS line of work)

```
Dear Dr. Kozhirbayev,

Your work on Kazakh–Russian language identification for noisy user text (with Yessenbayev and Makazhanov) and the recent KRCS paper are the closest published lines I’ve found to a problem I hit while building a capstone system on Kazakhstani Telegram and reviews.

I’m Bogdan Savelyev. I collected a 3,076-example gold set for document-level ru / kz / mixed, with guidelines that treat loanword-only Kazakh as kz rather than mixed. On that gold test, transformer LID clearly beats the FastText/Lingua baselines we tried; applying the model to a larger pool changes how much “mixed” you think is in the wild compared with auto-labels at scrape time.

I know the NU toolkit is already named KazNLP — my student project reused that name by accident, so I’d rebrand for any paper. I’m reaching out to ask whether a short conversation about fit (resource note vs methods, and a sensible venue) would be welcome. Happy to send a one-pager first if that’s easier.

[GitHub] · [1-pager]

Thank you for your time,
Bogdan Savelyev
```

### 4.3 Maksim Borisov (peer / warm intro path)

**Subject:** Your KRCS dataset — adjacent LID gold for kk–ru social text

```
Hi Maksim,

I saw your NAACL SRW paper on kk–ru code-switched MT and the KRCS set. Congrats — that eval set is exactly the kind of thing the pair was missing.

I finished a solo SIC capstone on a neighboring problem: document-level LID that separates real switches from Kazakh+loanwords, with a 3k+ gold set and a public pipeline. I’m trying to find someone in the KRCS orbit who might tell me if a short paper on that gold would complement what you already released.

If you’re open to a quick chat (or a pointer to who on the team prefers such emails), I’d appreciate it. Not asking for co-authorship out of the blue.

Bogdan Savelyev
[links]
```

### 4.4 Tommi Jauhiainen

**Subject:** Gold eval for kk–ru social LID (loanwords vs code-switching)

```
Dear Dr. Jauhiainen,

I’ve been using your surveys and the Automatic Language Identification in Texts line of work as the map for a student project on Kazakh–Russian user-generated text.

The practical failure mode I measured is false “mixed” labels: scrapers and n-gram LID treat Russian loanwords inside Kazakh sentences as code-switching. I built a 3,076-example gold set with that distinction written into the guidelines, and compared FastText, Lingua, and XLM-R on one shared test split (XLM-R ~96.6% macro-F1).

I’m at the stage of figuring out whether this belongs near VarDial / LID evaluation work or closer to code-switching workshops. If a short email exchange or a 15-minute call is possible, I’d be grateful for your take on framing — I’m not asking you to read a full paper yet.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
[links]
```

### 4.5 Marcos Zampieri

**Subject:** VarDial-shaped question: kk–ru LID with a loanword vs switch gold set

```
Dear Professor Zampieri,

I’m writing because of your VarDial work and the LID / language-variety evaluation papers (including the true-labels LID work with Jauhiainen et al.). I have a finished student project on a messy bilingual case that sits between “similar languages” and code-switching: Russian and Kazakh in Telegram and reviews, where loanword-heavy Kazakh gets labeled mixed by off-the-shelf LID.

Artifact in one line: 3,076 gold documents, shared test ladder (FastText / Lingua / XLM-R), and a filter-first cascade before sentiment. I’d like advice on whether a short paper belongs at VarDial, a code-switching workshop, or a resource track — and I’m happy to keep the first conversation at that level of detail.

Bogdan Savelyev
[affiliation as student / SIC] · [links]
```

### 4.6 Thamar Solorio

**Subject:** Underrepresented CS pair: kk–ru document LID gold

```
Dear Professor Solorio,

LinCE and your long line of code-switching workshops made it obvious that most CS benchmarks still skip Central Asian pairs. I built a solo capstone dataset and models for document-level Kazakh–Russian LID on real social text, with annotation guidelines aimed at the loanword-vs-switch confusion that breaks naive mixed labels.

Numbers if useful: gold n=3,076; XLM-R macro-F1 96.56% on gold test n=461; large scraped pool where auto-“mixed” was mostly noise. Tone on mixed reviews exists as a second stage, but the LID gold is the part I’d defend first.

I’m looking for guidance on whether this is CALCS-shaped, and whether a brief call would be appropriate. I am not asking you to join as co-author in this email — only whether the problem is worth a conversation.

Respectfully,
Bogdan Savelyev
[links]
```

### 4.7 Monojit Choudhury

**Subject:** kk–ru social LID — false “mixed” at scale

```
Dear Professor Choudhury,

Your code-mixing / multilingual inclusion work (including the CALCS community and papers on how models mishandle linguistic diversity) is why I’m writing. In Kazakhstani Telegram, automatic LID paints almost everything as mixed; when I measured it, the true switch rate under a stricter definition was tiny compared with the auto label rate.

I’ve put together a gold set and a transformer baseline for ru/kz/mixed under that stricter definition, then used it to rescore a larger corpus. If you’re open to a short note on whether this is a useful data point for the CS community — or who among your students/collaborators looks at Turkic–Russian mixing — I’d appreciate a pointer.

Bogdan Savelyev
[links · city]
```

### 4.8 Genta Winata

**Subject:** Adding kk–ru to the CS map (document LID gold)

```
Hi Genta,

I’ve used your code-switching survey and the github paper list while finishing a capstone on Kazakh–Russian mixed social text. Most CS LID/sentiment work still doesn’t cover this pair; I have a 3k+ document-level gold set that separates true switches from loanword Kazakh, plus a simple XLM-R baseline and a public demo pipeline.

If you have a minute: does this sound more like CALCS material or VarDial-style LID? A one-line opinion already helps. Happy to send a one-pager.

Bogdan
[links]
```

### 4.9 Sunayana Sitaram / Kalika Bali (MSR — slightly more formal)

**Subject:** Resource question: kk–ru code-switch LID gold (social domain)

```
Dear Dr. Sitaram,

I’m a student who finished an individual NLP capstone on Kazakh–Russian document-level language ID for noisy social text. GLUECoS and your code-switching evaluation work are the benchmark style I had in mind, for a pair that still rarely appears in those suites.

I have a manually labeled gold set (3,076) with guidelines for loanwords vs switches, and shared-split comparisons against FastText and Lingua. I’m writing to ask whether MSR’s multilingual/CS group ever looks at Turkic–Russian mixing, and whether a short conversation or a referral would be appropriate. No request for internship paperwork in this email — only fit.

Thank you,
Bogdan Savelyev
[links]
```

(For Bali: swap name; mention low-resource / inclusive multilingual tech instead of GLUECoS.)

### 4.10 Yves Scherrer

**Subject:** Multi-signal LID: Kazakh with Russian loans vs true mixed documents

```
Dear Professor Scherrer,

Your VarDial and closely-related-variety work (including multi-label Scandinavian LID) resonates with a labeling problem I hit on Kazakh–Russian UGC: many documents aren’t cleanly one language, but “mixed” in scraper labels is also wrong when the only Russian material is a loanword inside Kazakh morphosyntax.

I built a three-way gold set and baselines for that distinction. I’d welcome advice on how the VarDial community prefers such cases to be framed (variety ID vs code-switching vs multi-label LID). A short reply is plenty.

Bogdan Savelyev
[links]
```

### 4.11 Zhandos Yessenbayev / Aibek Makazhanov (shared template)

**Subject:** Following your KazNLP LID work — new gold for loanword vs switch

```
Dear Dr. [Yessenbayev/Makazhanov],

I learned the NU KazNLP pipeline’s LID component (document- and word-level kk/ru/other on noisy UGC) while working on a related student project. My focus is a stricter document-level mixed class: true code-switching versus Kazakh sentences that only contain Russian loans — a distinction that still breaks FastText-style labeling on Telegram-scale data.

I’ve released (or can share) a 3,076-example gold set and XLM-R baselines. I’d like to ask whether anyone from the original KazNLP line is still advising students on this topic, and whether a brief conversation would be welcome. I’ll use a different project name in any paper to avoid clashing with your toolkit.

Bogdan Savelyev
[links]
```

### 4.12 Injy Hamed (shorter)

**Subject:** Non-Arabic CS pair seeking CALCS-facing advice

```
Dear Dr. Hamed,

I saw your code-switched Arabic NLP survey and CALCS organizing work. I’m a student with a finished gold set for Kazakh–Russian document LID (loanword vs true switch) and I’m trying to learn whether CALCS is open to underrepresented pairs presented as resource/short papers.

If you can spare a short reply on fit — or redirect me to the right PC — I’d be grateful.

Bogdan Savelyev
[links]
```

---

## 5. One-pager checklist (attach or link)

Keep to a single PDF page:

- Problem: false mixed on kk–ru UGC (one example pair of sentences)
- Gold: 3 076, guideline one-liner, split sizes
- Ladder table: FT / Lingua / XLM-R on same test
- What you will *not* overclaim (tone LLM labels; 16k mixed not audited)
- Ask: conversation about venue + possible advising
- Links + email

---

## 6. Tracking sheet (copy to Sheets)

| name | email | wave | date_sent | bump_date | reply | next_step | notes |
|------|-------|------|-----------|-----------|-------|-----------|-------|
| Malykh | val@maly.hk | A | | | | | KRCS advisor |
| Kozhirbayev | … | A | | | | | NU |
| … | | | | | | | |

Statuses: `queued` · `sent` · `bumped` · `replied` · `call_booked` · `closed_no` · `closed_yes`

---

## 7. Pre-mortem (so you don’t waste months)

| Failure mode | Guardrail |
|--------------|-----------|
| Silence from everyone | Wave A volume first; use LinkedIn only after email; ask Borisov for intro |
| Someone says “publish on arXiv alone” | Fine as step 1; still need faculty for peer-reviewed venue |
| Reviewer kills tone section | Lead with LID; demote tone to appendix / future work |
| Name clash with NU KazNLP | Rename before any preprint |
| You ask for co-authorship in email 1 | Don’t; earn a second email |

---

## 8. What “help with publication” looks like in practice

After a positive reply, a normal sequence is:

1. They skim the one-pager → suggest venue + missing baseline/related work  
2. You rewrite as a 4–8 page workshop paper  
3. They decide whether to join as advisor/co-author (affiliation, last-author pattern varies by lab)  
4. Submit to workshop deadline; iterate on reviews  

If nobody replies in 3–4 weeks: put a clean preprint on arXiv under a new name, cite Kozhirbayev/KRCS/Jauhiainen properly, then email again with “here’s the preprint, still looking for advising feedback.” Preprints make you look serious; they don’t replace peer review.
