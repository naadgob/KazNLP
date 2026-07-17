# Professor outreach — KazNLP / kk–ru LID + mixed tone

**Author:** Bogdan Savelyev  
**Prepared:** 2026-07-16  
**Goal of wave 1:** get a reply and a short conversation — not a review, not co-authorship on day one.

Emails below are ready to copy. Links are already filled: repo `https://github.com/naadgob/KazNLP`, weights & data `https://huggingface.co/datasets/naadgob/kaznlp-weights`. One-pager now exists: `docs/outreach/onepager/KazNLP_onepager.pdf` (source `.html`/`.md` alongside) — attach it or send on request. Prefer a distinct project name in subject lines (your repo is also called KazNLP; NU already owns that name for a toolkit).

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

## 3b. Expanded candidate list — Wave 4 (queued, found 2026-07-16)

New names from mining CALCS/VarDial committees, Turkic NLP (TUMLU, KyrgyzNLP, Kazakh UD), Kazakhstan faculty, and GLUECoS/LinCE/SentiMix. None overlap with people already emailed. Confidence = email reliability.

### A+ — Kazakh–Russian code-switching / Kazakh LID (send first)

| Name | Affiliation | Why | Email | Conf |
|------|-------------|-----|-------|------|
| Daniil Orel | MBZUAI | Qorǵau — kk–ru **code-switched** safety benchmark | daniil.orel@mbzuai.ac.ae | high |
| Aigerim Aitim | IITU | Kazakh corpus; explicitly cites kk–ru CS detection | a.aitim@iitu.edu.kz | high |
| Diana Turmakhan | MBZUAI | Qorǵau / KazMMLU (kk+ru) | diana.turmakhan@mbzuai.ac.ae | high |
| Maiya Goloburda | MBZUAI | Qorǵau kk–ru code-switched prompts | maiya.goloburda@mbzuai.ac.ae | med |
| Nurkhan Laiyk | MBZUAI | Qorǵau kk–ru | nurkhan.laiyk@mbzuai.ac.ae | med |
| Bakhtiyor Meraliyev | SDU | Kazakh–Russian BERT on social media | bakhtiyor.meraliyev@sdu.edu.kz | low |

### Kazakh NLP resources / LLMs (NU · ISSAI · MBZUAI)

| Name | Affiliation | Why | Email | Conf |
|------|-------------|-----|-------|------|
| Rustem Yeshpanov | NU / ISSAI | KazNERD, KazSAnDRA, KazParC | rustem.yeshpanov@nu.edu.kz | high |
| Adai Shomanov | NU SEDS | Kazakh QA/RAG | adai.shomanov@nu.edu.kz | high |
| Zhenisbek Assylbekov | Purdue Fort Wayne | Kazakh embeddings/morphology | zassylbe@pfw.edu | high |
| Rustem Takhanov | NU | Kazakh LM theory | rustem.takhanov@nu.edu.kz | high |
| Maxat Tezekbayev | NU | Kazakh LM | maxat.tezekbayev@nu.edu.kz | high |
| Arman Bolatov | NU | Kazakh NLP | arman.bolatov@nu.edu.kz | high |
| Artur Pak | NU | Kazakh LM | artur.pak@nu.edu.kz | high |
| Yerbolat Khassanov | ISSAI/NU | KSC, KazNERD, Turkic ASR/LID | yerbolat.khassanov@nu.edu.kz | med |
| Mukhammed Togmanov | MBZUAI | KazMMLU lead | mukhammed.togmanov@mbzuai.ac.ae | high |
| Nurdaulet Mukhituly | MBZUAI | KazMMLU / Sherkala | nurdaulet.mukhituly@mbzuai.ac.ae | high |
| Fajri Koto | MBZUAI (faculty) | Sherkala PI, KazMMLU | fajri.koto@mbzuai.ac.ae | med |

### KazNU / Almaty MT & corpora

| Name | Affiliation | Why | Email | Conf |
|------|-------------|-----|-------|------|
| Madina Mansurova | KazNU | Kazakh pipeline, morphology | mansurova.madina@gmail.com | high |
| Diana Rakhimova | KazNU / IICT | kk–ru MT, low-resource Turkic | diana.rakhimova@kaznu.kz | high |
| Ualsher Tukeyev | KazNU | Kazakh/Turkic MT, morphology | ualsher.tukeyev@gmail.com | high |
| Zhandos Zhumanov | KazNU | Kazakh parallel corpora | z.zhake@gmail.com | high |
| Iskander Akhmetov | KBTU / IICT | Kazakh NLP, summarization | iskander.akhmetov@gmail.com | high |
| Ryskhan Satybaldiyeva | Satbayev | Kazakh processing, semantic search | r.satybaldiyeva@satbayev.university | high |
| Nurgali Kadyrbek | KazNU | Kazakh dependency | nurgali.kadyrbek@kaznu.kz | low |
| Vladislav Karyukin | KazNU | kk–en/ru NMT (w/ Malykh) | vladislav.karyukin@kaznu.kz | low |
| Rustam Mussabayev | IICT Almaty | NLP lab head | rustam@iict.kz | low |
| Nazerke Sultanova | SDU | Kazakh DNN LM | nazerke.sultanova@sdu.edu.kz | low |
| Saule Belginova | Turan Univ | TUMLU author (KZ) | saule.belginova@turan-edu.kz | low |
| Saida Mussakhojayeva | ISSAI | KazakhTTS2, KSC2 | saida.mussakhojayeva@nu.edu.kz | low |

### Turkic NLP (Uzbek · Azerbaijani · Kyrgyz · TUMLU)

| Name | Affiliation | Why | Email | Conf |
|------|-------------|-----|-------|------|
| Jafar Isbarov | GWU / aLLMA Lab | TUMLU lead (9 Turkic incl. Kazakh) | jafar.isbarov@gwu.edu | high |
| Abdullatif Köksal | LMU / DeepMind | TUMLU / TurkishMMLU | akoksal@cis.lmu.de | high |
| Samir Rustamov | ADA University | TUMLU advisor | srustamov@ada.edu.az | high |
| Mammad Hajili | Microsoft | TUMLU Azerbaijani | mammadhajili@microsoft.com | high |
| Osman Tursun | QUT | Uyghur NLP, TUMLU | osman.tursun@qut.edu.au | high |
| Elvin Mammadov | BHOS | Azerbaijani foundation models | elvin.mammadov.std@bhos.edu.az | high |
| Kavsar Huseynova | BHOS / aLLMA | TUMLU | kavsar.huseynova.std@bhos.edu.az | med |
| Anar Rzayev | ISTA | TUMLU, multilingual benchmarks | anar.rzayev@ist.ac.at | med |
| Duygu Ataman | NYU / METU | SIGTURK organizer, TUMLU advisor | ataman@nyu.edu | med |
| Elmurod Kuriyozov | Urgench / A Coruña | Uzbek sentiment/NER, Turkic embeddings | e.kuriyozov@udc.es | high |
| Anton Alekseev | Steklov / SPbU | KyrgyzNLP lead, Kyrgyz LID | anton.m.alexeyev@gmail.com | high |
| Timur Turatali | KSTU | KyrgyzNLP | timur.turat@gmail.com | high |
| Alexander Panchenko | Skoltech / AIRI | multilingual low-resource | panchenko.alexander@gmail.com | med |
| Oleg Serikov | AIRI / HSE | Turkic minority langs | oleg.serikov@airi.net | low |
| Ulugbek Salaev | Urgench | Uzbek transliteration | ulugbek.salaev@udc.es | low |

### Turkic UD / morphology

| Name | Affiliation | Why | Email | Conf |
|------|-------------|-----|-------|------|
| Jonathan North Washington | Swarthmore | Kazakh UD treebank | jwashin1@swarthmore.edu | high |
| Francis M. Tyers | Indiana Univ. | Kazakh UD treebank | ftyers@iu.edu | high |

### LID / VarDial / dialects

