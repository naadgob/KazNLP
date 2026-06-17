"""Build web/story.html: narrative landing from index.html design + STORY.md."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "web" / "index.html"
OUT = ROOT / "web" / "story.html"
LABELER_ASSETS = ROOT / "web" / "assets" / "labeler"

# Drop screenshots into web/assets/labeler/ with these filenames (see user message in chat).
LABELER_SLIDES = [
    (
        "01-manual-language.png",
        "Ручная разметка языка",
        "Режим Language: RU / KZ / MIXED, метрики сессии и очередь unlabeled.",
    ),
    (
        "02-manual-sentiment.png",
        "Ручная разметка тона",
        "Режим Sentiment на mixed: positive / negative / skip, фильтр mixed tone unlabeled.",
    ),
    (
        "03-llm-batch.png",
        "LLM batch (только язык)",
        "Пакетная разметка языка через Ollama (ru / kz / mixed). Тон в этом режиме не размечается.",
    ),
]


def _labeler_carousel_html() -> str:
    slides: list[str] = []
    for i, (fname, title, caption) in enumerate(LABELER_SLIDES):
        src = LABELER_ASSETS / fname
        rel = f"assets/labeler/{fname}"
        if src.is_file():
            media = f'<img src="{rel}" alt="{title}" loading="lazy" width="1280" height="720">'
        else:
            media = (
                f'<div class="labeler-placeholder" role="img" aria-label="{title}">'
                f"<strong>{title}</strong>"
                f"<span>Скриншот: <code>web/assets/labeler/{fname}</code></span>"
                f"</div>"
            )
        active = " is-active" if i == 0 else ""
        slides.append(
            f"""        <div class="labeler-slide{active}" data-slide="{i}" role="group" aria-roledescription="slide" aria-label="{i + 1} из {len(LABELER_SLIDES)}">
          <figure>
            {media}
            <figcaption><strong>{title}</strong>{caption}</figcaption>
          </figure>
        </div>"""
        )
    dots = "".join(
        f'<button type="button" class="labeler-dot{" is-active" if i == 0 else ""}" data-goto="{i}" aria-label="Слайд {i + 1}"></button>'
        for i in range(len(LABELER_SLIDES))
    )
    return f"""      <div class="labeler-carousel motion-inview" id="labeler-carousel">
        <div class="labeler-carousel-viewport">
          <div class="labeler-carousel-track" id="labeler-track">
{chr(10).join(slides)}
          </div>
        </div>
        <div class="labeler-carousel-controls">
          <div class="labeler-carousel-nav">
            <button type="button" class="labeler-btn" id="labeler-prev" aria-controls="labeler-track">Назад</button>
            <button type="button" class="labeler-btn" id="labeler-next" aria-controls="labeler-track">Вперёд</button>
          </div>
          <div class="labeler-dots" role="tablist" aria-label="Слайды labeler">
            {dots}
          </div>
          <span class="labeler-counter" id="labeler-counter" aria-live="polite">1 / {len(LABELER_SLIDES)}</span>
        </div>
      </div>"""

EXTRA_CSS = """
    .section-light {
      background: var(--paper);
      color: var(--ink);
      padding-block: var(--space-7);
      border-top: 1px solid var(--line-dark);
      position: relative;
      isolation: isolate;
    }
    .section-light .section-head h2 { color: var(--ink); }
    .section-light.pipeline-band {
      background: var(--paper);
      border-block: 1px solid var(--line-dark);
      padding-block: var(--space-7);
    }
    .section-light.pipeline-band::before { display: none; }
    .section-light .section-head p { color: var(--muted); }
    .section-light .prose-block { color: #3f3f46; }
    .section-light .prose-block strong { color: var(--ink); }
    .section-light .research-card { border-top-color: var(--line-dark); }
    .section-light .research-chip { border-color: var(--line-dark); color: var(--muted); }
    .section-light .research-chip--production {
      border-color: var(--ink);
      color: var(--ink);
      background: rgba(0, 0, 0, 0.04);
    }
    .section-light .research-chip--pretrained { color: var(--muted); }
    .section-light .path-diagram {
      background: var(--white);
      border-color: var(--line-dark);
      color: #52525b;
    }
    .section-light .compare-card {
      background: var(--white);
      border-color: var(--line-dark);
    }
    .section-light .compare-caption { color: var(--muted); }
    .section-light .callout {
      border-color: var(--line-dark);
      background: var(--white);
    }
    .section-light .callout p { color: #52525b; }
    .section-light .stat .lbl { color: var(--muted); }
    .section-light .stat .val { color: var(--ink); }
    .section-light .stats {
      background: var(--line-dark);
      border-color: var(--line-dark);
    }
    .section-light .stat { background: var(--white); box-shadow: 0 1px 0 var(--line-dark); }
    .section-light .research-card-head h3 { color: var(--ink); }
    .section-light .compare-quote { color: var(--ink); }
    .section-light .research-row--conclusion .research-row-body {
      border-left-color: rgba(0, 0, 0, 0.12);
    }
    .section-light .research-row--conclusion p { color: #52525b; }
    .section-light .limits h3 { color: var(--ink); }
    .section-light .research-row-k { color: var(--muted); }
    .section-light .research-row p { color: #3f3f46; }
    .section-light .pain-grid {
      background: var(--line-dark);
      border-color: var(--line-dark);
    }
    .section-light .pain-grid > * { background: var(--paper); color: var(--ink); }
    .section-light .pain-grid .pain-h {
      background: var(--paper-2);
      color: var(--muted);
    }
    .section-light .limits {
      border-color: var(--line-dark);
      background: var(--white);
    }
    .section-light .limits li {
      border-color: var(--line-dark);
      color: #52525b;
    }
    .section-light .anchor-num { border-color: var(--line-dark); background: var(--white); }
    .section-light .anchor-num .lbl { color: var(--muted); }
    .section-light .story-links a { color: #52525b; }
    .section-light .story-links a:hover { color: var(--black); }
    .section-light .footer-line { border-color: var(--line-dark); color: var(--muted); }
    .section-light .goal-list li { color: #3f3f46; border-color: var(--line-dark); }
    .section-light .audience-item {
      border-color: var(--line-dark);
      background: var(--white);
      color: #3f3f46;
    }
    .section-light .audience-item strong { color: var(--ink); }
    .section-light .week-row { border-color: var(--line-dark); }
    .section-light .week-row span { color: var(--muted); }
    .section-light .pitch-box {
      border-color: var(--line-dark);
      background: var(--white);
      color: #3f3f46;
    }
    .section-light .pipe-light .pipe-schema-label { color: var(--muted); }
    .section-light .pipe-light .pipe-node {
      background: var(--white);
      border-color: var(--line-dark);
    }
    .section-light .pipe-light .pipe-node-t { color: var(--ink); }
    .section-light .pipe-light .pipe-node-k { color: var(--muted); }
    .section-light .pipe-light .pipe-connector-h,
    .section-light .pipe-light .pipe-node--route::after {
      background: rgba(0, 0, 0, 0.14);
    }
    .section-light .pipe-light .pipe-route-card {
      background: var(--white);
      border: 1px solid var(--line-dark);
    }
    .section-light .pipe-light .pipe-route-card h4 { color: var(--ink); }
    .section-light .pipe-light .pipe-route-card p { color: var(--muted); }
    .section-light .repro-block {
      background: var(--white);
      border-color: var(--line-dark);
      color: #52525b;
    }
    .section-light .repro-block code { color: var(--ink); }

    .act-label {
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--muted);
      margin: var(--space-5) 0 var(--space-2);
      padding-top: var(--space-3);
      border-top: 1px solid var(--line-dark);
    }
    .section-light .act-label { border-top-color: var(--line-dark); color: var(--muted); }
    .story-chain {
      font-family: var(--font-mono);
      font-size: 12px;
      line-height: 1.75;
      padding: var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      background: rgba(255, 255, 255, 0.02);
      margin: var(--space-4) 0;
      white-space: pre-line;
    }
    .section-light .story-chain {
      background: var(--white);
      border-color: var(--line-dark);
      color: #3f3f46;
    }
    .story-chain strong { color: var(--white); font-weight: 600; }
    .section-light .story-chain strong { color: var(--ink); }
    .glossary {
      margin-top: var(--space-4);
      padding: var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      max-width: 72ch;
      font-size: 14px;
      line-height: 1.55;
      color: var(--muted-light);
    }
    .section-light .glossary {
      border-color: var(--line-dark);
      background: var(--white);
      color: #52525b;
    }
    .glossary dt {
      font-weight: 600;
      color: var(--white);
      margin-top: 10px;
    }
    .section-light .glossary dt { color: var(--ink); }
    .glossary dt:first-child { margin-top: 0; }
    .glossary dd { margin: 4px 0 0; }
    .goal-primary {
      padding: var(--space-4);
      border: 1px solid rgba(212, 160, 36, 0.35);
      border-radius: var(--radius-md);
      background: rgba(212, 160, 36, 0.06);
      margin-bottom: var(--space-4);
      max-width: 72ch;
    }
    .goal-primary h3 {
      font-size: 20px;
      margin: 0 0 var(--space-2);
      letter-spacing: -0.02em;
      color: var(--mixed);
    }
    .goal-primary p { margin: 0; font-size: 16px; line-height: 1.55; color: var(--muted-light); }
    .section-light .goal-primary p { color: #52525b; }

    .story-hero .sub { max-width: 62ch; }
    .prose-block {
      max-width: 68ch;
      color: var(--muted-light);
      font-size: 17px;
      line-height: 1.62;
      margin-bottom: var(--space-4);
    }
    .prose-block p + p { margin-top: 1em; }
    .compare-duet {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--space-3);
      margin-top: var(--space-4);
    }
    @media (max-width: 768px) { .compare-duet { grid-template-columns: 1fr; } }
    .compare-card {
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      padding: var(--space-4);
      background: rgba(255, 255, 255, 0.02);
    }
    .compare-card--mixed { border-color: color-mix(in srgb, var(--mixed) 35%, transparent); }
    .compare-card--kz { border-color: color-mix(in srgb, var(--kz) 35%, transparent); }
    .compare-card .tag {
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: var(--space-2);
      display: inline-block;
    }
    .compare-card--mixed .tag { color: var(--mixed); }
    .compare-card--kz .tag { color: var(--kz); }
    .compare-quote {
      font-size: 18px;
      line-height: 1.45;
      margin-bottom: var(--space-2);
    }
    .compare-caption { font-size: 14px; color: var(--muted); }
    .path-diagram {
      font-family: var(--font-mono);
      font-size: 13px;
      line-height: 1.7;
      color: var(--muted-light);
      padding: var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      background: rgba(255, 255, 255, 0.02);
      margin: var(--space-4) 0;
      white-space: pre-line;
    }
    .pain-grid {
      display: grid;
      grid-template-columns: 1.1fr 1fr 1fr;
      gap: 1px;
      background: var(--line);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      overflow: hidden;
      margin-top: var(--space-4);
    }
    @media (max-width: 900px) { .pain-grid { grid-template-columns: 1fr; } }
    .pain-grid > * {
      background: var(--ink);
      padding: var(--space-3) var(--space-4);
      font-size: 14px;
      line-height: 1.5;
    }
    .pain-grid .pain-h {
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--muted);
      background: rgba(255, 255, 255, 0.03);
    }
    .goal-list {
      list-style: none;
      padding: 0;
      margin: var(--space-4) 0 0;
      max-width: 68ch;
      display: grid;
      gap: 0;
    }
    .goal-list li {
      padding: var(--space-2) 0;
      border-bottom: 1px solid var(--line);
      font-size: 16px;
      line-height: 1.5;
      color: var(--muted-light);
    }
    .goal-list li:last-child { border-bottom: none; }
    .audience-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: var(--space-3);
      margin-top: var(--space-4);
    }
    @media (max-width: 768px) { .audience-grid { grid-template-columns: 1fr; } }
    .audience-item {
      padding: var(--space-3) var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      font-size: 15px;
      line-height: 1.5;
      color: var(--muted-light);
    }
    .audience-item strong {
      display: block;
      font-size: 16px;
      color: var(--white);
      margin-bottom: 6px;
      letter-spacing: -0.01em;
    }
    .benchmark-ladder { margin-top: var(--space-4); display: grid; gap: 12px; max-width: 680px; }
    .bench-row {
      display: grid;
      grid-template-columns: 110px 1fr 72px;
      align-items: center;
      gap: 16px;
      font-size: 14px;
    }
    .bench-bar {
      height: 8px;
      background: rgba(255, 255, 255, 0.06);
      border-radius: 4px;
      overflow: hidden;
    }
    .section-light .bench-bar { background: rgba(0, 0, 0, 0.08); }
    .bench-fill {
      height: 100%;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.25);
    }
    .section-light .bench-fill { background: rgba(0, 0, 0, 0.18); }
    .bench-fill--win { background: var(--kz); }
    .section-light .bench-fill--win { background: var(--kz); }
    .bench-pct { font-family: var(--font-mono); text-align: right; }
    .bench-pct--win { color: var(--kz); font-weight: 600; }
    .bench-row--dim { opacity: 0.55; }
    .qualifier-box {
      margin-top: var(--space-4);
      padding: var(--space-4);
      border-radius: var(--radius-md);
      border: 1px solid color-mix(in srgb, var(--mixed) 40%, transparent);
      background: rgba(212, 160, 36, 0.06);
      max-width: 72ch;
      font-size: 15px;
      line-height: 1.55;
      color: var(--muted-light);
    }
    .section-light .qualifier-box {
      background: rgba(212, 160, 36, 0.08);
      color: #52525b;
    }
    .qualifier-box strong { color: var(--mixed); }
    .repro-block {
      font-family: var(--font-mono);
      font-size: 13px;
      line-height: 1.65;
      padding: var(--space-4);
      border-radius: var(--radius-md);
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.03);
      color: var(--muted-light);
    }
    .repro-block code { color: var(--white); }
    .anchor-nums {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: var(--space-3);
      margin-top: var(--space-5);
    }
    @media (max-width: 768px) { .anchor-nums { grid-template-columns: 1fr; } }
    .anchor-num {
      padding: var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
    }
    .anchor-num .val {
      font-family: var(--font-display);
      font-size: clamp(28px, 4vw, 40px);
      font-weight: 600;
      margin-bottom: 6px;
    }
    .anchor-num .lbl { font-size: 14px; color: var(--muted); line-height: 1.45; }
    .story-links {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-3);
      margin-top: var(--space-4);
    }
    .story-links a {
      font-size: 14px;
      color: var(--muted-light);
      text-decoration: underline;
      text-underline-offset: 3px;
    }
    .story-links a:hover { color: var(--white); }
    .heatmap-cell .num { font-size: clamp(16px, 1.4vw, 22px); }
    .limits li::before { content: '-'; }
    .limits {
      max-width: 720px;
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      padding: var(--space-4) var(--space-5);
    }
    .limits h3 { font-size: 20px; margin-bottom: var(--space-3); letter-spacing: -0.02em; }
    .limits ul { list-style: none; padding: 0; margin: 0; }
    .limits li {
      padding: var(--space-2) 0;
      border-bottom: 1px solid var(--line);
      font-size: 15px;
      color: var(--muted-light);
      padding-left: 16px;
      position: relative;
    }
    .limits li:last-child { border-bottom: none; }
    .sources-grid { margin-top: var(--space-5); max-width: 920px; }
    .sources-grid h3 {
      font-size: 20px;
      letter-spacing: -0.02em;
      margin-bottom: var(--space-3);
    }
    .sources-list {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: var(--space-2);
    }
    @media (max-width: 768px) { .sources-list { grid-template-columns: 1fr; } }
    .source-item {
      display: flex;
      flex-direction: column;
      gap: 6px;
      padding: var(--space-3);
      border: 1px solid var(--line-dark);
      border-radius: var(--radius-md);
      background: var(--white);
      font-size: 13px;
      line-height: 1.5;
      color: #52525b;
    }
    .source-item strong {
      display: block;
      color: var(--ink);
      font-size: 14px;
      margin-bottom: 0;
    }
    .source-item code {
      display: block;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--muted);
      line-height: 1.45;
      word-break: break-word;
    }
    .source-item .src-status {
      display: inline-block;
      align-self: flex-start;
      margin-top: 2px;
      padding: 3px 8px;
      border-radius: var(--radius-pill);
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      background: rgba(0, 0, 0, 0.04);
    }
    .source-item .src-status--ok { color: var(--positive); background: rgba(34, 179, 104, 0.1); }
    .source-item .src-status--no { color: var(--negative); background: rgba(224, 69, 69, 0.1); }
    .source-item .src-status--caveat { color: var(--mixed); background: rgba(212, 160, 36, 0.12); }
    .pitch-box {
      margin-top: var(--space-5);
      padding: var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      font-size: 17px;
      line-height: 1.55;
      color: var(--muted-light);
      max-width: 68ch;
    }
    .pitch-box cite {
      display: block;
      margin-top: var(--space-3);
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--muted);
      font-style: normal;
    }
    .week-grid {
      margin-top: var(--space-4);
      display: grid;
      gap: 0;
      max-width: 560px;
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      overflow: hidden;
    }
    .section-light .week-grid { border-color: var(--line-dark); }
    .week-row {
      display: grid;
      grid-template-columns: 72px 1fr;
      gap: var(--space-3);
      padding: var(--space-2) var(--space-3);
      border-bottom: 1px solid var(--line);
      font-size: 14px;
      line-height: 1.45;
    }
    .week-row:last-child { border-bottom: none; }
    .week-row span {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--muted);
      padding-top: 2px;
    }
    .before-after {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--space-3);
      margin-top: var(--space-4);
      max-width: 72ch;
    }
    @media (max-width: 768px) { .before-after { grid-template-columns: 1fr; } }
    .before-after > div {
      padding: var(--space-3) var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      font-size: 14px;
      line-height: 1.55;
      color: var(--muted-light);
    }
    .section-light .before-after > div {
      border-color: var(--line-dark);
      background: var(--white);
      color: #52525b;
    }
    .before-after strong {
      display: block;
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 8px;
      color: var(--muted);
    }
    .pipe-light { margin-top: var(--space-4); }
    .tone-cm {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1px;
      max-width: 280px;
      margin-top: var(--space-3);
      background: var(--line);
      border-radius: var(--radius-md);
      overflow: hidden;
    }
    .tone-cm span {
      padding: 20px;
      text-align: center;
      background: rgba(255, 255, 255, 0.04);
      font-size: 20px;
      font-weight: 600;
    }
    .tone-cm .pos { background: rgba(34, 179, 104, 0.2); color: var(--positive); }
    .tone-cm .neg { background: rgba(224, 69, 69, 0.15); color: var(--negative); }
    .hero-caveat {
      margin-top: var(--space-3);
      padding: var(--space-3) var(--space-4);
      border: 1px solid color-mix(in srgb, var(--mixed) 35%, transparent);
      border-radius: var(--radius-md);
      background: rgba(212, 160, 36, 0.06);
      font-size: 14px;
      line-height: 1.55;
      color: var(--muted-light);
      max-width: 62ch;
    }
    .hero-caveat strong { color: var(--mixed); font-weight: 600; }
    .journey-intro {
      max-width: 72ch;
      font-size: 16px;
      line-height: 1.62;
      color: #52525b;
      margin-bottom: var(--space-4);
    }
    .journey-intro p + p { margin-top: 0.85em; }
    .chapter-map {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: var(--space-2);
      margin: var(--space-4) 0;
      font-size: 13px;
      line-height: 1.45;
    }
    @media (max-width: 900px) { .chapter-map { grid-template-columns: 1fr 1fr; } }
    @media (max-width: 560px) { .chapter-map { grid-template-columns: 1fr; } }
    .chapter-map-item {
      padding: var(--space-2) var(--space-3);
      border: 1px solid var(--line-dark);
      border-radius: var(--radius-md);
      background: var(--white);
      color: #52525b;
    }
    .chapter-map-item strong {
      display: block;
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 4px;
    }
    .journey-callout {
      margin: var(--space-4) 0;
      padding: var(--space-3) var(--space-4);
      border: 1px solid var(--line-dark);
      border-radius: var(--radius-md);
      background: var(--white);
      font-size: 14px;
      line-height: 1.55;
      color: #52525b;
      max-width: 72ch;
    }
    .journey-callout strong { color: var(--ink); }
    .method-box {
      margin-top: var(--space-4);
      padding: var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      background: rgba(255, 255, 255, 0.03);
      max-width: 72ch;
      font-size: 15px;
      line-height: 1.55;
      color: var(--muted-light);
    }
    .method-box h4 {
      margin: 0 0 var(--space-2);
      font-size: 14px;
      letter-spacing: -0.01em;
      color: var(--white);
    }
    .method-box ul { margin: 0; padding-left: 1.1em; }
    .method-box li + li { margin-top: 6px; }
    .section-light .method-box {
      border-color: var(--line-dark);
      background: var(--white);
      color: #52525b;
    }
    .section-light .method-box h4 { color: var(--ink); }
    .limits-top {
      margin-bottom: var(--space-4);
      max-width: 720px;
    }
    .limits-top li {
      padding: var(--space-2) 0;
      border-bottom: 1px solid var(--line-dark);
      font-size: 15px;
      color: #52525b;
      list-style: none;
      padding-left: 0;
    }
    .limits-top li:last-child { border-bottom: none; }
    .research-timeline { display: flex; flex-direction: column; gap: 0; }
    #product.pipeline-band,
    #product.pipeline-band.section-dark {
      overflow: visible;
      padding-bottom: var(--space-8);
    }
    #product .pipe-schema,
    #product .pipe-schema-branch,
    #product .container {
      overflow: visible;
    }
    body > .pill-nav-wrap.is-sticky {
      background: transparent;
      border-bottom: none;
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
    }
    .labeler-section { padding-block: var(--space-7); }
    .labeler-carousel {
      margin-top: var(--space-4);
      position: relative;
    }
    .labeler-carousel-viewport {
      overflow: hidden;
      border: 1px solid var(--line-dark);
      border-radius: var(--radius-md);
      background: var(--white);
    }
    .labeler-carousel-track {
      display: flex;
      transition: transform 520ms cubic-bezier(0.22, 1, 0.36, 1);
    }
    .labeler-slide {
      flex: 0 0 100%;
      min-width: 100%;
    }
    .labeler-slide figure { margin: 0; }
    .labeler-slide img {
      display: block;
      width: 100%;
      height: auto;
      max-height: min(62vh, 640px);
      object-fit: contain;
      background: #f4f4f5;
    }
    .labeler-slide figcaption {
      padding: var(--space-3) var(--space-4);
      font-size: 14px;
      line-height: 1.5;
      color: #52525b;
      border-top: 1px solid var(--line-dark);
    }
    .labeler-slide figcaption strong {
      display: block;
      color: var(--ink);
      font-size: 15px;
      margin-bottom: 4px;
    }
    .labeler-placeholder {
      min-height: 320px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      padding: var(--space-5);
      text-align: center;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.5;
      background: linear-gradient(180deg, #fafafa, #f0f0f1);
    }
    .labeler-placeholder code {
      font-family: var(--font-mono);
      font-size: 12px;
      color: #71717a;
    }
    .labeler-carousel-controls {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: var(--space-3);
      margin-top: var(--space-3);
    }
    .labeler-carousel-nav {
      display: flex;
      gap: 8px;
    }
    .labeler-btn {
      font-family: var(--font-mono);
      font-size: 12px;
      letter-spacing: 0.04em;
      padding: 8px 14px;
      border: 1px solid var(--line-dark);
      border-radius: var(--radius-pill);
      background: var(--white);
      color: var(--ink);
      cursor: pointer;
      transition: background 180ms ease, border-color 180ms ease;
    }
    .labeler-btn:hover { background: #f4f4f5; }
    .labeler-btn:focus-visible {
      outline: 2px solid var(--ink);
      outline-offset: 2px;
    }
    .labeler-dots {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: center;
      flex: 1;
    }
    .labeler-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      border: none;
      padding: 0;
      background: rgba(0, 0, 0, 0.18);
      cursor: pointer;
    }
    .labeler-dot.is-active { background: var(--ink); }
    .labeler-dot:focus-visible {
      outline: 2px solid var(--ink);
      outline-offset: 2px;
    }
    .labeler-counter {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--muted);
      white-space: nowrap;
    }
    @media (max-width: 640px) {
      .labeler-carousel-controls { flex-wrap: wrap; }
      .labeler-counter { width: 100%; text-align: center; }
    }
