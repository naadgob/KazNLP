"""Build kaznlp-story-deck-self.html (20 slides) from existing deck CSS + PRESENTATION_OUTLINE."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_DONOR = ROOT / "docs" / "capstone" / "kaznlp-story-deck-self.html"
OUT = CSS_DONOR

EXTRA_CSS = """
    .slide {
      padding: 44px 64px 40px 0;
      flex-direction: row;
      gap: 0;
    }
    .chapter-rail {
      width: 108px;
      flex-shrink: 0;
      padding: 8px 0 0 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      border-right: 1px solid var(--line);
      margin-right: 28px;
      align-self: stretch;
    }
    .slide--paper .chapter-rail { border-color: var(--line-dark); }
    .rail-act {
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--muted-dim);
      line-height: 1.35;
      opacity: 0.45;
      transition: opacity 0.2s ease, color 0.2s ease;
    }
    .rail-act.is-current { opacity: 1; color: var(--mixed); }
    .rail-act--i.is-current { color: var(--ru); }
    .rail-act--ii.is-current { color: var(--mixed); }
    .rail-act--iii.is-current { color: var(--kz); }
    .rail-act--iv.is-current { color: var(--pos); }
    .rail-act-name { display: block; font-size: 9px; letter-spacing: 0.06em; margin-top: 2px; }
    .rail-slide {
      margin-top: auto;
      font-family: var(--font-mono);
      font-size: 28px;
      font-weight: 500;
      letter-spacing: -0.04em;
      color: var(--fg);
      padding-bottom: 4px;
    }
    .slide--paper .rail-slide { color: var(--ink); }
    .slide-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-height: 0;
      min-width: 0;
      padding-right: 64px;
    }
    .sc-q {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.03em;
      color: var(--mixed);
      margin-bottom: 8px;
      max-width: 78ch;
      line-height: 1.4;
    }
    .slide--paper .sc-q { color: #a16207; }
    .sc-story {
      font-size: 15px;
      line-height: 1.5;
      color: var(--muted);
      max-width: 78ch;
      margin-bottom: 18px;
    }
    .slide--paper .sc-story { color: #52525b; }
    .slide--peak::before {
      content: "";
      position: absolute;
      top: 0; left: 108px; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--mixed), transparent 70%);
      opacity: 0.7;
    }
    .slide--peak.slide--paper::before { left: 108px; }
    .role-grid {
      display: grid;
      grid-template-columns: 140px 1fr;
      gap: 10px 20px;
      font-size: 15px;
      max-width: 820px;
    }
    .role-grid dt { color: var(--ru); font-weight: 600; }
    .role-grid dd { color: var(--muted); margin: 0; }
    .slide--paper .role-grid dd { color: #52525b; }
    .timeline-strip {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      max-width: 900px;
    }
    .tl-card {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 16px 18px;
    }
    .tl-card__val { font-size: 26px; font-weight: 600; margin-bottom: 4px; }
    .tl-card__lbl { font-size: 13px; color: var(--muted); }
    .manifesto-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      max-width: 52ch;
    }
    .manifesto-body h1 { font-size: 48px; max-width: none; margin-bottom: 20px; }
    .bridge-flow {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      margin: 16px 0;
      font-size: 14px;
    }
    .bridge-node {
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid var(--line);
      background: var(--surface);
    }
    .bridge-node--after { border-color: var(--kz); color: var(--kz); }
    .bridge-arrow { color: var(--muted-dim); font-family: var(--font-mono); }
    .proto-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      max-width: 880px;
    }
    .proto-card {
      border: 1px solid var(--line-dark);
      border-radius: 12px;
      padding: 16px 18px;
      background: #fff;
    }
    .proto-card h3 { font-size: 14px; margin-bottom: 8px; color: var(--ink); }
    .proto-card p { font-size: 14px; color: #52525b; line-height: 1.45; }
    .qualifier-badge {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 6px 12px;
      border-radius: 6px;
      background: rgba(212, 160, 36, 0.15);
      color: var(--mixed);
      border: 1px solid rgba(212, 160, 36, 0.35);
      margin-bottom: 14px;
    }
    .qual-compare {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      max-width: 720px;
      margin-top: 8px;
    }
    .qual-box {
      padding: 14px 16px;
      border-radius: 10px;
      border: 1px solid var(--line);
      font-size: 14px;
    }
    .qual-box--ok { border-color: rgba(34, 179, 104, 0.4); }
    .qual-box--no { border-color: rgba(224, 69, 69, 0.35); }
    .cmd-block {
      font-family: var(--font-mono);
      font-size: 13px;
      line-height: 1.55;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 14px 18px;
      color: var(--muted);
    }
    .cmd-block code { color: var(--fg); }
    .data-pills {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 8px;
    }
    .data-pill {
      padding: 12px 18px;
      border-radius: 10px;
      border: 1px solid var(--line);
      background: var(--surface);
    }
    .data-pill strong { display: block; font-size: 22px; margin-bottom: 2px; }
    .data-pill span { font-size: 13px; color: var(--muted); }
    h1 { font-size: 38px; max-width: 24ch; }
    .slide--manifesto .slide-body { justify-content: center; }
    .slide--manifesto h1 { font-size: 44px; max-width: 28ch; }
"""

ACTS = [
    ("I", "Ставки"),
    ("II", "Тупики"),
    ("III", "Доказ."),
    ("IV", "Продукт"),
]

ACT_FOR_SLIDE = {
    **{i: "I" for i in range(1, 6)},
    **{i: "II" for i in range(6, 10)},
    **{i: "III" for i in range(10, 16)},
    **{i: "IV" for i in range(16, 21)},
}


def rail(act: str, num: int) -> str:
    parts = []
    for code, name in ACTS:
        cls = f"rail-act rail-act--{code.lower()}"
        if code == act:
            cls += " is-current"
        parts.append(f'<div class="{cls}">{code}<span class="rail-act-name">{name}</span></div>')
    parts.append(f'<div class="rail-slide num">{num:02d}</div>')
    return f'<nav class="chapter-rail" aria-label="Акты">{"".join(parts)}</nav>'


def slide(
    num: int,
    label: str,
    question: str,
    title: str,
    story: str,
    body: str,
    therefore: str,
    *,
    paper: bool = False,
    peak: bool = False,
    manifesto: bool = False,
    foot_meta: str = "",
) -> str:
    act = ACT_FOR_SLIDE[num]
    classes = ["slide"]
    if num == 1:
        classes.append("active")
    if paper:
        classes.append("slide--paper")
    if peak:
        classes.append("slide--peak")
    if manifesto:
        classes.append("slide--manifesto")
    cls = " ".join(classes)
    grain = "" if paper else '<div class="grain" aria-hidden="true"></div>'
    foot = f'<div class="vyvod"><strong>Вывод:</strong> {therefore}</div>'
    if foot_meta and not therefore:
        foot = f'<p class="slide-muted">{foot_meta}</p>'
    elif foot_meta:
        foot += f'<p class="slide-muted">{foot_meta}</p>'
    return f"""
      <section class="{cls}" data-act="{act}" data-slide="{num:02d}" data-label="{label}">
        {grain}
        {rail(act, num)}
        <div class="slide-body">
          <p class="sc-q">Вопрос: {question}</p>
          <h1>{title}</h1>
          <p class="sc-story">{story}</p>
          {body}
          <footer class="slide-foot">
            {foot}
          </footer>
        </div>
      </section>"""


SLIDES = [
    slide(
        1, "01 Открытие",
        "Зачем вообще отдельный проект про LID в Казахстане?",
        "Два языка в одном отзыве",
        "В Telegram, на Kaspi и в 2GIS люди пишут шала-казахский: русский и казахский в одном сообщении. "
        "Чтобы считать долю двуязычия или учить тональность, сначала нужно отделить ru, kz и mixed. "
        "KazNLP: pipeline «сначала язык, потом тон» на корпусе 422k+ строк, не на учебной выборке.",
        """<div class="s01-grid" style="margin-top:4px;align-items:center">
          <p class="s01-meta" style="font-size:15px;color:var(--muted);margin:0">Samsung Innovation Campus<br>Bogdan Savelyev · июнь 2026</p>
          <div class="pipe-flow" aria-label="Pipeline">
            <span class="pipe-node">TEXT</span><span class="pipe-line"></span>
            <span class="pipe-node">LID</span><span class="pipe-line"></span>
            <span class="pipe-node">ROUTE</span><span class="pipe-line"></span>
            <span class="pipe-node">TONE</span>
          </div>
        </div>""",
        "Без точного LID любая аналитика по mixed строится на шуме.",
    ),
    slide(
        2, "02 Источники",
        "Это лабораторная задача или реальные тексты?",
        "Где живёт проблема",
        "Корпус из KZ digital: 422&nbsp;141 комментарий Telegram (Telethon), 39&nbsp;129 отзывов Kaspi, "
        "отзывы 2GIS для tone. Колонка language при сборе Telegram ставится FastText v1: метка сборщика, не ground truth.",
        """<div class="uc-grid" style="margin-top:4px">
          <article class="uc-card">
            <span class="uc-source">Telegram <span class="num">422&nbsp;141</span></span>
            <p class="uc-quote">«Всё супер, рахмет, күтеміз келесі жаңалықты»</p>
          </article>
          <article class="uc-card">
            <span class="uc-source">Kaspi <span class="num">39&nbsp;129</span></span>
            <p class="uc-quote">«Курьер молодец, уақытында әкелді»</p>
          </article>
          <article class="uc-card">
            <span class="uc-source">2GIS · tone</span>
            <p class="uc-quote">«Тамақтары дәмді, но официант долго не подходил»</p>
          </article>
        </div>""",
        "Проблема масштабируется вместе с объёмом данных.",
    ),
    slide(
        3, "03 Кому мешает",
        "Кому мешает неточный LID?",
        "Что ломается без фильтра",
        "Исследователь кладёт «mixed» в корпус для sentiment и подмешивает kz с русским заёмом. "
        "Аналитик строит дашборд по языкам. Продуктовая команда видит «массовое двуязычие». "
        "Во всех случаях auto-LID путает code-switch с заёмным словом в казахской грамматике.",
        """<dl class="role-grid">
          <dt>Исследователь</dt><dd>Обучает sentiment на шумных mixed-метках</dd>
          <dt>Аналитик</dt><dd>Доля bilingual завышена в десятки раз</dd>
          <dt>Продукт</dt><dd>Решения по «массовому mixed» без проверки</dd>
          <dt>NLP</dt><dd>Модели учатся на auto-labels, не на речи</dd>
        </dl>""",
        "Нужен измеримый фильтр, а не ещё одна эвристика.",
    ),
    slide(
        4, "04 Граница",
        "Где проходит граница mixed и kz?",
        "Не всякий казахский с русским словом это mixed",
        "«Курьер молодец, уақытында әкелді»: две языковые фразы, это mixed. "
        "«Качествосы жақсы, арзан»: казахская грамматика с русским заёмом, это kz. "
        "Наивный LID видит кириллицу и казахские буквы и часто ставит mixed на втором примере.",
        """<div class="cmp-cols">
          <article class="cmp-col cmp-col--yes">
            <span class="cmp-badge">Переключение (mixed)</span>
            <p class="cmp-quote">«Курьер молодец, уақытында әкелді»</p>
            <p class="cmp-caption">Две фразы, две грамматики</p>
            <span class="chip chip--mixed">mixed</span>
          </article>
          <article class="cmp-col cmp-col--no">
            <span class="cmp-badge">Заём, не mixed</span>
            <p class="cmp-quote">«Качествосы жақсы, арзан»</p>
            <p class="cmp-caption">Казахская грамматика (-сы)</p>
            <span class="chip chip--kz">kz</span>
          </article>
        </div>""",
        "Задача не «есть ли казахские буквы», а «есть ли переключение языковых фраз».",
    ),
    slide(
        5, "05 Диагностика",
        "Насколько сильно врёт auto-LID?",
        "Из ~100 auto-mixed только 2-3 настоящих",
        "На срезе 27&nbsp;628 FT-mixed эвристика is_real_mixed() пропустила 460 строк (~1,66%). "
        "После FT v2 на корпусе 66&nbsp;462 mixed precision по той же эвристике: 2,32% (1&nbsp;542/66&nbsp;462). "
        "Эвристика не gold, но порядок шума зафиксирован.",
        """<div class="stats-hero">
          <div>
            <div class="comment-grid" aria-hidden="true">
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot comment-dot--true">✓</span><span class="comment-dot"></span><span class="comment-dot"></span>
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span>
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot comment-dot--true">✓</span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span>
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span>
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot comment-dot--true">✓</span><span class="comment-dot"></span><span class="comment-dot"></span>
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span>
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span>
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span>
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span>
              <span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span><span class="comment-dot"></span>
            </div>
            <p class="grid-caption">из 100 помеченных автоматикой: 2-3 настоящих bilingual</p>
          </div>
          <div class="metric-stack">
            <div class="metric-card"><div class="metric-card__val num">1,66%</div><div class="metric-card__lbl">460 / 27&nbsp;628 (срез FT-mixed)</div></div>
            <div class="metric-card metric-card--accent"><div class="metric-card__val num">2,32%</div><div class="metric-card__lbl">1&nbsp;542 / 66&nbsp;462 (FT v2 corpus)</div></div>
          </div>
        </div>""",
        "Синтетика и правила не спасут без ручного эталона.",
        peak=True,
        foot_meta="main.ipynb §3 · эвристика, не prevalence",
    ),
    slide(
        6, "06 Синтетика",
        "Почему 480k синтетики не решили задачу?",
        "480k синтетики дали 85% F1. На Telegram это не сработало",
        "Старт в main.ipynb (cells 0-21): KazSAnDRA 180&nbsp;064 + clapAI ru 164&nbsp;148, генерация 480&nbsp;000 строк. "
        "На hold-out 96&nbsp;000 строк F1 84,96%. Реальный Telegram показал обратное: synthetic F1 не переносится на KZ соцмедиа.",
        """<div class="research-panel">
          <article class="research-card">
            <span class="research-chip">FastText v1 · baseline</span>
            <div class="research-rows">
              <div><p class="research-row-k">Train</p><p class="research-row-v">480k строк, 4 стратегии mixed</p></div>
              <div><p class="research-row-k">Test</p><p class="research-row-v">F1 <span class="num">84,96%</span> на n=96&nbsp;000</p></div>
            </div>
          </article>
          <div class="big-stat"><span class="big-stat__val num">480k</span><span class="big-stat__lbl">synthetic train</span></div>
        </div>""",
        "Synthetic: baseline, не production.",
        paper=True,
        foot_meta="cells 0-21",
    ),
    slide(
        7, "07 Telegram",
        "Что случилось, когда подключили Telegram?",
        "Реальный корпус рос, шум остался",
        "Сбор Telethon по KZ-каналам (cells 22-44). FastText v1 ставит language при сборе. "
        "Датасет: 146&nbsp;206 → 241&nbsp;576 → 422&nbsp;141 на диске. "
        "Визуально почти всё mixed выглядит как ru или kz с заёмом.",
        """<div class="timeline-strip">
          <article class="tl-card"><p class="tl-card__val num">146k</p><p class="tl-card__lbl">волна 1</p></article>
          <article class="tl-card"><p class="tl-card__val num">242k</p><p class="tl-card__lbl">волна 2</p></article>
          <article class="tl-card"><p class="tl-card__val num">422k</p><p class="tl-card__lbl">финал на диске</p></article>
        </div>""",
        "Нужна диагностика, не сразу трансформер.",
    ),
    slide(
        8, "08 Тупики",
        "Что пробовали до gold и почему остановились?",
        "Четыре shortcut не заменили gold",
        "FT v2: recall 95,51% на 868 seeds, precision 2,32% на корпусе. "
        "Lingua v2: R(mixed) 98,76%, P(mixed) 76,81% на gold test. "
        "LLM для gold LID отвергнут. YouTube ~4,7k не доводили. Kaspi 39&nbsp;129 добавил второй домен с тем же шумом.",
        """<div class="dead-grid">
          <article class="dead-card"><h3>FastText v2</h3><p>95,51% seeds · 2,32% corpus precision</p></article>
          <article class="dead-card"><h3>Lingua v2</h3><p>R 98,76% · P 76,81% mixed на gold</p></article>
          <article class="dead-card"><h3>LLM LID</h3><p>Высокий FP на mixed, исключён</p></article>
          <article class="dead-card"><h3>YouTube</h3><p>~4,7k, прерван</p></article>
        </div>""",
        "Нужны ручной эталон и модель с контекстом целой фразы.",
        foot_meta="cells 45-113",
    ),
    slide(
        9, "09 Мост",
        "Что нужно вместо правил?",
        "Filter-first: gold, затем XLM-R, затем tone",
        "Короткие пути исчерпаны: синтетика, FastText, token-level Lingua. "
        "Следующий шаг: gold LID с честным split и XLM-RoBERTa на сыром text. "
        "Принцип: сначала точный LID на gold, потом скоринг корпуса, потом tone только на mixed.",
        """<div class="bridge-flow">
          <span class="bridge-node">ДО: auto-LID → шум</span>
          <span class="bridge-arrow">→</span>
          <span class="bridge-node">gold 3&nbsp;076 + XLM-R</span>
          <span class="bridge-arrow">→</span>
          <span class="bridge-node bridge-node--after">ПОСЛЕ: filter-first pipeline</span>
        </div>""",
        "Act III: как строили эталон и доказывали качество.",
        manifesto=True,
    ),
    slide(
        10, "10 Gold",
        "Как собирали эталон?",
        "3&nbsp;076 ручных меток LID",
        "Kaspi + Telegram, cheap_clean: 388&nbsp;748 → 254&nbsp;601. Gold батчами: ручная разметка, heuristic-batch, очередь Lingua. "
        "После dedup 3&nbsp;076: ru 1&nbsp;000, kz 999, mixed 1&nbsp;077. LLM в gold LID не использовали.",
        """<div class="gold-layout">
          <div class="class-bars">
            <div class="class-bar"><span class="class-bar__label" style="color:var(--ru)">ru</span><div class="class-bar__track"><div class="class-bar__fill class-bar__fill--ru"></div></div><span class="class-bar__num num">1&nbsp;000</span></div>
            <div class="class-bar"><span class="class-bar__label" style="color:var(--kz)">kz</span><div class="class-bar__track"><div class="class-bar__fill class-bar__fill--kz"></div></div><span class="class-bar__num num">999</span></div>
            <div class="class-bar"><span class="class-bar__label" style="color:var(--mixed)">mixed</span><div class="class-bar__track"><div class="class-bar__fill class-bar__fill--mixed"></div></div><span class="class-bar__num num">1&nbsp;077</span></div>
          </div>
        </div>""",
        "Есть эталон; нужен честный протокол обучения.",
        paper=True,
        foot_meta="cells 114-153 · gold_v1.csv",
    ),
    slide(
        11, "11 Протокол",
        "Почему метрики можно доверять?",
        "Честный split: gold-only test, synth только в train",
        "Stratified 80/10/10, random_state=42: train 2&nbsp;691, val 462, test 461 (gold-only). "
        "538 synthetic hard-паттернов только в train, вес gold:synth = 3:1. "
        "XLM-R учится на сыром text, не text_norm: нормализация режет bilingual-сигнал.",
        """<div class="proto-grid">
          <article class="proto-card"><h3>Split</h3><p>train 2&nbsp;691 · val 462 · test <span class="num">461</span> gold-only</p></article>
          <article class="proto-card"><h3>Synthetic</h3><p>538 строк только train · weight 3:1</p></article>
          <article class="proto-card"><h3>Input</h3><p>Сырой text, не text_norm (~219/1077 mixed теряют признаки)</p></article>
          <article class="proto-card"><h3>Eval</h3><p>Val и test без synthetic · один test.csv для ladder</p></article>
        </div>""",
        "Можно обучать и сравнивать модели на одном test.",
        paper=True,
    ),
    slide(
        12, "12 XLM-R",
        "Какой результат дала модель?",
        "96,56% macro-F1 на gold test",
        "XLM-RoBERTa-base, Kaggle 2× T4. v1: 95,92%; v2: 96,56% на n=461. "
        "CM v2: ru 150/150, kz 142/150, mixed 153/161. 14 из 16 ошибок: граница kz↔mixed.",
        """<div class="cm-layout">
          <div><div class="cm-hero-num num">96,56%</div><p class="cm-hero-sub">macro-F1 · gold test n=<span class="num">461</span></p></div>
          <table class="cm-table" aria-label="Confusion matrix">
            <thead><tr><th></th><th>pred ru</th><th>pred kz</th><th>pred mixed</th></tr></thead>
            <tbody>
              <tr><td class="cm-row-label">true ru</td><td><div class="cm-cell cm-cell--hi">150</div></td><td><div class="cm-cell cm-cell--zero">0</div></td><td><div class="cm-cell cm-cell--zero">0</div></td></tr>
              <tr><td class="cm-row-label">true kz</td><td><div class="cm-cell cm-cell--zero">0</div></td><td><div class="cm-cell cm-cell--hi">142</div></td><td><div class="cm-cell cm-cell--err">8</div></td></tr>
              <tr><td class="cm-row-label">true mixed</td><td><div class="cm-cell cm-cell--err">2</div></td><td><div class="cm-cell cm-cell--err">6</div></td><td><div class="cm-cell cm-cell--hi">153</div></td></tr>
            </tbody>
          </table>
        </div>""",
        "LID v2: production-модель; сравним с baselines на том же test.",
        paper=True,
        foot_meta="xlm-r_v2.pt · cells 173, 268",
    ),
    slide(
        13, "13 Ladder",
        "Почему не остановились на FastText или Lingua?",
        "71% → 89% → 96,56% на одном hold-out",
        "§10 main.ipynb (cells 267-268): все LID-модели на test.csv n=461. "
        "FastText v1 63,24% → v2 70,92% → Lingua v2 88,63% → XLM-R v2 96,56%. "
        "Lingua ловит почти все mixed (R 98,76%), но P 76,81%: для фильтра корпуса непригодна.",
        """<div class="ladder-wrap">
          <div class="ladder-row"><span class="ladder-name">FastText v2</span><div class="ladder-bar"><div class="ladder-fill ladder-fill--ft"></div></div><span class="ladder-pct num">70,92%</span></div>
          <div class="ladder-row"><span class="ladder-name">Lingua v2</span><div class="ladder-bar"><div class="ladder-fill ladder-fill--ling"></div></div><span class="ladder-pct num">88,63%</span></div>
          <div class="ladder-row"><span class="ladder-name">XLM-R v2</span><div class="ladder-bar"><div class="ladder-fill ladder-fill--xlm"></div></div><span class="ladder-pct ladder-pct--win num">96,56%</span></div>
        </div>""",
        "Главный научный результат: LID; применяем к корпусу.",
        peak=True,
        foot_meta="один test.csv · macro-F1",
    ),
    slide(
        14, "14 Корпус",
        "Что получилось на полном пуле?",
        "331&nbsp;468 строк в main.csv",
        "XLM-R v2 перескорил Kaspi+Telegram → kaspi-telegram_dataset_v2.csv (254&nbsp;652). "
        "Добавлены 2GIS. Финальная сборка cell 237: main.csv 331&nbsp;468 (ru 281&nbsp;409 · kz 33&nbsp;695 · mixed 16&nbsp;364). "
        "Промежуточные ячейки 203/221 устарели; каноничное число: cell 237.",
        """<div class="funnel-layout">
          <div class="funnel-stack">
            <div class="funnel-stage"><p class="funnel-val num">422&nbsp;141</p><p class="funnel-lbl">Telegram raw</p></div>
            <p class="funnel-arrow">↓ clean + Kaspi + 2GIS + XLM-R v2</p>
            <div class="funnel-stage"><p class="funnel-val num">331&nbsp;468</p><p class="funnel-lbl">main.csv</p></div>
            <p class="funnel-arrow">↓ language = mixed</p>
            <div class="funnel-stage funnel-stage--final"><p class="funnel-val num">16&nbsp;364</p><p class="funnel-lbl">main_mixed.csv</p></div>
          </div>
        </div>""",
        "16k: следующий слайд объясняет, что это значит и чего не значит.",
        foot_meta="cell 237 · disk-verified 2026-06-15",
    ),
    slide(
        15, "15 Qualifier",
        "Что 16&nbsp;364 mixed НЕ означает?",
        "Model-predicted, не human-audited",
        "main_mixed.csv: предсказания XLM-R v2, не ручной аудит. Corpus audit 100 random mixed не выполняли. "
        "Gold test mixed P/R ~95% на n=461 не переносится автоматически на 16&nbsp;364 строк корпуса.",
        """<span class="qualifier-badge">model-predicted · not human-audited</span>
        <div class="qual-compare">
          <div class="qual-box qual-box--ok"><strong>Корректно:</strong> отфильтровали 16&nbsp;364 кандидата по LID v2</div>
          <div class="qual-box qual-box--no"><strong>Некорректно:</strong> «подтверждённых mixed» или «честных 16k»</div>
        </div>""",
        "Корпус: применение модели; tone: отдельная ветка.",
    ),
    slide(
        16, "16 Tone",
        "Tone 97,33%: это то же, что LID 96,56%?",
        "Две разные задачи на разных eval set",
        "Tone на mixed-отзывах 2GIS. Gold 3&nbsp;529; ~94% меток от LLM-draft (llm_composer), manual 217. "
        "Tone v1: 97,33% на test n=525. Метрика отражает согласованность с LLM-разметкой, не независимую human validation. v2 хуже (96,19%), выбран v1.",
        """<div class="tone-layout">
          <div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
              <div class="dual-metric dual-metric--lid"><p class="dual-metric__task">LID macro-F1</p><p class="dual-metric__val num">96,56%</p><p style="font-size:12px;color:#71717a">gold n=461</p></div>
              <div class="dual-metric dual-metric--tone"><p class="dual-metric__task">Tone accuracy</p><p class="dual-metric__val num">97,33%</p><p style="font-size:12px;color:#71717a">mixed 2GIS n=525</p></div>
            </div>
            <p class="caveat-box">94% tone gold = llm_composer. Manual 217 строк не оценены отдельно.</p>
          </div>
        </div>""",
        "LID: главный результат; tone: stretch goal с оговоркой.",
        paper=True,
        foot_meta="eval_tone_v1.py · metrics_tone_test.json",
    ),
    slide(
        17, "17 Cascade",
        "Как части связаны в продукте?",
        "Filter-first cascade",
        "inference/pipeline.py: сырой text → XLM-R LID v2 (ru|kz|mixed) → auto-route. "
        "Ru → RuBERT. Kz → Kazakh sentiment BERT. Mixed → Tone v1. Тональность на mixed не смешивается с монолингвальными путями.",
        """<div class="cascade-steps" style="max-width:520px">
          <div class="cascade-step">1. XLM-R LID v2 → ru | kz | mixed</div>
          <p class="cascade-arrow">↓</p>
          <div class="cascade-step">2. ru → RuBERT · kz → Kazakh BERT</div>
          <p class="cascade-arrow">↓</p>
          <div class="cascade-step">3. mixed → Tone v1 (XLM-R fine-tune)</div>
        </div>""",
        "Pipeline вышел за рамки ноутбука: demo.",
    ),
    slide(
        18, "18 Demo",
        "Как проверить без автора проекта?",
        "Локальный demo и defense path",
        "python scripts/setup_demo_models.py → python run_demo.py (127.0.0.1:8000). "
        "Labeler: python run_labeler.py. Tone: python scripts/eval_tone_v1.py. "
        "main.ipynb (270 ячеек) не воспроизводится Run All; defense path: cells 45, 173, 237, 268 + скрипты. Первый API-запрос может дать 503 (загрузка ~8,56 GB).",
        """<div class="demo-layout">
          <div class="cmd-block">
            <code>python scripts/setup_demo_models.py</code><br>
            <code>python run_demo.py</code><br>
            <code>python scripts/eval_tone_v1.py</code>
          </div>
          <div class="demo-shell">
            <div class="demo-chrome"><i></i><i></i><i></i> inference · local</div>
            <div class="demo-body">
              <div class="demo-echo"><span class="echo-ru">Курьер молодец,</span> <span class="echo-kz">уақытында әкелді</span></div>
              <div class="inf-row">
                <div class="inf-block"><p class="inf-k">Язык</p><p class="inf-big inf-big--mixed">MIXED</p></div>
                <div class="inf-block"><p class="inf-k">Тон</p><p class="inf-big inf-big--neg">Негатив</p></div>
              </div>
            </div>
          </div>
        </div>""",
        "Работает локально; limits на финальном слайде.",
    ),
    slide(
        19, "19 Limits",
        "Где границы проекта?",
        "Честные limits",
        "Один разметчик gold LID; κ не считали. Tone и LID на разных доменах (Telegram/Kaspi vs 2GIS). "
        "16&nbsp;364 mixed не аудированы на корпусе. Tone 97,33%: в основном LLM-label agreement. "
        "Telethon cells 31, 35, 41, 88 нельзя перезапускать. Student-scale исследование, не production NLP.",
        """<div class="limits-list">
          <div class="limit-item"><span>Разметка</span>Один annotator, без κ на kz/mixed borderline</div>
          <div class="limit-item"><span>Tone gold</span>94% LLM draft; метрика на согласованности</div>
          <div class="limit-item"><span>Корпус</span>16&nbsp;364 = model-predicted, human precision не измерялась</div>
          <div class="limit-item"><span>Repro</span>Run All не работает; CSV + eval_tone_v1.py + demo</div>
        </div>""",
        "Итог с тремя опорными числами.",
    ),
    slide(
        20, "20 Закрытие",
        "Главный итог проекта?",
        "Авто-LID в KZ соцмедиа шумит. Мы измерили, собрали gold и отфильтровали корпус",
        "Проект начался с «почему все пишут mixed». Ответ: измерение шума и gold 3&nbsp;076, не очередная архитектура. "
        "До: auto-LID → аналитика на шуме. После: filter-first pipeline с XLM-R v2 96,56% на честном test и локальным demo.",
        """<div class="close-nums">
          <div class="close-num"><div class="close-num__val num">~1,66% / 2,32%</div><div class="close-num__lbl">диагностика шума (эвристика)</div></div>
          <div class="close-num"><div class="close-num__val num" style="color:var(--pos)">96,56%</div><div class="close-num__lbl">LID macro-F1, n=461</div></div>
          <div class="close-num"><div class="close-num__val num" style="color:var(--ru)">97,33%</div><div class="close-num__lbl">tone mixed 2GIS, LLM caveat</div></div>
        </div>
        <p class="close-cta" style="margin-top:20px">STORY.md · main.ipynb · run_demo.py</p>""",
        "Filter-first LID для шала-казахского: измерили шум, доказали на gold, собрали demo.",
        manifesto=True,
    ),
]

JS = """
  <script>
    (function () {
      var stage = document.getElementById('deck-stage');
      var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
      var STORE = 'deck:idx:self:' + (location.pathname || '/');
      var idx = 0;
      function fit() {
        var sw = window.innerWidth, sh = window.innerHeight, pad = 32;
        var s = Math.min((sw - pad) / 1920, (sh - pad) / 1080);
        if (!isFinite(s) || s <= 0) s = 1;
        stage.style.transform = 'translate(' + ((sw - 1920 * s) / 2) + 'px,' + ((sh - 1080 * s) / 2) + 'px) scale(' + s + ')';
      }
      function paint() {
        slides.forEach(function (el, i) { el.classList.toggle('active', i === idx); });
        var counter = document.getElementById('deck-counter');
        if (counter) counter.textContent = String(idx + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
      }
      function go(i) {
        idx = Math.max(0, Math.min(slides.length - 1, i));
        paint();
        try { localStorage.setItem(STORE, String(idx)); } catch (_) {}
      }
      function onKey(e) {
        var t = e.target;
        if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) return;
        if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); go(idx + 1); }
        else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); go(idx - 1); }
        else if (e.key === 'Home') { e.preventDefault(); go(0); }
        else if (e.key === 'End') { e.preventDefault(); go(slides.length - 1); }
      }
      window.addEventListener('keydown', onKey, true);
      try {
        var saved = parseInt(localStorage.getItem(STORE) || '0', 10);
        if (!isNaN(saved) && saved >= 0 && saved < slides.length) idx = saved;
      } catch (_) {}
      window.addEventListener('resize', fit);
      fit(); paint();
    })();
  </script>
"""


def main() -> None:
    donor = CSS_DONOR.read_text(encoding="utf-8")
    start = donor.find("<style>")
    end = donor.find("</style>") + len("</style>")
    css_block = donor[start:end]
    css_block = css_block.replace(
        "padding: 56px 88px 48px;",
        "padding: 44px 64px 40px 0; flex-direction: row;",
    )
    # inject extra CSS before closing style tag
    css_block = css_block.replace("</style>", EXTRA_CSS + "\n  </style>")

    head = donor[:start]
    for old_title in (
        "<title>KazNLP - Story Deck Self (20 slides)</title>",
        "<title>KazNLP — Story Deck Self (20 slides)</title>",
    ):
        head = head.replace(old_title, "<title>KazNLP - Story Deck Self (20 slides)</title>")

    body = f"""{head}
{css_block}
</head>
<body>
  <div class="deck-shell">
    <div class="deck-stage" id="deck-stage">
{"".join(SLIDES)}
      <div class="deck-counter" id="deck-counter" aria-live="polite">01 / 20</div>
    </div>
  </div>
{JS}
</body>
</html>
"""
    OUT.write_text(body, encoding="utf-8")
    print(f"Wrote {OUT} (20 slides)")


if __name__ == "__main__":
    main()