| Name | Affiliation | Why | Email | Conf |
|------|-------------|-----|-------|------|
| Igor Sterner | Cambridge | token-level code-switching LID | is473@cam.ac.uk | high |
| Çağrı Çöltekin | Tübingen | VarDial organizer, Turkic UD | ccoltekin@sfs.uni-tuebingen.de | high |
| Sina Ahmadi | UZH | low-resource LID | sina.ahmadi@uzh.ch | high |
| Verena Blaschke | LMU | dialect NLP | verena.blaschke@cis.lmu.de | high |
| Aarohi Srivastava | Notre Dame | DialectBench | asrivas2@nd.edu | high |
| David Chiang | Notre Dame | dialect robustness | dchiang@nd.edu | high |
| Jonathan Dunn | Illinois | LID at scale + CS | jedunn@illinois.edu | high |
| Radu Tudor Ionescu | Bucharest | dialect identification | radu.ionescu@fmi.unibuc.ro | high |
| Rob van der Goot | ITU Copenhagen | non-standard NLP, VarDial | robv@itu.dk | high |
| Anjali Kantharuban | CMU | dialect gap MT/ASR | anjaliruban@cmu.edu | high |
| Tanja Samardžić | IDSIA | dialects, VarDial | tanja.samardzic@supsi.ch | high |
| Fahim Faisal | GMU | DialectBench lead | ffaisal@gmu.edu | high |
| Orevaoghene Ahia | UW | DialectBench | oahia@cs.washington.edu | high |
| Kabir Ahuja | UW | multilingual eval | kahuja@cs.washington.edu | high |
| Noëmi Aepli | UZH / UPenn | dialect LID, VarDial | naepli@cl.uzh.ch | med |

### Code-switching community (CALCS)

| Name | Affiliation | Why | Email | Conf |
|------|-------------|-----|-------|------|
| Garry Kuwanto | Boston Univ. | CALCS organizer | gkuwanto@bu.edu | high |
| Mahardika Krisna Ihsani | MBZUAI | CALCS organizer | mahardika.ihsani@mbzuai.ac.ae | high |
| Ruochen Zhang | Brown | multilingual CS | ruochen_zhang@brown.edu | high |
| Maite Heredia | UPV/EHU | Basque–Spanish CS | maite.heredia@ehu.eus | high |
| Jeremy Barnes | UPV/EHU | CS/LID under-resourced | jeremy.barnes@ehu.eus | high |
| Aitor Soroa | UPV/EHU | multilingual LID | a.soroa@ehu.eus | high |
| Naiara Perez | UPV/EHU | Basque low-resource | naiara.perez@ehu.eus | high |
| Chris Emezue | Mila / Lanfrica | Yoruba–English CS ASR | chris.emezue@lanfrica.com | high |
| Olga Kellert | ASU | Spanish–Guaraní CS LID | olga.kellert@asu.edu | med |
| Xi Ai | NUS | CALCS organizer | barid.x.ai@gmail.com | med |
| Begoña Altuna | UEU | Basque NLP | begona.altuna@ueu.eus | med |

### GLUECoS / LinCE / code-mixed sentiment

| Name | Affiliation | Why | Email | Conf |
|------|-------------|-----|-------|------|
| Simran Khanuja | CMU | GLUECoS lead | skhanuja@andrew.cmu.edu | high |
| Shuguang Chen | Univ. of Houston | LinCE contact; CALCS shared tasks | schen52@uh.edu | high |
| Parth Patwa | Amazon (MS UCLA) | SemEval SentiMix organizer | parthpatwa@g.ucla.edu | high |
| Soumitra Ghosh | IIT BHU | Hinglish sentiment+emotion | ghosh.soumitra2@gmail.com | high |
| Sandipan Dandapat | Microsoft | GLUECoS | sadandap@microsoft.com | high |
| Tanuja Ganu | MSR India | GLUECoS | tanuja.ganu@microsoft.com | high |
| Anirudh Srinivasan | UT Austin | GLUECoS | anirudhsriniv@gmail.com | high |
| Gustavo Aguilar | Amazon | LinCE lead (UH addr may be stale) | gaguilaralas@uh.edu | med |
| Amitava Das | BITS Pilani Goa | code-mixed LID/sentiment pioneer | amitava.das@goa.bits-pilani.ac.in | med |

**Not contactable yet (no verified email):** Aida Kasieva, Gulira Jumalieva (Kyrgyz), Ayrat Gatiatullin (Tatar). **Dropped as low-fit/spammy:** 4 LyngualLabs junior co-authors, LLM-robustness pair (Upadhayay/Behzadan).

**SENT 2026-07-16 (wave 4a, 36):** all of A+ (Orel, Aitim, Turmakhan, Goloburda, Laiyk, Meraliyev); Kazakh LLM (Yeshpanov, Shomanov, Assylbekov, Takhanov, Khassanov, Togmanov, Mukhituly, Koto); KazNU/Almaty (Mansurova, Rakhimova, Tukeyev, Zhumanov, Akhmetov, Satybaldiyeva, Kadyrbek, Karyukin, Mussabayev, Sultanova, Belginova, Mussakhojayeva); Turkic (Isbarov, Köksal, Rustamov, Ataman, Kuriyozov, Alekseev, Panchenko, Serikov); Turkic UD (Washington, Tyers). Bump date 2026-07-30.

**~~DEFERRED to wave 4b/4c~~ SENT 2026-07-17 (wave 4b, 45).** Bump date 2026-07-31. All of LID/VarDial (15): Sterner, Çöltekin, Ahmadi, Blaschke, Srivastava, Chiang, Dunn, Ionescu, van der Goot, Kantharuban, Samardžić, Faisal, Ahia, Ahuja, Aepli. CALCS community (11): Kuwanto, Ihsani, Zhang, Heredia, Barnes, Soroa, Perez, Emezue, Kellert, Xi Ai, Altuna. GLUECoS/LinCE/sentiment (9): Khanuja, Chen, Patwa, Ghosh, Dandapat, Ganu, Srinivasan, Aguilar, Das. Turkic/low-resource juniors (10): Tezekbayev, Bolatov, Pak, Salaev, Turatali, Hajili, Huseynova, Mammadov, Rzayev, Tursun. Emails were concise + per-person hook (group templates for LID/CALCS/GLUECoS/juniors).

---

## 3c. US faculty — Wave 5 (SENT 2026-07-16, 58)

All US-based professors, two templates: NLP/method variant and linguist (borrowing-vs-switch) variant. Bump date 2026-07-30.

### NLP / method / comp-sociolinguistics (34)

| Name | University | Email |
|------|-----------|-------|
| Gina-Anne Levow | UW | levow@uw.edu |
| David Yarowsky | JHU | yarowsky@jhu.edu |
| Mans Hulden | CU Boulder | mhulden@colorado.edu |
| David Jurgens | Michigan | jurgens@umich.edu |
| Yulia Tsvetkov | UW | yuliats@cs.washington.edu |
| Julia Hirschberg | Columbia | julia@cs.columbia.edu |
| David Mortensen | CMU | dmortens@cs.cmu.edu |
| Katharina Kann | CU Boulder | katharina.kann@colorado.edu |
| Rada Mihalcea | Michigan | mihalcea@umich.edu |
| Steven Bethard | Arizona | bethard@arizona.edu |
| Alexis Palmer | CU Boulder | alexis.palmer@colorado.edu |
| Heng Ji | UIUC | hengji@illinois.edu |
| Wei Xu | Georgia Tech | wei.xu@cc.gatech.edu |
| Alan Ritter | Georgia Tech | alan.ritter@cc.gatech.edu |
| Marine Carpuat | UMD | marine@cs.umd.edu |
| Nanyun Peng | UCLA | violetpeng@cs.ucla.edu |
| Kevin Duh | JHU | kevinduh@cs.jhu.edu |
| Mark Dredze | JHU | mdredze@cs.jhu.edu |
| Brendan O'Connor | UMass Amherst | brenocon@cs.umass.edu |
| David Bamman | UC Berkeley | dbamman@berkeley.edu |
| Mihai Surdeanu | Arizona | msurdeanu@arizona.edu |
| Micha Elsner | Ohio State | elsner.14@osu.edu |
| Nathan Schneider | Georgetown | nathan.schneider@georgetown.edu |
| Amir Zeldes | Georgetown | amir.zeldes@georgetown.edu |
| Ndapa Nakashole | UCSD | nnakashole@ucsd.edu |
| Lori Levin | CMU | lsl@cs.cmu.edu |
| Kyle Gorman | CUNY | kgorman@gc.cuny.edu |
| Diyi Yang | Stanford | diyiy@cs.stanford.edu |
| Jonathan May | USC/ISI | jonmay@isi.edu |
| Kyle Mahowald | UT Austin | mahowald@utexas.edu |
| Junyi Jessy Li | UT Austin | jessy@austin.utexas.edu |
| Ellie Pavlick | Brown | epavlick@cs.brown.edu |
| Dan Jurafsky | Stanford | jurafsky@stanford.edu |
| Fei Xia | UW | fxia@uw.edu |