"""

MINIMAL_JS = """
  <script>
    (function () {
      var $ = function (s) { return document.querySelector(s); };
      var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

      function onScroll() {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        document.documentElement.style.setProperty('--scroll-p', h > 0 ? window.scrollY / h : 0);
        var wrap = $('#nav-wrap');
        if (wrap) wrap.classList.toggle('is-sticky', window.scrollY > 100);
      }
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();

      $$('[data-scroll]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          var id = a.getAttribute('data-scroll');
          if (!id) return;
          var el = document.getElementById(id);
          if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        });
      });

      var links = $$('.nav-links a[data-scroll]');
      var sections = $$('section[id]');
      var lightSections = { problem: 1, journey: 1, tone: 1, limits: 1, labeler: 1 };
      if (links.length && sections.length) {
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (!en.isIntersecting) return;
            var id = en.target.id;
            links.forEach(function (l) {
              var active = l.getAttribute('data-scroll') === id;
              l.classList.toggle('is-active', active);
              if (active) l.setAttribute('aria-current', 'true');
              else l.removeAttribute('aria-current');
            });
            var wrap = $('#nav-wrap');
            if (wrap) wrap.classList.toggle('nav-on-light', !!lightSections[id]);
          });
        }, { rootMargin: '-35% 0px -55% 0px', threshold: 0 });
        sections.forEach(function (s) { io.observe(s); });
      }

      var productBand = $('#product');
      if (productBand) productBand.classList.add('is-visible');

      (function initLabelerCarousel() {
        var carousel = $('#labeler-carousel');
        var track = $('#labeler-track');
        if (!carousel || !track) return;
        var slides = Array.prototype.slice.call(carousel.querySelectorAll('.labeler-slide'));
        var dots = Array.prototype.slice.call(carousel.querySelectorAll('.labeler-dot'));
        var counter = $('#labeler-counter');
        var prev = $('#labeler-prev');
        var next = $('#labeler-next');
        var idx = 0;
        var total = slides.length;
        function go(n) {
          idx = (n + total) % total;
          track.style.transform = 'translateX(' + (-idx * 100) + '%)';
          slides.forEach(function (s, i) { s.classList.toggle('is-active', i === idx); });
          dots.forEach(function (d, i) { d.classList.toggle('is-active', i === idx); });
          if (counter) counter.textContent = (idx + 1) + ' / ' + total;
        }
        if (prev) prev.addEventListener('click', function () { go(idx - 1); });
        if (next) next.addEventListener('click', function () { go(idx + 1); });
        dots.forEach(function (d) {
          d.addEventListener('click', function () {
            var n = parseInt(d.getAttribute('data-goto'), 10);
            if (!isNaN(n)) go(n);
          });
        });
        document.addEventListener('keydown', function (e) {
          if (!track.closest('#labeler')) return;
          if (e.key === 'ArrowLeft') go(idx - 1);
          if (e.key === 'ArrowRight') go(idx + 1);
        });
      })();

      var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      function revealVisible() {
        $$('.motion-inview, .motion-research').forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.top < window.innerHeight * 0.92 && r.bottom > 0) el.classList.add('is-visible');
        });
      }
      $$('.motion-inview, .motion-research').forEach(function (el) {
        if (reduced) el.classList.add('is-visible');
      });
      if (!reduced) {
        var io2 = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) e.target.classList.add('is-visible');
          });
        }, { threshold: 0.08, rootMargin: '0px 0px -8% 0px' });
        $$('.motion-inview, .motion-research').forEach(function (el) { io2.observe(el); });
        var band = $('#product');
        if (band) {
          var io3 = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
              if (e.isIntersecting) e.target.classList.add('is-visible');
            });
          }, { threshold: 0.15 });
          io3.observe(band);
        }
        revealVisible();
        window.addEventListener('load', revealVisible);
        window.addEventListener('hashchange', function () { setTimeout(revealVisible, 80); });
      } else {
        var band = $('#product');
        if (band) band.classList.add('is-visible');
      }
    })();
  </script>