### Code-switching / language-contact linguists (24)

| Name | University | Email |
|------|-----------|-------|
| Rena Torres Cacoullos | Penn State | rena@psu.edu |
| Constantine Lignos | Brandeis | lignos@brandeis.edu |
| Paola Dussias | Penn State | pdussias@psu.edu |
| Jorge Valdés Kroff | Florida | jvaldeskroff@ufl.edu |
| Melinda Fricke | Pittsburgh | melinda.fricke@pitt.edu |
| Naomi Shin | New Mexico | naomishin@unm.edu |
| Phillip Carter | FIU | pmcarter@fiu.edu |
| Ana Maria Carvalho | Arizona | anac@arizona.edu |
| Kendra Dickinson | Rutgers | kendra.dickinson@rutgers.edu |
| Silvina Montrul | UIUC | montrul@illinois.edu |
| Rakesh Bhatt | UIUC | rbhatt@illinois.edu |
| Kim Potowski | UIC | kimpotow@uic.edu |
| Jennifer Cabrelli | UIC | cabrelli@uic.edu |
| Jennifer Austin | Rutgers–Newark | jenaustin@newark.rutgers.edu |
| Patrícia Amaral | Indiana | pamaral@indiana.edu |
| Mark Amengual | UC Santa Cruz | amengual@ucsc.edu |
| Ariel Chan | UC Santa Cruz | arielchan@ucsc.edu |
| Josefina Bittar Prieto | UC Santa Cruz | jbittarp@ucsc.edu |
| Agustina Carando | UC Davis | acarando@ucdavis.edu |
| Gabriela Alfaraz | Michigan State | alfarazg@msu.edu |
| Meagan Driver | Michigan State | driverme@msu.edu |
| Lauren Schmidt | SDSU | lbschmidt@sdsu.edu |
| Anna Babel | Ohio State | babel.6@osu.edu |
| Marlyse Baptista | UPenn | marlyse.baptista@sas.upenn.edu |

**Held (low-confidence inferred addresses, verify before send):** Rodrigo Delgado, Salvatore Callesano, Liliana Sánchez, Luis López, Silvia Perez-Cortes, Ricardo Otheguy.

---

## 3d. Replies log (2026-07-16)

**Substantive replies (answered):**
- **Monojit Choudhury** — no longer in code-mixing; cc'd Prashant Kodali (IIIT/Microsoft). Replied to the thread, addressed Kodali. Awaiting Kodali.
- **Kyle Gorman (CUNY)** — suggested an LID workshop or SIGWRIT (writing systems in NLP; sigwrit.org — had a Kazakh-writing paper). Replied with the Cyrillic-shared-script angle (script, not just lexicon, drives the false "mixed"). Offered a one-pager. Warm, open.
- **Nilufar Abdurakhmonova** — brief "thank you"; replied offering a one-pager + asking about regional Turkic venues.
- **Constantine Lignos (Brandeis)** — behind on email; handed the thread to his former student Elena Álvarez-Mellado (borrowing-detection corpus co-author, now faculty), cc'ing her. Replied 2026-07-16 thanking him and inviting Elena's input; offered annotation guide + one-pager. NOTE: mail tool doesn't expose Cc, so Elena wasn't reply-all'd — respond directly once she writes, or get her address to loop in.
- **Barbara Bullock (UT Austin, emerita)** — endorsed the approach as sound; compared it to Diab & Kamboj on annotator disagreement over Hindi-vs-English tokens (attached W11-3407.pdf); referred me to **Nikolay Hakimov** (Bamberg, Russian speaker, Russian–German code-mixing). Replied 2026-07-16 engaging the annotator-boundary parallel and thanking her. Retired, so no advisor path, but a strong warm referral.
  - **Nikolay Hakimov** (nikolay.hakimov@uni-bamberg.de) — cold email sent 2026-07-16 on Bullock's referral, tied to his usage-based/frequency work on code-mixing. NEW lead, awaiting reply.
- **Anton Alekseev (KyrgyzNLP)** — very substantive. Corrected me (no Kyrgyz LID specifically; KyrgyzNLP = survey arXiv 2411.05503 + bib kyrgyznlp.github.io). Pointers: Baisa & Suchomel (char-trigram Turkic web corpora), OpenLID, **KyrText** (Kyrgyz web data contaminated with Kazakh — direct parallel), Odagiri (ky–ru switch vs borrowing, linguistic). Advice: frame as language-contact-aware dataset + eval; annotation policy > XLM-R score; add a smoothed char-trigram LM baseline; venues VarDial/CALCS, ACL short possible with agreement analysis, LRE journal for fuller resource. Replied 2026-07-16 owning the LID correction, committing to the trigram baseline, adopting the framing. DONE char-trigram baseline (main.ipynb §10.2: char 3-gram + Laplace NB, 88.00% macro-F1, mixed recall 70.8% on gold n=461). TODO: read KyrText + Odagiri.
- **Micha Elsner (OSU)** — substantive. Flagged "tone" (thought lexical tone; confirmed = sentiment). Slightly misread sentiment stage as 3 gated systems (it's one binary head on mixed only). Pointers: Arabizi non-standard-script papers, Indic Latin-script LID — wants comparison with script-mismatch CS literature. Same solo-annotation caveat as Anton; suggests code-mixing venue over resource. Replied 2026-07-16: confirmed sentiment, corrected the pipeline, drew the shared-Cyrillic vs Arabizi-Latin contrast, will position against those papers. TODO: read Arabizi + Indic-Latin LID, rename "tone" → sentiment in writeup.

**New replies 2026-07-17 (answered):**
- **Jonathan Washington (Swarthmore, Kazakh UD)** — engaged, substantive. Read my rule as "Kazakh morphology = loanword" and flagged two gaps: (1) bare Russian nouns with no Kazakh morphology; (2) some "loanword" calls would read as switching to speakers → false positives. Supervises a **Kyrgyz–Russian** CS project (same boundary problem). Asked how I used the Kazakh UD treebank; suggested **Apertium Kazakh analyser+disambiguator** (>90%). Replied: clarified labels are document-level (established/integrated borrowing → kz; productive/clause-level → mixed), owned the bare-noun gray zone and the solo-annotation/no-IAA weakness, admitted I did NOT use UD as training data (background only), committed to trying Apertium for the morphology cue + char-trigram baseline, pointed his student to KyrText + Odagiri (via Anton), accepted his offer of a call. **Warmest lead so far — potential advisor + cross-project (ky–ru) link.**
- **Jonathan Dunn (Illinois)** — brief, handed me to PhD student **Gunjan** (cc'd; India related-languages disentangling). Replied: cc not exposed by the send tool, so asked him to forward / share Gunjan's address; framed kk–ru as the same disentangling minus the script cue; asked about OpenLID vs character-level. TODO: write Gunjan directly once I have her email.
- **Tommi Jauhiainen (Helsinki, LID survey author)** — very substantive; asked for class counts + test-split size, and made the key scoping point: core LID is out of VarDial scope, but the "Russian loanwords counted as Kazakh" angle makes it VarDial-suitable; otherwise closer to code-switching workshops. No LID-only workshop exists. Advice: submit to whichever deadline opens first, resubmit elsewhere if rejected. Offered to keep a running email thread. Replied 2026-07-17: gave the 3-way counts (mixed 1077 / ru 1000 / kz 999, test n=461), confirmed the loanword-as-Kazakh framing, noted 2026 editions closed so targeting next cycle with IAA + char-trigram, asked how he handles loanword-bearing segments when cleaning Russian from Cyrillic data. Sent a follow-up clarification separating the two datasets: (1) LID gold 3,076 → language-ID filter, XLM-R 96.6 macro-F1 on n=461; (2) sentiment gold 3,503 audited (1754 neg / 1749 pos) + 882 synth → separate tone model that runs only on the code-switched slice (test n=525, ~97.3). Framed the project as a filter-first cascade (LID first, sentiment downstream on the mixed slice only). 3rd msg from Tommi: explained HeLI-OTS word-list backoff; proposed a neutral shared-loanword list (score 100%-identical kk/ru borrowings neutral, re-identify residual) but noted it "doesn't directly solve real code-switching detection" — i.e. NOT a rejection, he's flagging the limit of lexical LID, which is exactly what the doc-level gold targets. Replied 2026-07-17: accepted the loanword-list idea as a transparent non-neural baseline (buildable from FastText error analysis), drew the border (lexical word-list vs document switch label = complementary, not competing), asked whether HeLI-OTS can expose the neutral-list re-ID step callable from Python. 4th msg from Tommi: pointed to heliport (ZJaume Rust/Python port); re-ID = strip loanword list and re-run. Replied 2026-07-17: will wire heliport as non-neural baseline (loanword list from FastText errors → strip → re-run vs XLM-R on n=461); will send numbers; soft ask for sanity-check on list construction. TODO: heliport baseline + loanword list. **DONE 2026-07-17:** `scripts/heli_lid.py`, `heli_loanwords_v1.txt`, §10.3 — HeLI raw 69.73% / HeLI+neutral 68.26% macro-F1 on n=461 (did not beat raw; residual mixed-as-rus=80). Tommi replied "Sounds good, let me know how it goes." Sent metrics email 2026-07-17 with full ladder + residuals + list size (1494) + repo link (pushed `7058fb1`); asked him to sanity-check list construction. 5th msg from Tommi: asked whether mixed should output majority lang or "mixed"; reframed 80/161 residual rus as possibly good if mixed docs are Russian-heavy; proposed overlapping 2-/3-word (longer) subsentence windows through heliport with multi-lang → mixed (cf. HeLI language-set ID, Springer 2015 https://link.springer.com/chapter/10.1007/978-3-319-18111-0_48). Replied 2026-07-17: clarified gold is doc-level switch≠majority; accepted windowed HeLI as next baseline; will report new F1 + how many of the 80 flip; asked preferred window/threshold if he has one. **DONE HeLI+windows 2026-07-17:** sizes 2/3/4 stride 1 after strip → macro-F1 **86.92%** (acc 87.20%, R_mixed 68.94%, P_mixed 92.50%); residual flip **69/80** (min_count=2: 61/80, F1 84.4%). 6th msg from Tommi: do grid-search on window params (he won't guess; Bogdan knows switch lengths). Draft reply ready with first-pass numbers + commit to small grid table. TODO: light grid (sizes × min_count) → send table. **DONE grid 2026-07-17:** best = sizes **(2,3)** min_count=1 → macro-F1 **86.92%** (tied with 2+3+4/+5); flip 69/80. **SENT grid results 2026-07-17** (msg 19f70308f572f082): full grid summary + best config + honest "strip alone doesn't help"; floated a short workshop/resource note on kk–ru doc LID (loanword vs switch, HeLI window ladder as interpretable rung) and offered him a sanity-check on a future draft — soft, no co-author/supervision ask yet. Next: error pass on 11 non-flipping residuals + missed mixed; escalate advising/co-author only if he bites. **Tommi reply 2026-07-17 (msg 19f70377):** "Indeed this interests me" but guarding his time (windowed language-set ID is below other todos); offered to read the draft once it's ready. Soft yes + boundary → deliver a finished note, don't pile on. Error pass DONE: all 11 non-flip = single-word Kazakh insertions or 2-word Kazakh spans heliport reads as kir/ukr → no kaz window fires; adding size-1 windows → 88.52% macro-F1 but P(mixed) 0.925→0.880. Draft reply staged in chat (not sent). **Strong ongoing email lead; highest-influence LID contact.**

**Elena Álvarez Mellado (borrowing-detection corpus, via Constantine Lignos) 2026-07-17:** replied warm (msg 19f7038e) — agrees lone borrowings are improperly tagged as CS, wants annotation guide + summary + kk-ru implementation. **SENT reply 19f7049e:** framing + gold/XLM-R numbers, offered guide + one-pager, asked how she'd handle token-span vs document-level loanword-vs-switch call. New substantive lead on the borrowing-vs-CS boundary.
- **Nikola Ljubešić (JSI/Ljubljana)** — short, endorsed VarDial; advised: define dataset with labeled CS vs loanword examples, then test which model discriminates (fastText maybe, XLM-R for sure). Replied 2026-07-17: confirmed I did exactly that (distinction in the guidelines), his model guess matched (XLM-R 96.6 vs fastText 71), noted the hard part was label definition not model capacity; asked whether JANES/CLASSLA annotate the switch at token vs document level. Replied from nljubesi@gmail.com (not the JSI address).
- **Maite Heredia (UPV/EHU, Basque–Spanish CS)** 2026-07-17 (msg 19f705a5) — warm; CALCS is a good thematic fit; last edition took 4-page short / 8-page long, non-archival allowed; she's not organizing, doesn't know next-edition date, points to Genta Winata (already contacted). **SENT reply 19f70636:** thanked, said non-archival matters (feedback without blocking a fuller paper), noted I already wrote Genta, asked whether Basque–Spanish was annotated token- vs message-level and whether lone Spanish borrowings caused the same false-mixed problem. Offered one-pager.
- **Rob van der Goot (ITU Copenhagen, VarDial)** 2026-07-17 (msg 19f6fde0) — lukewarm "ok fit"; flagged kk/ru are languages not dialects → check with VarDial organizers. **SENT reply 19f70637:** agreed, noted it matches Tommi's scoping (plain kk/ru = LID, out of scope; the loanword-as-Kazakh confusability is the narrower VarDial-shaped angle); will check with organizers before assuming fit.
- **Jonathan Dunn (Illinois)** 2026-07-17 (msg 19f704cd) — gave Gunjan's address (gunjana2@illinois.edu) + "character-level worked best." **SENT thanks 19f70638.** **Gunjan (gunjana2@illinois.edu) — cold email SENT 19f7063a** via Dunn intro: same disentangling minus script cue, gold/XLM-R numbers, char-trigram baseline ask; asked her borrowing-vs-switch level (token/doc) + OpenLID vs character-level. NEW lead, awaiting reply.

**Bounced / bad address (fix before re-send):** naepli@cl.uzh.ch (Noëmi Aepli — "naepli wasn't found at cl.uzh.ch"; try naepli@ifi.uio.no or her current page), ayu@stei.itb.ac.id (Purwarianti — "ayu wasn't found"; the STEI listing address is dead, needs another route). Several googlemail delivery-failure notices also arrived from the 2026-07-17 blast — not yet triaged per-address.

**Recurring reviewer signal (4 independent people now — add Washington):** annotation policy separating borrowing from code-switching is the real contribution; XLM-R score is secondary; solo annotation = no inter-annotator agreement is the main weakness; VarDial / CALCS are the natural venues.

**Auto-replies / out-of-office (no action; bump after they return):** Dan Jurafsky, Melinda Fricke, Isabelle Augenstein, Marlyse Baptista (away), Meagan Driver, Marine Carpuat (travel until Jul 16), Yves Scherrer, Barbara Plank.

---

## 3e. Wave 6 — global additions (found & verified 2026-07-17)

**SENT 2026-07-17 (all 15).** Bump date 2026-07-31. Batch 1: Çetinoğlu, Poplack, Ljubešić, Burchell, Kargaran, Purwarianti (ayu@stei.itb.ac.id, verified), Sakti, Nguyen. Batch 2: Eryiğit, Oflazer, Zaghouani, Wintner, Haizhou Li, Kondrak, Kunchukuttan.

15 new experts NOT in any earlier wave, chosen for regional spread since the US list (Wave 5) is already saturated. Countries covered: Germany, Canada, Slovenia, UK, Netherlands, Indonesia, Japan, Turkey, Qatar, Israel, China/Singapore, India. Every affiliation + email below was checked against the person's own institutional page or a paper of theirs on 2026-07-17. Emails marked `verify` still need a manual check. Each person has a personalized email tied to their specific work.

### Batch 1 (verified 2026-07-17)

| Name | Region | Affiliation | Why (their work) | Email | Conf |
|------|--------|-------------|------------------|-------|------|
| Özlem Çetinoğlu | Germany | IMS, Univ. Stuttgart | Turkish–German code-switching corpus + SAGT CS treebank; parsing non-canonical/CS text | ozlem@ims.uni-stuttgart.de | high |
| Shana Poplack | Canada | Univ. of Ottawa | Founder of the borrowing-vs-code-switching distinction (Nonce Borrowing Hypothesis); your annotation rule is her theory | spoplack@uottawa.ca | high |
| Nikola Ljubešić | Slovenia | Jožef Stefan Institute / Univ. Ljubljana | LID + tools for non-standard internet text in closely related Slavic langs (JANES, CLASSLA, ReLDI); Russian is one of your two | nikola.ljubesic@ijs.si | high |
| Laurie Burchell | UK | Common Crawl / Univ. of Edinburgh | OpenLID (200-lang LID) + CommonLID (shows LID evals overestimate accuracy on web data) | laurie.burchell@ed.ac.uk | high |
| Amir Hossein Kargaran | Germany | LMU Munich (CIS) | GlotLID (2000+ language fastText LID); the exact tool that mislabels kk/ru | amir@cis.lmu.de | high |
| Ayu Purwarianti | Indonesia | Institut Teknologi Bandung | IndoRobusta code-mixing robustness; IndoNLU; SEA code-mixing with heavy borrowing | ayu@stei.itb.ac.id | high |
| Sakriani Sakti | Japan | JAIST / NAIST; SIGUL chair | Machine speech chain for Indonesian–English code-switching ASR/TTS; leads SIGUL under-resourced SIG | ssakti@jaist.ac.jp | high |
| Dong Nguyen | Netherlands | Utrecht University | Computational Sociolinguistics survey (w/ Doğruöz); multilingualism + social media; VarDial | d.p.nguyen@uu.nl | high |

### Emails (personalized, ready to copy)

**Özlem Çetinoğlu — Subject: kk–ru code-switching gold, from a neighbor of your Turkish–German work**

```
Dear Dr. Çetinoğlu,

Your SAGT Turkish–German treebank and your "Challenges of computational processing of code-switching" are why I'm writing from the Kazakh–Russian side. I hit the problem you know well, one Turkic language in heavy contact, except my noise comes from Kazakh that only carries Russian loanwords, which off-the-shelf LID reads as "mixed".

I built a document-level gold set (3,076 ru/kz/mixed) with a guideline that treats loanword-only Kazakh as Kazakh, not a switch. A fine-tuned XLM-R reaches ~96.6% macro-F1 on a held-out gold test, against ~71% FastText and ~89% Lingua. On a ~331k-message corpus the real switch rate lands near 5%, far below what keyword heuristics claimed.

I'd value your read on whether my document-level loanword-vs-switch call is compatible with how SAGT marked switch points, and where a resource like this fits (VarDial, CALCS). Happy to send a one-page summary.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Shana Poplack — Subject: Operationalizing the borrowing / code-switching line for Kazakh–Russian**

```
Dear Professor Poplack,

Your distinction between borrowing and code-switching, and the nonce borrowing work, is the theory behind a project I just finished, so I wanted to write to you directly.

In Kazakhstani social media, Kazakh sentences carry a lot of Russian loanwords. Automatic language detectors treat any Russian material as a switch, so they label almost everything "mixed". I wrote an annotation guideline that does what your work argues for: a Kazakh sentence with only Russian loanwords counts as Kazakh, and only genuine switching counts as mixed. I hand-labeled 3,076 messages that way, and when a model trained on them re-scores a 331,000-message corpus, real switching drops to about 5%, roughly a tenth of what the naive method claimed.

I'd be grateful for your view on whether my document-level operationalization stays faithful to the borrowing-vs-switching distinction, and where it oversimplifies. I can send a one-page summary if useful.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Nikola Ljubešić — Subject: LID on non-standard kk–ru social text (borrowing vs switch)**

```
Dear Dr. Ljubešić,

Your JANES and CLASSLA work on LID and non-standard internet text for closely related Slavic languages is close to my setting: Kazakh and Russian mixed in noisy social media, where Russian is one of the two languages.

My problem is that Kazakh with Russian loanwords looks identical to real code-switching at the character level, so fastText-style LID calls almost everything "mixed". I built a document-level gold set (3,076 ru/kz/mixed) whose guideline treats loanword-only Kazakh as Kazakh; XLM-R hits ~96.6% macro-F1 on a held-out gold test (vs ~71% FastText, ~89% Lingua), and on a ~331k corpus the true switch rate is near 5%.

I'd value your advice on how you separated genuine mixing from loanword noise in JANES-style data, and whether VarDial is the right home for this. One-pager available.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Laurie Burchell — Subject: A mixed class for kk–ru, and CommonLID-style overestimation**

```
Dear Dr. Burchell,

Your CommonLID finding, that existing LID evaluations overestimate accuracy on real web data, matched my experience exactly for Kazakh, Russian, and their mix. OpenLID covers kk and ru as monolingual labels, but the case that broke everything for me is the third one: Kazakh carrying Russian loanwords, which reads as "mixed" to fastText even though it isn't a switch.

I hand-labeled 3,076 messages under a guideline that keeps loanword-only Kazakh as kz, and only tags genuine switching as mixed. XLM-R gets ~96.6% macro-F1 on a held-out gold test where FastText sits near 71%. On a ~331k corpus the real switch rate is about 5%, versus the ~1.7% precision of a keyword heuristic that flagged 27,628 messages as mixed.

Would a document-level mixed class fit into an OpenLID-style pipeline, and how would you benchmark it fairly? Happy to share data and a one-pager.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Amir Hossein Kargaran — Subject: GlotLID on Kazakh–Russian: the false "mixed" case**

```
Dear Amir,

GlotLID is the kind of model my project stress-tests. It labels Kazakh and Russian well on their own, but Kazakh social text is full of Russian loanwords, and a Cyrillic-on-Cyrillic pair gives a character n-gram model no script signal to lean on, so genuine code-switching and loanword-only Kazakh look the same.

I hand-labeled 3,076 messages (ru/kz/mixed) with a guideline that treats loanword-only Kazakh as Kazakh, and fine-tuned XLM-R to ~96.6% macro-F1 on a held-out gold test (fastText ~71%, Lingua ~89%). A reviewer suggested I add a smoothed character-trigram baseline, which is where your fastText experience would help me most.

Do you think GlotLID-style models can be pushed to separate borrowing from switching for a contact pair like this, or is that inherently a document-level job? One-pager available.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Ayu Purwarianti — Subject: Borrowing vs code-switching for kk–ru (echoes IndoRobusta)**

```
Dear Professor Purwarianti,

Your IndoRobusta work on code-mixing robustness is the closest thing I found to my problem, one border and one language family over. Indonesian mixes with English and local languages and carries plenty of borrowing; Kazakh does the same with Russian, and that borrowing is exactly what makes automatic LID call everything "mixed".

I built a document-level Kazakh–Russian gold set (3,076 ru/kz/mixed) whose guideline treats loanword-only Kazakh as Kazakh, not a switch. XLM-R reaches ~96.6% macro-F1 on a held-out gold test (vs ~71% fastText, ~89% Lingua); applied to ~331k messages, real switching is near 5%.

I'd value your view on how you separate borrowing from genuine mixing in Indonesian, and whether a code-mixing or resource venue fits this best. Happy to send a one-pager.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Sakriani Sakti — Subject: kk–ru text LID before code-switch processing (SIGUL fit?)**

```
Dear Professor Sakti,

Your machine speech chain work on Indonesian–English code-switching, and your role leading SIGUL, are why I'm writing. My project sits on the text side, one step before CS processing: deciding whether a Kazakh–Russian message is genuinely code-switched or just Kazakh with Russian loanwords, which is where automatic LID falls apart.

I hand-labeled 3,076 messages (ru/kz/mixed) under a guideline that keeps loanword-only Kazakh as Kazakh; XLM-R reaches ~96.6% macro-F1 on a held-out gold test, and on a ~331k corpus the true switch rate is near 5%. It's released as a gold set plus weights.

Two questions: would SIGUL (or LT4All) be a reasonable home for a kk–ru gold LID resource, and does the loanword-vs-switch split matter for CS speech pipelines like yours? One-pager available.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Dong Nguyen — Subject: A computational-sociolinguistics take on kk–ru borrowing vs switching**

```
Dear Dr. Nguyen,

Your Computational Sociolinguistics survey, and its multilingualism section, framed how I think about a project I just finished. It's a sociolinguistic distinction turned into a labeling task: on Kazakhstani social media, Kazakh carries many Russian loanwords, and automatic LID reads that as code-switching, so it over-counts mixing badly.

I hand-labeled 3,076 messages (ru/kz/mixed) with a guideline that treats loanword-only Kazakh as Kazakh and only tags genuine switching as mixed. A fine-tuned XLM-R reaches ~96.6% macro-F1 on a held-out gold test; re-scoring a ~331k corpus drops real switching to about 5%, roughly a tenth of the heuristic estimate.

I'd value your view on framing this as computational sociolinguistics rather than plain LID, and where the survey's multilingualism thread points for a venue. Happy to send a one-pager.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

### Batch 2 — more regions (verified 2026-07-17)

| Name | Region | Affiliation | Why (their work) | Email | Conf |
|------|--------|-------------|------------------|-------|------|
| Gülşen Eryiğit | Turkey | Istanbul Technical Univ. | ITU Turkish NLP pipeline; social media text normalization for Turkish; Turkic langs (Uyghur, Turkmen) | gulsen.cebiroglu@itu.edu.tr | high |
| Kemal Oflazer | Turkey/USA | CMU (LTI) | Foundational Turkish computational morphology; MT into morphologically rich langs | ko@cs.cmu.edu | high |
| Wajdi Zaghouani | Qatar | Northwestern Univ. in Qatar | North-African Arabizi treebank with word-level code-switching labels; MADAR; Arabic social media | wajdi.zaghouani@northwestern.edu | high |
| Shuly Wintner | Israel | Univ. of Haifa | Arabizi CS dataset; "Shared Lexical Items as Triggers of Code-Switching" (the "Shared" word tag) | shuly@cs.haifa.ac.il | high |
| Haizhou Li | China/Singapore | CUHK-Shenzhen / NUS | SEAME Mandarin–English code-switching corpus; language-boundary detection & LID | haizhouli@cuhk.edu.cn | high |
| Grzegorz Kondrak | Canada | Univ. of Alberta | Character-level NLP, transliteration, cognates, cipher language identification | gkondrak@ualberta.ca | high |
| Anoop Kunchukuttan | India | Microsoft India / AI4Bharat | Related-languages NLP, transliteration, code-mixing, IndicNLP toolkit | anoop.kunchukuttan@gmail.com | high |

**Gülşen Eryiğit — Subject: kk–ru LID before normalization, from the Kazakh side of Turkic NLP**

```
Dear Prof. Eryiğit,

Your ITU Turkish NLP pipeline and your work on social media text normalization for Turkish are close to a problem I just worked on for Kazakh. Before any normalization, my noisy Kazakhstani text needs a language call, and that call breaks: Kazakh sentences carry so many Russian loanwords that automatic LID tags them "mixed" even when no switching happened.

I hand-labeled 3,076 messages (ru/kz/mixed) under a guideline that keeps loanword-only Kazakh as Kazakh, and only tags genuine switching as mixed. XLM-R reaches ~96.6% macro-F1 on a held-out gold test (fastText ~71%, Lingua ~89%); on a ~331k corpus real switching is near 5%.

Since your pipeline already handles Turkic social text, I'd value your view on where the borrowing-vs-switch decision should live, and whether a Turkic resource venue fits. One-pager available.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Kemal Oflazer — Subject: Morphological integration as a signal for Kazakh–Russian borrowing vs switching**

```
Dear Prof. Oflazer,

Your finite-state Turkish morphology work is partly why I'm writing. Kazakh is agglutinative like Turkish, and I think morphology is exactly what separates a Russian loanword that has taken Kazakh suffixes from a genuine switch into Russian, which is the distinction that automatic LID keeps getting wrong on Kazakhstani social media.

I built a document-level gold set (3,076 ru/kz/mixed) whose guideline treats loanword-only Kazakh as Kazakh. A fine-tuned XLM-R reaches ~96.6% macro-F1 on a held-out gold test, and re-scoring a ~331k corpus drops real switching to about 5%, far below what keyword heuristics claimed.

Two questions from a solo student: is morphological integration a usable, testable signal for the borrowing-vs-switch line, and what would you tell someone trying to turn a finished capstone into a first paper? One-pager ready.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Wajdi Zaghouani — Subject: Word-level borrowing vs switching, from Arabizi to Kazakh–Russian**

```
Dear Prof. Zaghouani,

Your North-African Arabizi treebank, with its word-level code-switching labels, is the closest annotation problem I found to mine. Yours mixes scripts; mine hides inside one, because Kazakh and Russian share Cyrillic and Kazakh carries heavy Russian borrowing, so automatic LID calls almost everything "mixed".

I hand-labeled 3,076 Kazakhstani messages (ru/kz/mixed) with a guideline that keeps loanword-only Kazakh as Kazakh and tags only genuine switching as mixed. XLM-R hits ~96.6% macro-F1 on a held-out gold test (fastText ~71%); on a ~331k corpus real switching is near 5%.

I'd value your view on how your team drew the loanword-vs-switch line during Arabizi annotation, and whether a WANLP-style resource track has an analog that would fit a kk–ru gold set. One-pager available.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Shuly Wintner — Subject: A "Shared" tier for Kazakh–Russian, echoing your CS-trigger work**

```
Dear Prof. Wintner,

Your "Shared Lexical Items as Triggers of Code Switching," and the "Shared" language-ID tag in your Arabizi corpus, describe exactly the zone that wrecks my Kazakh–Russian labels. A Russian loanword absorbed into Kazakh lives in both lexicons, and automatic LID reads it as a switch, so it over-counts mixing badly.

I hand-labeled 3,076 messages (ru/kz/mixed) with a guideline that keeps loanword-only Kazakh as Kazakh; XLM-R reaches ~96.6% macro-F1 on a held-out gold test, and on a ~331k corpus real switching lands near 5% rather than the ~1.7% precision of a keyword heuristic.

Two questions: should a document-level model keep a "shared/ambiguous" tier like yours instead of forcing kz/ru/mixed, and would your trigger findings predict where my false "mixed" cases cluster? Happy to share data and a one-pager.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Haizhou Li — Subject: Same-script code-switching LID: Kazakh–Russian vs SEAME**

```
Dear Prof. Li,

SEAME was built for language-boundary detection and LID on Mandarin–English code-switching, and that's why I wanted to write. SEAME's two languages sit in different scripts, so a boundary is visible; my case is the opposite. Kazakh and Russian share Cyrillic, and Kazakh carries heavy Russian borrowing, so automatic LID has no script cue and calls almost everything "mixed".

I hand-labeled 3,076 Kazakhstani text messages (ru/kz/mixed) under a guideline that keeps loanword-only Kazakh as Kazakh; a fine-tuned XLM-R reaches ~96.6% macro-F1 on a held-out gold test, and on a ~331k corpus real switching is near 5%.

Do you think same-script contact pairs need a different LID protocol than SEAME's, and would a text-side gold set be useful alongside speech corpora like yours? One-pager available.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Grzegorz Kondrak — Subject: Character-level separation of Kazakh–Russian loanwords vs switches**

```
Dear Prof. Kondrak,

Your character-level work, transliteration, cognates, and cipher language identification, is directly useful to a problem I just finished. Kazakh and Russian share Cyrillic, so a character n-gram model carries all the LID signal, and integrated Russian loanwords blur it exactly the way cognates blur relatedness.

I hand-labeled 3,076 messages (ru/kz/mixed) with a guideline that keeps loanword-only Kazakh as Kazakh; XLM-R reaches ~96.6% macro-F1 on a held-out gold test, and a reviewer asked me to add a smoothed character-trigram baseline, which is where your methods would help me most.

My question: can cognate-style character similarity, or your orthographic similarity measures, help separate a morphologically integrated loanword from a genuine switch? I'd value your read, and can send a one-pager.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

**Anoop Kunchukuttan — Subject: Borrowing vs switching for a related-languages pair (kk–ru)**

```
Dear Anoop,

Your related-languages framing in IndicNLP, plus your transliteration and code-mixing work, match how I think about Kazakh–Russian. The twist is script: Indic code-mixing often shows up Romanized against English, while kk–ru shares Cyrillic, so borrowing hides in plain sight and automatic LID over-labels "mixed".

I hand-labeled 3,076 messages (ru/kz/mixed) under a guideline that keeps loanword-only Kazakh as Kazakh; XLM-R reaches ~96.6% macro-F1 on a held-out gold test (fastText ~71%), and on a ~331k corpus real switching is near 5%.

I'd value your view on how AI4Bharat separates borrowing from switching in code-mixed Indic data, and whether a related-languages framing (VarDial or a resource track) is the right home for a kk–ru gold set. One-pager available.

Bogdan Savelyev
Samsung Innovation Campus capstone (individual)
GitHub https://github.com/naadgob/KazNLP · data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

### Shortlist for the next round (real & relevant; verify email before send)

- **Kareem Darwish** — Arabic dialect identification (script/variety confusion). (verify current affiliation)
- **Jacob Eisenstein** — USA (Google) — computational sociolinguistics, lexical variation in social media. (new US name; email hard)
- **Yaron Matras** — UK/contact linguistics — borrowing and language contact theory. (linguistics depth beyond NLP)
- **Penelope Gardner-Chloros** — UK (Birkbeck) — code-switching theory (may be emerita).
- **Manuel Mager** — indigenous American languages, code-switching/LID. (Latin America angle; email verify)
- **Charibeth Cheng** — Philippines (De La Salle) — Taglish / Filipino code-switching. (SE Asia)
- **Reut Tsarfaty** — Israel (Bar-Ilan) — morphologically rich languages, non-canonical text.
- Cyrillic + Russian-contact neighbors worth hunting: a **Mongolian** (Cyrillic) NLP contact and a **Tajik** (Cyrillic Persian) contact — both mirror the kk–ru script-shared setup, but I don't have verified emails yet.

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

Links: GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights

Best regards,
Bogdan Savelyev
bogsav999@gmail.com
```

### 4.2 Zhanibek Kozhirbayev

**Subject:** Document-level kk–ru LID on UGC (after your KazNLP / KRCS line of work)

```
Dear Dr. Kozhirbayev,

Your work on Kazakh–Russian language identification for noisy user text (with Yessenbayev and Makazhanov) and the recent KRCS paper are the closest published lines I’ve found to a problem I hit while building a capstone system on Kazakhstani Telegram and reviews.

I’m Bogdan Savelyev. I collected a 3,076-example gold set for document-level ru / kz / mixed, with guidelines that treat loanword-only Kazakh as kz rather than mixed. On that gold test, transformer LID clearly beats the FastText/Lingua baselines we tried; applying the model to a larger pool changes how much “mixed” you think is in the wild compared with auto-labels at scrape time.

I know the NU toolkit is already named KazNLP — my student project reused that name by accident, so I’d rebrand for any paper. I’m reaching out to ask whether a short conversation about fit (resource note vs methods, and a sensible venue) would be welcome. Happy to send a one-pager first if that’s easier.

GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights

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
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
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
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

### 4.5 Marcos Zampieri

**Subject:** VarDial-shaped question: kk–ru LID with a loanword vs switch gold set

```
Dear Professor Zampieri,

I’m writing because of your VarDial work and the LID / language-variety evaluation papers (including the true-labels LID work with Jauhiainen et al.). I have a finished student project on a messy bilingual case that sits between “similar languages” and code-switching: Russian and Kazakh in Telegram and reviews, where loanword-heavy Kazakh gets labeled mixed by off-the-shelf LID.

Artifact in one line: 3,076 gold documents, shared test ladder (FastText / Lingua / XLM-R), and a filter-first cascade before sentiment. I’d like advice on whether a short paper belongs at VarDial, a code-switching workshop, or a resource track — and I’m happy to keep the first conversation at that level of detail.

Bogdan Savelyev
Samsung Innovation Campus (individual capstone) · GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
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
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

### 4.7 Monojit Choudhury

**Subject:** kk–ru social LID — false “mixed” at scale

```
Dear Professor Choudhury,

Your code-mixing / multilingual inclusion work (including the CALCS community and papers on how models mishandle linguistic diversity) is why I’m writing. In Kazakhstani Telegram, automatic LID paints almost everything as mixed; when I measured it, the true switch rate under a stricter definition was tiny compared with the auto label rate.

I’ve put together a gold set and a transformer baseline for ru/kz/mixed under that stricter definition, then used it to rescore a larger corpus. If you’re open to a short note on whether this is a useful data point for the CS community — or who among your students/collaborators looks at Turkic–Russian mixing — I’d appreciate a pointer.

Bogdan Savelyev
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

### 4.8 Genta Winata

**Subject:** Adding kk–ru to the CS map (document LID gold)

```
Hi Genta,

I’ve used your code-switching survey and the github paper list while finishing a capstone on Kazakh–Russian mixed social text. Most CS LID/sentiment work still doesn’t cover this pair; I have a 3k+ document-level gold set that separates true switches from loanword Kazakh, plus a simple XLM-R baseline and a public demo pipeline.

If you have a minute: does this sound more like CALCS material or VarDial-style LID? A one-line opinion already helps. Happy to send a one-pager.

Bogdan
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

### 4.9 Sunayana Sitaram / Kalika Bali (MSR — slightly more formal)

**Subject:** Resource question: kk–ru code-switch LID gold (social domain)

```
Dear Dr. Sitaram,

I’m a student who finished an individual NLP capstone on Kazakh–Russian document-level language ID for noisy social text. GLUECoS and your code-switching evaluation work are the benchmark style I had in mind, for a pair that still rarely appears in those suites.

I have a manually labeled gold set (3,076) with guidelines for loanwords vs switches, and shared-split comparisons against FastText and Lingua. I’m writing to ask whether MSR’s multilingual/CS group ever looks at Turkic–Russian mixing, and whether a short conversation or a referral would be appropriate. No request for internship paperwork in this email — only fit.

Thank you,
Bogdan Savelyev
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

(For Bali: swap name; mention low-resource / inclusive multilingual tech instead of GLUECoS.)

### 4.10 Yves Scherrer

**Subject:** Multi-signal LID: Kazakh with Russian loans vs true mixed documents

```
Dear Professor Scherrer,

Your VarDial and closely-related-variety work (including multi-label Scandinavian LID) resonates with a labeling problem I hit on Kazakh–Russian UGC: many documents aren’t cleanly one language, but “mixed” in scraper labels is also wrong when the only Russian material is a loanword inside Kazakh morphosyntax.

I built a three-way gold set and baselines for that distinction. I’d welcome advice on how the VarDial community prefers such cases to be framed (variety ID vs code-switching vs multi-label LID). A short reply is plenty.

Bogdan Savelyev
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

### 4.11 Zhandos Yessenbayev / Aibek Makazhanov (shared template)

**Subject:** Following your KazNLP LID work — new gold for loanword vs switch

```
Dear Dr. [Yessenbayev/Makazhanov],

I learned the NU KazNLP pipeline’s LID component (document- and word-level kk/ru/other on noisy UGC) while working on a related student project. My focus is a stricter document-level mixed class: true code-switching versus Kazakh sentences that only contain Russian loans — a distinction that still breaks FastText-style labeling on Telegram-scale data.

I’ve released (or can share) a 3,076-example gold set and XLM-R baselines. I’d like to ask whether anyone from the original KazNLP line is still advising students on this topic, and whether a brief conversation would be welcome. I’ll use a different project name in any paper to avoid clashing with your toolkit.

Bogdan Savelyev
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
```

### 4.12 Injy Hamed (shorter)

**Subject:** Non-Arabic CS pair seeking CALCS-facing advice

```
Dear Dr. Hamed,

I saw your code-switched Arabic NLP survey and CALCS organizing work. I’m a student with a finished gold set for Kazakh–Russian document LID (loanword vs true switch) and I’m trying to learn whether CALCS is open to underrepresented pairs presented as resource/short papers.

If you can spare a short reply on fit — or redirect me to the right PC — I’d be grateful.

Bogdan Savelyev
GitHub https://github.com/naadgob/KazNLP · weights & data https://huggingface.co/datasets/naadgob/kaznlp-weights
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
| Malykh | val@maly.hk | A | 2026-07-16 | 2026-07-30 | | | sent · KRCS advisor |
| Kozhirbayev | zhanibek.kozhirbayev@nu.edu.kz | A | 2026-07-16 | 2026-07-30 | | | sent · NU |
| Borisov | borisovmaksim@niuitmo.ru | A | 2026-07-16 | 2026-07-30 | | | sent · KRCS peer |
| Jauhiainen | tommi.jauhiainen@helsinki.fi | B | 2026-07-16 | 2026-07-30 | | | sent |
| Zampieri | mzampier@gmu.edu | B | 2026-07-16 | 2026-07-30 | | | sent · address inferred (NetID) |
| Solorio | thamar.solorio@mbzuai.ac.ae | C | 2026-07-16 | 2026-07-30 | | | sent |
| Choudhury | monojit.choudhury@mbzuai.ac.ae | C | 2026-07-16 | — | yes (same day) | intro accepted | replied: no longer in CS, cc'd Prashant Kodali |
| Kodali (Prashant) | prashant.kodali@research.iiit.ac.in / t-prakodali@microsoft.com | C | 2026-07-16 | 2026-07-30 | | await reply | warm intro via Choudhury; active in code-mixing |
| Winata | gentaindrawinata@gmail.com | C | 2026-07-16 | 2026-07-30 | | | sent |
| Scherrer | yves.scherrer@ifi.uio.no | B | 2026-07-16 | 2026-07-30 | | | sent · verified (Oslo faculty page) |
| Hamed | injy.hamed@mbzuai.ac.ae | C | 2026-07-16 | 2026-07-30 | | | sent · verified (ACL papers) |
| Sitaram | sunayana.sitaram@microsoft.com | C | 2026-07-16 | 2026-07-30 | | | sent · verified; note: high inbox volume |
| Nakov | preslav.nakov@mbzuai.ac.ae | B | 2026-07-16 | 2026-07-30 | | | sent · MBZUAI format |
| Baldwin | timothy.baldwin@mbzuai.ac.ae | B | 2026-07-16 | 2026-07-30 | | | sent · MBZUAI format |
| Anastasopoulos | antonis@gmu.edu | E→C | 2026-07-16 | 2026-07-30 | | | sent · verified (GMU faculty page) |
| Yessenbayev | zyessenbayev@binus.edu | A | 2026-07-16 | 2026-07-30 | | | sent · now at Bina Nusantara (Scholar) |
| Makazhanov | aibek.makazhanov@nu.edu.kz | A | 2026-07-16 | 2026-07-30 | | | sent · address may be stale |
| Lindén | krister.linden@helsinki.fi | B | 2026-07-16 | 2026-07-30 | | | sent · LID book co-author |
| Malmasi | malmasi@amazon.com | C | 2026-07-16 | 2026-07-30 | | | sent · DSL/VarDial |
| Abdurakhmonova | abdurahmonova.1987@mail.ru | D | 2026-07-16 | 2026-07-30 | | | sent · Turkic NLP |
| Bali | kalikab@microsoft.com | C | 2026-07-16 | 2026-07-30 | | | sent · inferred pattern |
| Kar (Sudipta) | sudipta.kar.8080@gmail.com | C | 2026-07-16 | 2026-07-30 | | | sent · CALCS organizer |
| Wijaya (Derry) | derry.wijaya@monash.edu | C | 2026-07-16 | 2026-07-30 | | | sent · CALCS |
| Diab (Mona) | mdiab@andrew.cmu.edu | C | 2026-07-16 | 2026-07-30 | | | sent |
| Bullock | bbullock@austin.utexas.edu | C | 2026-07-16 | 2026-07-30 | | | sent · linguist framing |
| Toribio | toribio@austin.utexas.edu | C | 2026-07-16 | 2026-07-30 | | | sent · linguist framing |
| Doğruöz | as.dogruoz@ugent.be | C | 2026-07-16 | 2026-07-30 | | | sent · CS survey |
| Habash | nizar.habash@nyu.edu | E→C | 2026-07-16 | 2026-07-30 | | | sent · CS survey co-author |
| Vu (Ngoc Thang) | thangvu@ims.uni-stuttgart.de | E→C | 2026-07-16 | 2026-07-30 | | | sent · CS survey |
| Sabty (Caroline) | caroline.sabty@giu-uni.de | E→C | 2026-07-16 | 2026-07-30 | | | sent · CS survey |
| Neubig | gneubig@cs.cmu.edu | E | 2026-07-16 | 2026-07-30 | | | sent · long-shot |
| Adelani | david.adelani@mcgill.ca | E | 2026-07-16 | 2026-07-30 | | | sent |
| Aji (Alham Fikri) | alham.fikri@mbzuai.ac.ae | E | 2026-07-16 | 2026-07-30 | | | sent · MBZUAI format |
| Yong (Zheng Xin) | contact.yong@brown.edu | E | 2026-07-16 | 2026-07-30 | | | sent · CS survey |
| Plank (Barbara) | bplank@cis.lmu.de | E | 2026-07-16 | 2026-07-30 | | | sent · inferred pattern |
| Augenstein | augenstein@di.ku.dk | E | 2026-07-16 | 2026-07-30 | | | sent |
| Vulić | iv250@cam.ac.uk | E | 2026-07-16 | 2026-07-30 | | | sent · may be stale (now DeepMind) |
| Korhonen | alk23@cam.ac.uk | E | 2026-07-16 | 2026-07-30 | | | sent |
| Fung (Pascale) | pascale@ust.hk | E | 2026-07-16 | 2026-07-30 | | | sent |
| Zhukova (Marina) | — | C | | | | | HELD — UCSB address defunct (now MSFT) |
| Elov (Botir) | — | D | | | | | HELD — no verified email |
| Ruder (Sebastian) | — | E | | | | | HELD — no public email (via ruder.io) |

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