"""

BODY = """
  <div class="ambient-layer" aria-hidden="true">
    <div class="global-grain"></div>
    <div class="scroll-progress" aria-hidden="true"></div>
  </div>
  <div class="ambient-track" aria-hidden="true">
    <div class="ambient-spot ambient-spot--1 is-visible"></div>
    <div class="ambient-spot ambient-spot--2 is-visible"></div>
    <div class="ambient-spot ambient-spot--3"></div>
    <div class="ambient-spot ambient-spot--4"></div>
    <div class="ambient-spot ambient-spot--5"></div>
  </div>

  <div class="pill-nav-wrap nav-entered" id="nav-wrap">
    <div class="pill-nav-anchor">
      <nav class="pill-nav" id="pill-nav" aria-label="Навигация по истории">
        <div class="nav-brand-slot">
          <span class="brand"><span class="brand-mark" aria-hidden="true">KZ</span>KazNLP</span>
        </div>
        <div class="nav-links">
          <a href="#problem" data-scroll="problem">Зачем</a>
          <a href="#goal" data-scroll="goal">Цель</a>
          <a href="#journey" data-scroll="journey">Путь</a>
          <a href="#lid" data-scroll="lid">Фильтр</a>
          <a href="#tone" data-scroll="tone">Тон</a>
          <a href="#product" data-scroll="product">Продукт</a>
          <a href="#labeler" data-scroll="labeler">Разметка</a>
          <a href="#limits" data-scroll="limits">Ограничения</a>
          <a href="#close" data-scroll="close">Итог</a>
        </div>
        <div class="nav-cta-slot">
          <a href="index.html#demo" class="cta">Попробовать</a>
        </div>
      </nav>
    </div>
  </div>

  <section class="hero story-hero motion-ready" id="hero">
    <div class="hero-grain" aria-hidden="true"></div>
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="container hero-grid">
      <div class="hero-eyebrow mono">
        <p>История проекта</p>
        <p class="hero-meta">Samsung Innovation Campus · Bogdan Savelyev</p>
      </div>
      <div class="hero-main">
        <h1><span class="h1-reg">Тональность</span> <span class="h1-em">смешанных отзывов</span></h1>
        <p class="sub">Capstone KazNLP: классифицировать тон (позитив / негатив) на отзывах 2GIS, где в одном тексте смешаны русский и казахский. Без честного фильтра ru / kz / mixed нельзя собрать обучающую выборку: auto-LID на Telegram врёт, kz с заёмным словом попадает в mixed.</p>
        <div class="hero-caveat">
          <strong>Честно о метриках.</strong> Tone v1 <span class="num">97,33%</span> на test <span class="num">n=525</span>: это agreement с LLM-разметкой на hold-out (~<span class="num">94%</span> gold от <code>llm_composer</code>), не независимая экспертиза. LID v2 <span class="num">96,56%</span> macro-F1 на gold test <span class="num">n=461</span> (ручной эталон). Подробности: секции <a href="#tone" data-scroll="tone" style="text-decoration:underline;color:inherit">Тон</a> и <a href="#limits" data-scroll="limits" style="text-decoration:underline;color:inherit">Ограничения</a>.
        </div>
      </div>
      <div class="hero-pipeline">
        <div class="pipeline-flow" aria-label="Pipeline">
          <span class="pipe-node">TEXT</span>
          <span class="pipe-line" aria-hidden="true"></span>
          <span class="pipe-node">LID</span>
          <span class="pipe-line" aria-hidden="true"></span>
          <span class="pipe-node">ROUTE</span>
          <span class="pipe-line" aria-hidden="true"></span>
          <span class="pipe-node">TONE</span>
        </div>
      </div>
      <div class="hero-bottom">
        <a href="#problem" class="hero-cta" data-scroll="problem">Читать историю</a>
        <p class="hero-aside">
          Deliverable: Tone v1 · <span class="num">3&nbsp;529</span> gold mixed<br>
          Опора: LID v2 · <span class="num">3&nbsp;076</span> gold LID · filter-first demo
        </p>
      </div>
    </div>
  </section>

  <section class="section-light" id="problem">
    <div class="container">
      <div class="section-head motion-inview">
        <h2>С чего начинался capstone</h2>
        <p>Задача: классифицировать тональность отзывов, где в одном сообщении смешаны русский и казахский (шала-казахский, code-switch).</p>
      </div>
      <div class="prose-block motion-inview">
        <p><strong>Что хотел получить.</strong> Модель, которая на входе получает сырой текст отзыва с 2GIS и на выходе говорит: позитив или негатив. Домен mixed: в одной фразе может быть «обслуживание тоже на уровне» и «рахмет, өте дәмді». Для ru-only и kz-only в продукте используются готовые RuBERT и Kazakh BERT; для mixed нужна отдельная fine-tuned модель (Tone v1 на XLM-RoBERTa).</p>
        <p><strong>Что мешало сразу учить tone.</strong> Чтобы собрать обучающую выборку «только mixed», нужно отделить mixed от ru и kz. При сборе корпуса Telegram колонка <code>language</code> ставится FastText v1: это метка сборщика, не эталон. На реальных данных почти всё помечается как mixed, хотя большая часть строк на самом деле монолингвальный казахский с русским заёмным словом. Если учить тональность на такой выборке, в неё попадёт kz-with-loanword вместо настоящего code-switch.</p>
        <p><strong>Вывод.</strong> Тональность mixed была целью capstone с первого дня. LID (language identification: ru / kz / mixed) пришлось построить как обязательный шаг: filter-first, сначала язык, потом тон.</p>
        <p><strong>Зачем это бизнесу.</strong> Платформа вроде 2GIS получает тысячи отзывов в день. Если mixed-отзыв ошибочно уходит в ветку «чистый казахский», тональность считается не той моделью; жалоба может попасть не в тот сценарий эскалации. KazNLP не интегрирован в продакшен, но показывает, какой pipeline нужен для честной маршрутизации.</p>
      </div>
      <dl class="glossary motion-inview">
        <dt>Шала-казахский / code-switch</dt>
        <dd>Переключение между русским и казахским в одном сообщении. Не путать с казахским предложением, где одно слово заимствовано из русского.</dd>
        <dt>LID (language ID)</dt>
        <dd>Классификация текста на ru, kz или mixed. В проекте: XLM-RoBERTa v2, обучен на ручном gold <span class="num">3&nbsp;076</span> строк.</dd>
        <dt>Gold</dt>
        <dd>Ручная разметка с фиксированным протоколом split. Для LID: test <span class="num">461</span> строк только gold. Для tone: test <span class="num">525</span> mixed-отзывов 2GIS.</dd>
      </dl>
      <div class="stats motion-inview">
        <div class="stat"><div class="val num">3&nbsp;529</div><div class="lbl">gold tone (2GIS mixed)</div></div>
        <div class="stat"><div class="val num">422&nbsp;141</div><div class="lbl">Telegram (контекст LID)</div></div>
        <div class="stat"><div class="val num">39&nbsp;129</div><div class="lbl">Kaspi (контекст LID)</div></div>
      </div>
      <div class="compare-duet motion-inview">
        <article class="compare-card compare-card--mixed">
          <span class="tag">mixed · code-switch</span>
          <p class="compare-quote">«Курьер молодец, уақытында әкелді»</p>
          <p class="compare-caption">Две языковые фразы. Такие тексты нужны для обучения Tone v1.</p>
        </article>
        <article class="compare-card compare-card--kz">
          <span class="tag">kz · заём, не mixed</span>
          <p class="compare-quote">«Качествосы жақсы, арзан»</p>
          <p class="compare-caption">Казахская грамматика (-сы), один язык. Наивный LID часто ошибочно ставит mixed.</p>
        </article>
      </div>
      <div class="callout motion-inview" style="margin-top: var(--space-5)">
        <strong>Блокер, который пришлось снять</strong>
        <p>Пока auto-LID путает kz с mixed, нельзя честно собрать выборку для тональности. Поэтому в ноутбуке сначала идут главы про диагностику шума и gold LID (cells 0-176), и только потом глава про tone (cells 238-264).</p>
      </div>
    </div>
  </section>

  <section class="section-dark" id="goal">
    <div class="container">
      <div class="section-head motion-inview">
        <h2>Цель и результат capstone</h2>
        <p>Две связанные задачи: тональность на mixed (главная) и фильтр языка (без него первая невозможна).</p>
      </div>
      <div class="goal-primary motion-inview">
        <h3>Главная цель: mixed tone classification</h3>
        <p>Классификатор тональности для смешанных отзывов 2GIS. Production-модель Tone v1 на hold-out test <span class="num">n=525</span>. Полные метрики, confusion matrix и оговорки про LLM-labels: секция <a href="#tone" data-scroll="tone" style="text-decoration:underline;color:inherit">Тон</a>.</p>
      </div>
      <ul class="goal-list motion-inview">
        <li><strong>Опора (не самоцель):</strong> фильтр ru / kz / mixed с macro-F1 <span class="num">96,56%</span> на gold test <span class="num">n=461</span>. Доказательства: секция <a href="#lid" data-scroll="lid" style="text-decoration:underline;color:inherit">Фильтр</a>.</li>
        <li><strong>Корпус:</strong> <code>main.csv</code> <span class="num">331&nbsp;468</span> строк с метками LID v2; <span class="num">16&nbsp;364</span> кандидата в mixed по предсказанию модели (не human-audited).</li>
        <li><strong>Продукт:</strong> cascade TEXT → LID → route → tone, локальный demo API и сервис разметки gold.</li>
      </ul>
      <div class="method-box motion-inview">
        <h4>Как читать метрики на защите</h4>
        <ul>
          <li><strong>Tone 97,33%:</strong> accuracy на gold test <span class="num">525</span> mixed 2GIS. ~<span class="num">488/525</span> test-строк размечены <code>llm_composer</code>; метрика отражает согласие модели с LLM, не blind human eval.</li>
          <li><strong>LID 96,56%:</strong> macro-F1 на ручном gold test <span class="num">461</span>. 14 из 16 ошибок: путаница kz ↔ mixed (см. CM в секции Фильтр).</li>
          <li><strong>1,66% и 2,32%:</strong> диагностика эвристики <code>is_real_mixed()</code> и precision FT v2 на корпусе, не доля mixed в Telegram.</li>
          <li><strong>Домены:</strong> LID учил на Telegram/Kaspi; tone на mixed 2GIS. End-to-end F1 cascade на 2GIS не измерял.</li>
        </ul>
      </div>
      <div class="pain-grid motion-inview">
        <div class="pain-h">Вопрос</div><div class="pain-h">Без KazNLP</div><div class="pain-h">С KazNLP</div>
        <div>Можно ли учить tone на mixed?</div><div>Нет: в «mixed» попадает kz с заёмом</div><div>Да: gold tone <span class="num">3&nbsp;529</span> mixed 2GIS, test <span class="num">525</span></div>
        <div>Как отфильтровать mixed?</div><div>FastText / эвристики: precision mixed на корпусе <span class="num">2,32%</span></div><div>XLM-R LID v2, gold test <span class="num">96,56%</span></div>
        <div>Как проверить на защите?</div><div>«Ещё один BERT 97%» без контекста</div><div>Filter-first pipeline + честные оговорки</div>
        <div>Воспроизводимость</div><div>Только ноутбук</div><div>Веса на диске, eval-скрипты, defense path</div>
      </div>
      <div class="prose-block motion-inview" style="margin-top: var(--space-5); margin-bottom: 0">
        <p>Формулировка из Final Report: «высокоточный фильтр ru / kz / mixed <strong>и</strong> тональность для подтверждённого mixed». LID занял большую часть исследовательского времени, потому что без него тональность строилась бы на шумных метках. Это не смена цели, а порядок работ в <code>main.ipynb</code>.</p>
      </div>
    </div>
  </section>

  <section class="section-light" id="journey">
    <div class="container">
      <div class="section-head motion-inview">
        <h2>Путь в main.ipynb</h2>
        <p>270 ячеек, 9 глав. Сначала снял блокер LID (главы 1-6), затем применил к корпусу (гл. 7), обучил tone (гл. 8), собрал продукт (гл. 9).</p>
      </div>
      <div class="journey-intro motion-inview">
        <p><strong>Как читать эту секцию.</strong> Ниже карточки идут в порядке <em>выполнения</em> в ноутбуке (cells 0 → 264). Исключение: §10 «baseline ladder» (cells 267-268) стоит в конце файла, но сравнивает все модели на одном gold test <span class="num">n=461</span>, собранном в главе 5. Это приложение к оценке, не отдельный этап исследования.</p>
        <p><strong>Почему так много про LID, если цель tone?</strong> Без честного разделения ru / kz / mixed нельзя отобрать 3 529 mixed-отзывов для tone gold. Главы 1-6 заняли ~70% исследовательского времени, потому что auto-labels на <span class="num">422k</span> Telegram давали ложный mixed почти везде.</p>
      </div>
      <div class="story-chain motion-inview"><strong>1. Цель</strong>       → mixed tone на 2GIS (секция Зачем)
<strong>2. Блокер</strong>    → auto-LID врёт: kz+заём ≠ code-switch
<strong>3. Тупики</strong>    → гл. 1-4 · cells 0-113
<strong>4. Gold + LID</strong> → гл. 5-6 · cells 114-176
<strong>5. §10 ladder</strong> → cells 267-268 · eval на test 461
<strong>6. Корпус</strong>   → гл. 7 · cells 177-237
<strong>7. Tone v1</strong>  → гл. 8 · cells 238-264
<strong>8. Продукт</strong>  → гл. 9 · inference + demo</div>
      <div class="chapter-map motion-inview" aria-label="Карта глав ноутбука">
        <div class="chapter-map-item"><strong>Гл. 1</strong>Синтетика 480k · cells 0-21</div>
        <div class="chapter-map-item"><strong>Гл. 2</strong>Telegram 422k · cells 22-44</div>
        <div class="chapter-map-item"><strong>Гл. 3</strong>Диагностика шума · cells 45-64</div>
        <div class="chapter-map-item"><strong>Гл. 4</strong>Правила, Lingua · cells 65-113</div>
        <div class="chapter-map-item"><strong>Гл. 5</strong>Gold LID 3 076 · cells 114-153</div>
        <div class="chapter-map-item"><strong>Гл. 6</strong>XLM-R LID v2 · cells 154-176</div>
        <div class="chapter-map-item"><strong>Гл. 7</strong>main.csv 331k · cells 177-237</div>
        <div class="chapter-map-item"><strong>Гл. 8</strong>Tone v1 · cells 238-264</div>
        <div class="chapter-map-item"><strong>Гл. 9</strong>Продукт · demo API</div>
      </div>
      <div class="research-timeline">
        <p class="act-label motion-inview">Акт I · Цель и блокер (до cells 0)</p>
        <div class="journey-callout motion-inview">
          <strong>Контекст.</strong> Capstone я начал с задачи тональности на mixed 2GIS. Уже на этапе сбора Telegram выяснил: колонка <code>language</code> = FastText при сборе, не ground truth. Пока не измерил масштаб шума и не собрал ручной эталон, к tone перейти нельзя. Подробнее: секция <a href="#problem" data-scroll="problem">Зачем</a>.
        </div>
        <p class="act-label motion-inview">Акт II · Тупики (гл. 1-4 · cells 0-113)</p>
        <article class="research-card motion-research">
          <div class="research-card-head">
            <span class="mono">01</span>
            <h3>Синтетика 480k</h3>
            <span class="research-chip research-chip--baseline">гл. 1 · cells 0-21</span>
          </div>
          <div class="research-rows">
            <div class="research-row"><span class="research-row-k">Что делал</span><p>Собрал синтетический mixed из KazSAnDRA (<span class="num">180&nbsp;064</span>), clapAI ru (<span class="num">164&nbsp;148</span>) и словарей popular/essential. Обучил FastText v1.</p></div>
            <div class="research-row"><span class="research-row-k">Результат</span><p>F1 <span class="num">84,96%</span> на synthetic test n=<span class="num">96&nbsp;000</span>.</p></div>
            <div class="research-row research-row--conclusion"><span class="research-row-k">Почему отклонён</span><div class="research-row-body"><p>Красивый F1 на синтетике не переносится на реальные Telegram-тексты. Для tone это тупик: фильтр языка на синтетике не доказывает качество на 2GIS.</p></div></div>
          </div>
        </article>
        <article class="research-card motion-research">
          <div class="research-card-head">
            <span class="mono">02</span>
            <h3>Реальный Telegram</h3>
            <span class="research-chip research-chip--baseline">гл. 2 · cells 22-44</span>
          </div>
          <div class="research-rows">
            <div class="research-row"><span class="research-row-k">Что делал</span><p>Собирал комментарии из Telegram-каналов (Telethon). При сборе каждой строке ставил <code>language</code> через FastText v1.</p></div>
            <div class="research-row"><span class="research-row-k">Рост</span><p><span class="num">146&nbsp;206</span> → <span class="num">241&nbsp;576</span> → <span class="num">422&nbsp;141</span> строк на диске (<code>telegram_code-switch_dataset.csv</code>).</p></div>
            <div class="research-row research-row--conclusion"><span class="research-row-k">Что выяснил</span><div class="research-row-body"><p>Ключевой вопрос: сколько строк с меткой mixed это настоящий code-switch, а сколько kz с одним русским словом? Без ответа нельзя ни строить LID, ни отбирать mixed для tone gold.</p></div></div>
          </div>
        </article>
        <article class="research-card motion-research">
          <div class="research-card-head">
            <span class="mono">03</span>
            <h3>Диагностика шума</h3>
            <span class="research-chip research-chip--baseline">гл. 3 · cells 45-64</span>
          </div>
          <div class="research-rows">
            <div class="research-row"><span class="research-row-k">Что делал</span><p>На срезе <span class="num">27&nbsp;628</span> строк с меткой FT-mixed прогнал узкую эвристику <code>is_real_mixed()</code> (и казахские ә/ң, и русская кириллица в одном тексте). Отдельно: FT v2 relabel на корпусе.</p></div>
            <div class="research-row"><span class="research-row-k">Цифры</span><p>Эвристика пропустила <span class="num">460</span> из <span class="num">27&nbsp;628</span> (~<span class="num">1,66%</span>): это TP эвристики, не prevalence mixed в корпусе. После FT v2 relabel: precision mixed <span class="num">2,32%</span> (<span class="num">1&nbsp;542/66&nbsp;462</span>).</p></div>
            <div class="research-row"><span class="research-row-k">Seeds</span><p>Пул <span class="num">868</span> кандидатов (не gold; пропускает shala-Kazakh без ә/ң).</p></div>
            <div class="research-row research-row--conclusion"><span class="research-row-k">Вывод</span><div class="research-row-body"><p>Auto-labels массово помечают kz как mixed. Короткие пути (добавить синтетику, relabel FT) не дают честный фильтр. Нужен ручной gold и модель, которая видит фразу целиком.</p></div></div>
          </div>
        </article>
        <article class="research-card motion-research">
          <div class="research-card-head">
            <span class="mono">04</span>
            <h3>Правила и Lingua</h3>
            <span class="research-chip research-chip--rejected">гл. 4 · cells 65-113</span>
          </div>
          <div class="research-rows">
            <div class="research-row"><span class="research-row-k">Что делал</span><p>Пробовал rule-based фильтры и Lingua (off-the-shelf LID). Lingua v2 прошёл <span class="num">411k</span> строк → <span class="num">6&nbsp;517</span> кандидатов в mixed. FT v2: recall <span class="num">95,51%</span> на seeds, но precision <span class="num">2,32%</span> на полном корпусе.</p></div>
            <div class="research-row"><span class="research-row-k">Lingua на seeds</span><p>v1 <span class="num">71,66%</span> · v2 <span class="num">95,97%</span> на пуле <span class="num">868</span> (ещё не gold test).</p></div>
            <div class="research-row"><span class="research-row-k">LLM для gold</span><p>Отвергнут: высокий false positive на mixed при автоматической разметке LID.</p></div>
            <div class="research-row research-row--conclusion"><span class="research-row-k">Вывод</span><div class="research-row-body"><p>Правила и Lingua не заменяют ручной эталон. Позже, на gold test <span class="num">n=461</span> (§10, cells 267-268), Lingua v2 даст macro-F1 <span class="num">88,63%</span> vs XLM-R <span class="num">96,56%</span>. См. ladder в секции Фильтр.</p></div></div>
          </div>
        </article>
        <p class="act-label motion-research">Акт III · Gold и LID v2 (гл. 5-6 · cells 114-176)</p>
        <article class="research-card motion-research">
          <div class="research-card-head">
            <span class="mono">05</span>
            <h3>Gold LID</h3>
            <span class="research-chip research-chip--production">гл. 5 · cells 114-153</span>
          </div>
          <div class="research-rows">
            <div class="research-row"><span class="research-row-k">Что делал</span><p>Ручная разметка ru / kz / mixed по протоколу. Очистка cheap_clean: <span class="num">388&nbsp;748</span> → <span class="num">254&nbsp;601</span> строка.</p></div>
            <div class="research-row"><span class="research-row-k">Состав</span><p><span class="num">3&nbsp;076</span> gold: ru <span class="num">1&nbsp;000</span> · kz <span class="num">999</span> · mixed <span class="num">1&nbsp;077</span> после dedup.</p></div>
            <div class="research-row"><span class="research-row-k">Протокол</span><p>Split 80/10/10 → test <span class="num">461</span> gold-only (<code>data/training/filter/v1/test.csv</code>). Synthetic 538 только в train. Вес gold:synthetic <span class="num">3:1</span>.</p></div>
            <div class="research-row"><span class="research-row-k">Важно</span><p>XLM-R обучал на сыром <code>text</code>, не <code>text_norm</code>: ~<span class="num">219/1077</span> mixed теряют сигнал при нормализации.</p></div>
            <div class="research-row research-row--conclusion"><span class="research-row-k">Зачем tone</span><div class="research-row-body"><p>Этот test.csv станет единым hold-out для всех LID baseline (§10). Тот же LID v2 потом фильтрует 2GIS-отзывы: в tone gold попадают только строки с <code>language == mixed</code> по модели.</p></div></div>
          </div>
        </article>
        <article class="research-card motion-research">
          <div class="research-card-head">
            <span class="mono">06</span>
            <h3>XLM-R LID v2</h3>
            <span class="research-chip research-chip--production">гл. 6 · cells 154-176</span>
          </div>
          <div class="research-rows">
            <div class="research-row"><span class="research-row-k">Что делал</span><p>Fine-tune XLM-RoBERTa-base на gold + synthetic. Kaggle 2× T4, AdamW lr 2e-5. Вход: сырой <code>text</code>.</p></div>
            <div class="research-row"><span class="research-row-k">Результат</span><p>v1 <span class="num">95,92%</span> → v2 <span class="num">96,56%</span> macro-F1 на test <span class="num">461</span>. Mixed P/R ~<span class="num">95%</span>. 14 из 16 ошибок: kz ↔ mixed.</p></div>
            <div class="research-row research-row--conclusion"><span class="research-row-k">Вывод</span><div class="research-row-body"><p>Фильтр языка доказан на ручном hold-out. Можно перескорить корпус и строить tone gold на отфильтрованных mixed 2GIS.</p></div></div>
          </div>
        </article>
        <div class="journey-callout motion-research">
          <strong>§10 Baseline ladder (cells 267-268, после гл. 8 в файле).</strong> Все модели (FastText v1/v2, Lingua v1/v2, XLM-R v2) я прогнал на одном <code>test.csv</code> n=<span class="num">461</span> из главы 5. Это не новый этап сбора данных, а честное сравнение на одном эталоне. Ladder: секция <a href="#lid" data-scroll="lid">Фильтр</a>.
        </div>
        <p class="act-label motion-research">Акт IV · Корпус и tone (гл. 7-8 · cells 177-264)</p>
        <article class="research-card motion-research">
          <div class="research-card-head">
            <span class="mono">07</span>
            <h3>Корпус 331k</h3>
            <span class="research-chip research-chip--production">гл. 7 · cells 177-237</span>
          </div>
          <div class="research-rows">
            <div class="research-row"><span class="research-row-k">Что делал</span><p>Перескорил Telegram+Kaspi через LID v2 → <code>kaspi-telegram_dataset_v2.csv</code> (<span class="num">254&nbsp;652</span>). Добавил 2GIS neg/pos после чистки.</p></div>
            <div class="research-row"><span class="research-row-k">2GIS</span><p>neg <span class="num">29&nbsp;479</span> · pos <span class="num">35&nbsp;928</span> после чистки.</p></div>
            <div class="research-row"><span class="research-row-k">main.csv</span><p><span class="num">331&nbsp;468</span> (ru <span class="num">281&nbsp;409</span> · kz <span class="num">33&nbsp;695</span> · mixed <span class="num">16&nbsp;364</span>).</p></div>
            <div class="research-row research-row--conclusion"><span class="research-row-k">Оговорка</span><div class="research-row-body"><p><span class="num">16&nbsp;364</span> mixed: предсказания LID v2, не ручной аудит. Корректно: «кандидаты по модели». Corpus audit 100 random из Action Plan не выполнял.</p></div></div>
          </div>
        </article>
        <article class="research-card motion-research">
          <div class="research-card-head">
            <span class="mono">08</span>
            <h3>Tone v1: цель capstone</h3>
            <span class="research-chip research-chip--production">гл. 8 · cells 238-264</span>
          </div>
          <div class="research-rows">
            <div class="research-row"><span class="research-row-k">Отбор данных</span><p>2GIS neg/pos → LID v2 → только <code>language == mixed</code> → разметка тона через <code>run_labeler.py</code> (LLM-draft + manual fixes) → баланс pos/neg → <span class="num">3&nbsp;529</span> gold.</p></div>
            <div class="research-row"><span class="research-row-k">Состав gold</span><p>pos <span class="num">1&nbsp;771</span>, neg <span class="num">1&nbsp;758</span>. <code>llm_composer</code> <span class="num">3&nbsp;312</span>, manual <span class="num">217</span>.</p></div>
            <div class="research-row"><span class="research-row-k">Train / test</span><p>+ <span class="num">882</span> synthetic только в train → merge <span class="num">4&nbsp;411</span>. Test <span class="num">525</span> gold-only, без synthetic.</p></div>
            <div class="research-row"><span class="research-row-k">Результат</span><p>Tone v1 accuracy <span class="num">97,33%</span>. v2 хуже (<span class="num">96,19%</span>), в production v1. Артефакт: <code>tone_v1.pt</code>, <code>eval_tone_v1.py</code>.</p></div>
            <div class="research-row research-row--conclusion"><span class="research-row-k">Оговорка</span><div class="research-row-body"><p>~<span class="num">94%</span> tone gold от LLM. Метрика <span class="num">97,33%</span> = agreement с LLM на hold-out. Manual <span class="num">217</span> отдельно не оценён.</p></div></div>
          </div>
        </article>
        <p class="act-label motion-research">Акт V · Продукт (гл. 9)</p>
        <article class="research-card motion-research">
          <div class="research-card-head">
            <span class="mono">09</span>
            <h3>Filter-first cascade</h3>
            <span class="research-chip research-chip--production">гл. 9 · inference</span>
          </div>
          <div class="research-rows">
            <div class="research-row"><span class="research-row-k">Что сделал</span><p>Собрал <code>inference/pipeline.py</code>: TEXT → LID v2 → route (ru → RuBERT, kz → Kazakh BERT, mixed → Tone v1). Локальный API (<code>run_demo.py</code>), сервис разметки gold (<code>run_labeler.py</code>).</p></div>
            <div class="research-row"><span class="research-row-k">Defense path</span><p>Без Run All ноутбука: веса на диске, cells 45, 173, 237, 268, eval-скрипты. Первый запрос API: 503 на 30-60 с (загрузка ~8,56 GB).</p></div>
            <div class="research-row research-row--conclusion"><span class="research-row-k">Связь с целью</span><div class="research-row-body"><p>Tone v1 не живёт отдельно: mixed tone classification встроена в единый cascade. Подробнее: секция <a href="#product" data-scroll="product">Продукт</a>.</p></div></div>
          </div>
        </article>
      </div>
    </div>
  </section>

  <section class="section-dark" id="lid">
    <div class="container">
      <div class="section-head motion-inview">
        <h2>Фильтр языка: доказательства</h2>
        <p>Опора для tone. Краткая сводка метрик; путь в ноутбуке: секция <a href="#journey" data-scroll="journey" style="text-decoration:underline;color:inherit">Путь</a>, карточки 05-06.</p>
      </div>
      <div class="prose-block motion-inview">
        <p>Gold LID <span class="num">3&nbsp;076</span> и единый test <span class="num">461</span> позволил сравнить все baseline на одном hold-out (§10, cells 267-268). XLM-R v2: macro-F1 <span class="num">96,56%</span>. 14 из 16 ошибок: kz ↔ mixed (именно эта путаница ломает маршрутизацию mixed → Tone v1).</p>
      </div>
      <div class="model-group motion-inview">
        <div class="model-group-head">
          <h3>XLM-R LID v2</h3>
          <p>macro-F1 <span class="num">96,56%</span> · gold test n=<span class="num">461</span> · 14 из 16 ошибок: kz ↔ mixed</p>
        </div>
        <div class="model-panels">
          <article class="model-panel model-panel--prod">
            <span class="tag tag-best">Production</span>
            <h4>Confusion matrix v2</h4>
            <div class="model-body">
              <div class="model-matrix">
                <p class="heatmap-title">rows = true, cols = pred</p>
                <div class="heatmap heatmap--lid">
                  <span class="heatmap-label"></span>
                  <span class="heatmap-label heatmap-label--ru">ru</span>
                  <span class="heatmap-label heatmap-label--kz">kz</span>
                  <span class="heatmap-label heatmap-label--mix">mixed</span>
                  <span class="heatmap-label heatmap-label--ru">true ru</span>
                  <div class="heatmap-cell" style="background:rgba(90,142,200,0.7)"><span class="num">150</span></div>
                  <div class="heatmap-cell"><span class="num">0</span></div>
                  <div class="heatmap-cell"><span class="num">0</span></div>
                  <span class="heatmap-label heatmap-label--kz">true kz</span>
                  <div class="heatmap-cell"><span class="num">0</span></div>
                  <div class="heatmap-cell" style="background:rgba(58,173,120,0.65)"><span class="num">142</span></div>
                  <div class="heatmap-cell" style="background:rgba(212,114,114,0.35)"><span class="num">8</span></div>
                  <span class="heatmap-label heatmap-label--mix">true mixed</span>
                  <div class="heatmap-cell" style="background:rgba(212,114,114,0.25)"><span class="num">2</span></div>
                  <div class="heatmap-cell" style="background:rgba(212,114,114,0.3)"><span class="num">6</span></div>
                  <div class="heatmap-cell" style="background:rgba(212,160,36,0.65)"><span class="num">153</span></div>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
      <div class="benchmark-ladder motion-inview">
        <p class="mono" style="color:var(--muted);margin-bottom:8px">§10 main.ipynb · один test.csv · n=<span class="num">461</span></p>
        <div class="bench-row bench-row--dim"><span>FastText v1</span><div class="bench-bar"><div class="bench-fill" style="width:65%"></div></div><span class="bench-pct num">63,24%</span></div>
        <div class="bench-row"><span>FastText v2</span><div class="bench-bar"><div class="bench-fill" style="width:73%"></div></div><span class="bench-pct num">70,92%</span></div>
        <div class="bench-row bench-row--dim"><span>Lingua v1</span><div class="bench-bar"><div class="bench-fill" style="width:88%"></div></div><span class="bench-pct num">84,96%</span></div>
        <div class="bench-row"><span>Lingua v2</span><div class="bench-bar"><div class="bench-fill" style="width:92%"></div></div><span class="bench-pct num">88,63%</span></div>
        <div class="bench-row"><span>XLM-R v2</span><div class="bench-bar"><div class="bench-fill bench-fill--win" style="width:100%"></div></div><span class="bench-pct bench-pct--win num">96,56%</span></div>
      </div>
      <div class="qualifier-box motion-inview">
        <strong>О корпусе main.csv.</strong> Среди 331 468 строк 16 364 помечены как mixed моделью LID v2, без выборочного ручного аудита на уровне корпуса. На защите опираюсь на gold-наборы: 3 076 строк LID и 3 529 mixed-отзывов для tone, а не на массовую авторазметку Telegram.
      </div>
    </div>
  </section>

  <section class="section-light" id="tone">
    <div class="container">
      <div class="section-head motion-inview">
        <h2>Результат capstone: Tone v1</h2>
        <p>Классификация тональности на смешанных отзывах 2GIS. Это главный deliverable; LID понадобился, чтобы собрать и маршрутизировать такие тексты.</p>
      </div>
      <div class="prose-block motion-inview">
        <p><strong>Задача.</strong> Позитив или негатив на mixed-отзыве 2GIS. Модель: fine-tuned XLM-RoBERTa, <code>tone_v1.pt</code>.</p>
        <p><strong>Как собрал gold.</strong> 2GIS neg/pos → LID v2 (<code>xlm-r_v2.pt</code>) → только строки с <code>language == mixed</code> → разметка тона (<code>run_labeler.py</code>: LLM-draft + manual) → баланс → <span class="num">3&nbsp;529</span> строк в <code>tone_mixed_balanced_audited.csv</code>.</p>
        <p><strong>Train / test.</strong> Gold <span class="num">3&nbsp;529</span> (pos <span class="num">1&nbsp;771</span>, neg <span class="num">1&nbsp;758</span>). + <span class="num">882</span> synthetic только в train. Test <span class="num">525</span> gold-only.</p>
        <p><strong>Метрика.</strong> Accuracy <span class="num">97,33%</span> на hold-out. Совпадает с <code>metrics_tone_test.json</code>. Tone v2: <span class="num">96,19%</span>, не вошёл в production.</p>
        <p><strong>Оговорка.</strong> ~<span class="num">94%</span> gold от <code>llm_composer</code>; на test <span class="num">488/525</span> тоже LLM. Метрика = agreement с LLM, не blind human eval. Manual <span class="num">217</span> отдельно не оценён.</p>
      </div>
      <div class="tone-cm motion-inview" aria-label="Confusion matrix tone v1">
        <span class="neg"><span class="num">257</span></span>
        <span class="pos"><span class="num">6</span></span>
        <span class="neg"><span class="num">8</span></span>
        <span class="pos"><span class="num">254</span></span>
      </div>
      <p class="mono motion-inview" style="color:var(--muted);font-size:12px;margin-top:8px">Confusion matrix Tone v1 · rows: true neg, true pos · cols: pred neg, pred pos · test n=525</p>
      <div class="qualifier-box motion-inview">
        <strong>Домены разные:</strong> LID обучал на Telegram/Kaspi; tone на mixed 2GIS. Это осознанное ограничение: tone gold собрал там, где есть размеченные mixed-отзывы.
      </div>
    </div>
  </section>

  <section class="section-dark pipeline-band is-visible" id="product">
    <div class="container">
      <div class="section-head motion-inview">
        <h2>Продукт: filter-first cascade</h2>
        <p>Как LID и tone работают вместе в <code>inference/pipeline.py</code>. Сначала язык, потом маршрут к нужной tone-модели.</p>
      </div>
      <div class="prose-block motion-inview" style="margin-bottom:var(--space-4)">
        <p>Пользователь вводит сырой текст. XLM-R LID v2 определяет ru, kz или mixed. Если ru: RuBERT (pretrained). Если kz: Kazakh BERT (pretrained). Если mixed: Tone v1 (fine-tuned XLM-R). Так mixed tone classification встроена в единый API, а не живёт отдельно от фильтра языка.</p>
      </div>
      <div class="pipe-schema motion-inview" aria-label="Pipeline">
        <p class="pipe-schema-label">TEXT → LID → route → tone → результат</p>
        <div class="pipe-schema-main">
          <div class="pipe-node pipe-node--input">
            <span class="pipe-node-k">Ввод</span>
            <span class="pipe-node-t">Сырой text</span>
            <span class="pipe-node-s">2GIS · Telegram · Kaspi</span>
          </div>
          <span class="pipe-connector-h" aria-hidden="true"></span>
          <div class="pipe-node pipe-node--lid">
            <span class="pipe-node-k">LID</span>
            <span class="pipe-node-t">XLM-R v2</span>
            <span class="pipe-node-s">ru / kz / mixed</span>
          </div>
          <span class="pipe-connector-h" aria-hidden="true"></span>
          <div class="pipe-node pipe-node--route">
            <span class="pipe-node-k">Route</span>
            <span class="pipe-node-t">Маршрутизация</span>
            <span class="pipe-node-s">по метке LID</span>
          </div>
        </div>
        <div class="pipe-schema-branch">
          <div class="pipe-schema-routes">
            <div class="pipe-route pipe-route--ru">
              <span class="pipe-route-tag">ru</span>
              <div class="pipe-route-card"><h4>RuBERT</h4><p>pretrained tone</p></div>
            </div>
            <div class="pipe-route pipe-route--kz">
              <span class="pipe-route-tag">kz</span>
              <div class="pipe-route-card"><h4>Kazakh BERT</h4><p>pretrained tone</p></div>
            </div>
            <div class="pipe-route pipe-route--mixed">
              <span class="pipe-route-tag">mixed</span>
              <div class="pipe-route-card"><h4>Tone v1</h4><p>capstone fine-tune</p></div>
            </div>
          </div>
          <div class="pipe-converge" aria-hidden="true">
            <div class="pipe-converge-bus"></div>
            <div class="pipe-converge-tail"><span class="pipe-connector-v"></span></div>
          </div>
          <div class="pipe-schema-out">
            <div class="pipe-node pipe-node--out">
              <span class="pipe-node-k">Результат</span>
              <span class="pipe-node-t">Класс тона</span>
              <div class="pipe-out-labels">
                <span class="pos">позитив</span>
                <span class="neg">негатив</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="repro-block motion-inview" style="margin-top:var(--space-5)">
        <code>python scripts/setup_demo_models.py</code><br>
        <code>python run_demo.py</code> &nbsp;# http://127.0.0.1:8000/<br>
        <code>python run_labeler.py</code> &nbsp;# разметка gold LID<br>
        <code>python scripts/eval_tone_v1.py</code> &nbsp;# метрики tone
      </div>
      <p class="motion-inview" style="margin-top:var(--space-3);color:var(--muted);font-size:14px;max-width:68ch">Первый запрос к API может вернуть 503 на 30-60 с (загрузка четырёх моделей, ~8,56 GB). Интерактивное демо: <a href="index.html#demo" style="text-decoration:underline">web/index.html</a>. Defense path: cells 45, 173, 237, 268.</p>
    </div>
  </section>

  <section class="section-light labeler-section" id="labeler">
    <div class="container">
      <div class="section-head motion-inview">
        <h2>Сервис разметки</h2>
        <p>Инструмент для gold LID и tone: ручная разметка, пакетная LLM-разметка языка и экспорт в CSV.</p>
      </div>
      <div class="prose-block motion-inview" style="margin-bottom:0">
        <p><strong>Зачем.</strong> Gold-данные должны быть воспроизводимы, а не только строкой в ноутбуке. Я вынес разметку в отдельный веб-сервис с очередью, метриками и экспортом.</p>
        <p><strong>Что размечено.</strong> <span class="num">3&nbsp;076</span> gold LID и основная часть tone gold для mixed-отзывов 2GIS. Язык: LLM ускорял черновик, финальные метки проверял вручную. Тон: только ручной режим.</p>
        <p><strong>Запуск.</strong> <code>python run_labeler.py</code> — локально, тот же код, что использовал при подготовке датасетов.</p>
      </div>
{labeler_carousel}
    </div>
  </section>

  <section class="section-light" id="limits">
    <div class="container">
      <div class="section-head motion-inview">
        <h2>Ограничения</h2>
        <p>Student-scale исследование с явно названными границами. Подробнее: Final_Report.md §3.5, §4.2.</p>
      </div>
      <div class="limits-top motion-inview">
        <h3 style="font-size:20px;margin-bottom:var(--space-3);letter-spacing:-0.02em">Пять границ (кратко)</h3>
        <ul style="list-style:none;padding:0;margin:0">
          <li>Tone <span class="num">97,33%</span>: в основном LLM-label agreement, не human validation</li>
          <li>LID на Telegram/Kaspi, tone на 2GIS; E2E cascade не измерял</li>
          <li><span class="num">16&nbsp;364</span> mixed в main.csv: model-predicted, не audited</li>
          <li>Один разметчик gold LID; согласие между двумя разметчиками не измерял</li>
          <li><code>main.ipynb</code> не воспроизводится Run All; defense path через артефакты на диске</li>
        </ul>
      </div>
      <div class="limits motion-inview">
        <h3>Что знаю честно</h3>
        <ul>
          <li>Один разметчик gold LID; согласие между двумя разметчиками не измерял</li>
          <li><span class="num">main.ipynb</span> (270 ячеек) не воспроизводится Run All; Telethon cells 31, 35, 41, 88 нельзя перезапускать</li>
          <li>Defense path: артефакты на диске, cells 45, 173, 237, 268, eval и demo скрипты</li>
          <li>Tone и LID на разных доменах (Telegram/Kaspi vs 2GIS)</li>
          <li><span class="num">16&nbsp;364</span> mixed в main.csv не проверял вручную на уровне корпуса</li>
          <li>Tone <span class="num">97,33%</span>: в основном LLM-label agreement на hold-out</li>
        </ul>
      </div>
      <div class="sources-grid motion-inview">
        <h3>Источники данных</h3>
        <div class="sources-list">
          <div class="source-item"><strong>Telegram 422 141</strong><code>data/raw/telegram_code-switch_dataset.csv</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>Kaspi 39 129</strong><code>data/processed/kaspi_reviews.csv</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>Gold LID 3 076</strong><code>main.ipynb cell 144 · gold_v1.csv</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>LID test 461</strong><code>data/training/filter/v1/test.csv</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>XLM-R v2 96,56%</strong><code>cells 173, 268</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>Ladder FT/Lingua/XLM-R</strong><code>§10 · n=461</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>main.csv 331 468</strong><code>cell 237 · disk</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>main_mixed 16 364</strong><code>cell 237 · model-predicted</code><span class="src-status src-status--caveat">caveat</span></div>
          <div class="source-item"><strong>Tone v1 97,33% n=525</strong><code>cell 255 · metrics_tone_test.json</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>94% tone gold = LLM</strong><code>tone_mixed_balanced_audited.csv</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>1,66% TP</strong><code>cells 45-46 · 460/27 628</code><span class="src-status src-status--caveat">эвристика</span></div>
          <div class="source-item"><strong>2,32% corpus precision</strong><code>cell 61 · 1 542/66 462</code><span class="src-status src-status--ok">проверено</span></div>
          <div class="source-item"><strong>16k human-audited</strong><code>не заявлялось</code><span class="src-status src-status--no">не подтверждено</span></div>
          <div class="source-item"><strong>Corpus audit 100 random</strong><code>Action Plan</code><span class="src-status src-status--no">не выполнен</span></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section-dark" id="close">
    <div class="container about-grid">
      <div class="motion-inview">
        <h2>Итог</h2>
        <p class="lead">Capstone KazNLP: mixed tone classification на отзывах 2GIS (<span class="num">97,33%</span> на test <span class="num">n=525</span>). Чтобы дойти до этой метрики, пришлось построить filter-first pipeline: auto-LID на <span class="num">422k</span> Telegram врал, поэтому собрал gold LID <span class="num">3&nbsp;076</span> и довёл XLM-R v2 до <span class="num">96,56%</span> macro-F1. LID занял больше глав ноутбука, потому что без честного фильтра языка tone учился бы на шуме.</p>
        <div class="anchor-nums">
          <div class="anchor-num">
            <div class="val num" style="color:var(--mixed)">97,33%</div>
            <div class="lbl">Tone v1 на mixed 2GIS, test n=525 (LLM caveat)</div>
          </div>
          <div class="anchor-num">
            <div class="val num" style="color:var(--positive)">96,56%</div>
            <div class="lbl">LID macro-F1, gold test n=461 (опора)</div>
          </div>
          <div class="anchor-num">
            <div class="val num">3&nbsp;529</div>
            <div class="lbl">gold tone mixed · 3 076 gold LID</div>
          </div>
        </div>
        <blockquote class="pitch-box">
          KazNLP: тональность на смешанных отзывах 2GIS. Честно: 97,33% на test n=525 это agreement с LLM-разметкой, не независимая экспертиза. Чтобы собрать mixed gold, построил filter-first cascade: LID v2 (96,56% macro-F1 на ручном gold) маршрутизирует текст к RuBERT, Kazakh BERT или Tone v1. Demo и eval воспроизводятся локально.
          <cite>Формулировка на 30 секунд</cite>
        </blockquote>
        <div class="week-grid motion-inview">
          <div class="week-row"><span>Нед 1</span>Action Plan, WBS, сбор корпуса</div>
          <div class="week-row"><span>1-2</span>EDA, FastText/Lingua baselines, guidelines gold</div>
          <div class="week-row"><span>2-3</span>XLM-R LID v2, Mixed Tone v1, labeler, demo</div>
          <div class="week-row"><span>3</span>LID/tone metrics, CM, gold test ladder</div>
          <div class="week-row"><span>4</span>Final Report, презентация, защита</div>
        </div>
        <p class="author" style="margin-top:var(--space-5)">Bogdan Savelyev</p>
        <p class="author-sub">Samsung Innovation Campus · Deep Learning / NLP · июнь 2026</p>
        <div class="story-links">
          <a href="../STORY.md">STORY.md</a>
          <a href="../docs/capstone/Final_Report.md">Final Report</a>
          <a href="index.html">Продуктовый лендинг</a>
          <a href="index.html#demo">Live demo</a>
        </div>
      </div>
    </div>
    <div class="container footer-line">
      <p>KazNLP · История проекта</p>
    </div>
  </section>
"""


def main() -> None:
    index = INDEX.read_text(encoding="utf-8")
    css_start = index.find("<style>")
    css_end = index.find("</style>") + len("</style>")
    css = index[css_start:css_end]
    css = css.replace("</style>", EXTRA_CSS + "\n  </style>")

    head = index[:css_start]
    head = head.replace(
        "<title>KazNLP — шала-казахский: LID + тон</title>",
        "<title>KazNLP - история проекта: mixed tone + LID</title>",
    )

    body = BODY.replace("{labeler_carousel}", _labeler_carousel_html())
    html = f"""{head}
{css}
</head>
<body>
{body}
{MINIMAL_JS}
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT} ({len(html.splitlines())} lines)")


if __name__ == "__main__":
    main()
