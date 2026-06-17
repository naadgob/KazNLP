#!/usr/bin/env python3
"""
Сбор отзывов 2ГИС по крупным городам KZ (фильтр по звёздам через API).

Как работает:
  1) Для каждого города + категории открывает страницу поиска 2gis.kz
  2) Достаёт ID заведений (branch_id) из HTML
  3) Тянет отзывы через public-api.reviews.2gis.com (параметр ratings)
  4) Пишет CSV в формате KazNLP

Запуск (из корня проекта):
  pip install requests

  # tone− (1–2★) — основной пул для негатива
  python collect_2gis_reviews.py --sentiment negative

  # tone+ round3 — новые города/категории, дедуп с tone_labeling + старым 2GIS
  python -c "from collect_2gis_reviews import main_positive_round3; main_positive_round3(
      tone_labeling_csv=r'C:/Users/nadgo/Downloads/tone_labeling.csv')"

  # кастомный фильтр
  python collect_2gis_reviews.py --ratings 3,4,5

Ориентир по корпусу (после chip-clean + LID): ~30k строк, ~4.3k mixed.
Для MVP tone: негатив — 2GIS, позитив — TG + выборочно 4–5★ 2GIS.

Внимание: только для исследования / capstone. Соблюдайте ToS 2ГИС.
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

REVIEWS_KEY = os.getenv(
    "DGIS_REVIEWS_KEY", "37c04fe6-a560-4549-b459-02309cf643ad"
)
REVIEWS_URL = "https://public-api.reviews.2gis.com/2.0/branches/{branch_id}/reviews"

CITIES: dict[str, str] = {
    # уже собрано / мегаполисы
    "almaty": "almaty",
    "astana": "astana",
    "shymkent": "shymkent",
    "atyrau": "atyrau",
    "karaganda": "karaganda",
    "aktobe": "aktobe",
    # юг — плотный шала-казахский в бытовых жалобах
    "turkestan": "turkestan",
    "taraz": "taraz",
    "kyzylorda": "kyzylorda",
    # запад / нефть
    "aktau": "aktau",
    "uralsk": "uralsk",
    # восток / север — двуязычный сервис + ЖКХ
    "semey": "semey",
    "ust_kamenogorsk": "ust-kamenogorsk",
    "pavlodar": "pavlodar",
    "kostanay": "kostanay",
    "ekibastuz": "ekibastuz",
}

# Поисковые запросы с высоким трафиком и живой разговорной речью (часто ru+kz в жалобах).
DEFAULT_CATEGORIES = [
    # еда, массовый рынок
    "кафе",
    "рестораны",
    "столовая",
    "шашлычная",
    "шаурма",
    "фастфуд",
    "пиццерия",
    "доставка еды",
    "кондитерская",
    "пекарня",
    # медицина
    "стоматология",
    "поликлиника",
    "больница",
    "аптеки",
    "ветклиника",
    # авто
    "автосервис",
    "автомойка",
    "шиномонтаж",
    "автозапчасти",
    "автосалон",
    # красота
    "салоны красоты",
    "парикмахерская",
    "барбершоп",
    # техника и связь
    "ремонт телефонов",
    "сервисный центр",
    "салон связи",
    "сотовый салон",
    # ритейл
    "супермаркеты",
    "продуктовый магазин",
    "магазин одежды",
    "обувной магазин",
    "мебельный магазин",
    "электроника",
    "торговый центр",
    "рынок",
    # жильё и коммуналка (эмоциональные mixed-жалобы)
    "управляющая компания",
    "жкх",
    "застройщик",
    # финансы
    "банки",
    "микрозаймы",
    "ломбард",
    # образование и дети
    "школы",
    "детские сады",
    "детский центр",
    # прочее с плотными отзывами
    "гостиницы",
    "фитнес клубы",
    "химчистка",
    "оптика",
    "нотариус",
    "клиники",
]

# Верхняя граница: ~1650 firm_id на одну SSR-страницу поиска 2ГИС.
MAX_FIRMS_PER_QUERY = 1600
MAX_REVIEWS_PER_FIRM = 150
MAX_PAGES_PER_FIRM = 8  # 8×50 = до 400 отзывов с API-страниц
FIRM_TIMEOUT_S = 90.0  # дольше — пропуск заведения, следующий firm_id
FLUSH_EVERY_FIRMS = 50  # сброс CSV на диск (не ждать конца категории)
REQUEST_TIMEOUT = (5, 25)  # (connect, read) сек на один HTTP-запрос
PAGE_SLEEP_S = 0.25  # пауза между страницами отзывов (не между заведениями)
HTTP_RETRIES = 6
HTTP_BACKOFF_BASE = 2.0
HTTP_BACKOFF_CAP_S = 90.0

RETRYABLE_HTTP = (
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
    requests.exceptions.ChunkedEncodingError,
)

FIRM_ID_RE = re.compile(r"7000\d{11,}")
# 2ГИС отдаёт firm_id в HTML только при SSR-профиле.
# С полным Chrome UA приходит ~11 KB SPA-оболочка без данных → 0 заведений.
SSR_USER_AGENT = "Mozilla/5.0"
MIN_SSR_HTML_BYTES = 50_000

# API public-api.reviews.2gis.com — параметр ratings (через запятую).
RATING_PRESETS: dict[str, str] = {
    "negative": "1,2",
    "positive": "4,5",
    "neutral": "3",
    "all": "1,2,3,4,5",
}
OUT_PRESETS: dict[str, str] = {
    "negative": "data/raw/2gis_reviews_negative.csv",
    "positive": "data/raw/2gis_reviews_positive.csv",
}

# Уже собрано в pos-раундах 1–2 (города × категории) — не повторять в round3.
POSITIVE_ROUND1_CITIES = ("karaganda", "aktobe", "aktau", "semey")
POSITIVE_ROUND2_CITIES = ("astana", "shymkent", "almaty")
POSITIVE_ROUND1_CATEGORIES = (
    "доставка еды",
    "кафе",
    "стоматология",
    "аптеки",
    "автосервис",
    "салоны красоты",
    "супермаркеты",
    "торговый центр",
)
POSITIVE_ROUND2_CATEGORIES = ("шаурма", "жкх", "стоматология", "доставка еды")

# Round3: города без pos-сбора + категории с длинными двуязычными отзывами.
POSITIVE_ROUND3_CITIES = (
    "atyrau",
    "turkestan",
    "taraz",
    "kyzylorda",
    "uralsk",
    "ust_kamenogorsk",
    "pavlodar",
    "kostanay",
    "ekibastuz",
)
POSITIVE_ROUND3_CATEGORIES = (
    # еда — развёрнутые отзывы, часто ru+kz
    "рестораны",
    "столовая",
    "шашлычная",
    "пиццерия",
    "фастфуд",
    "кондитерская",
    "пекарня",
    # медицина — благодарности врачам на двух языках
    "поликлиника",
    "клиники",
    "ветклиника",
    # авто / красота
    "автомойка",
    "шиномонтаж",
    "парикмахерская",
    "барбершоп",
    # сервис с деталями
    "гостиницы",
    "фитнес клубы",
    "ремонт телефонов",
    "сервисный центр",
    "детский центр",
    "оптика",
    "рынок",
)

DEFAULT_EXCLUDE_POSITIVE_PATHS = (
    "data/raw/2gis_reviews_positive.csv",
    "data/processed/2gis_reviews_positive.csv",
    "data/processed/2gis_reviews_positive_mixed.csv",
)


def ratings_log_label(ratings: str) -> str:
    compact = ratings.replace(" ", "")
    if compact in ("1,2", "2,1"):
        return "low-rated"
    if compact in ("4,5", "5,4"):
        return "high-rated"
    return f"ratings={ratings}"


def parse_rating_filter(ratings: str) -> set[int]:
    out: set[int] = set()
    for part in ratings.split(","):
        part = part.strip()
        if part.isdigit():
            out.add(int(part))
    if not out:
        raise ValueError(f"invalid ratings filter: {ratings!r}")
    return out


class FirmTimeout(Exception):
    """Превышен лимит времени на одно заведение."""


@dataclass
class ReviewRow:
    text: str
    rating: int
    city: str
    category: str
    place_id: str
    place_name: str
    review_id: str
    date_created: str
    source: str = "2gis"


def make_session() -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=4,
        connect=4,
        read=4,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update(
        {
            "User-Agent": SSR_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ru-KZ,ru;q=0.9,en;q=0.8",
        }
    )
    return s


def get_with_retry(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, str | int] | None = None,
    timeout: float | tuple[float, float] = 45,
    retries: int = HTTP_RETRIES,
    label: str = "",
) -> requests.Response:
    """GET с повторами при обрыве SSL/TCP (WinError 10054 и т.п.)."""
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            r = session.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r
        except RETRYABLE_HTTP as exc:
            last_err = exc
            if attempt >= retries:
                break
            wait = min(
                HTTP_BACKOFF_CAP_S,
                HTTP_BACKOFF_BASE**attempt + random.uniform(0.0, 1.5),
            )
            hint = label or url[:70]
            print(
                f"  HTTP retry {attempt}/{retries} [{hint}]: {exc!r} "
                f"→ sleep {wait:.1f}s",
                flush=True,
            )
            time.sleep(wait)
    assert last_err is not None
    raise last_err


def _extract_firm_ids(html: str, max_firms: int) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for fid in FIRM_ID_RE.findall(html):
        if fid in seen:
            continue
        seen.add(fid)
        out.append(fid)
        if len(out) >= max_firms:
            break
    return out


def fetch_search_html(
    session: requests.Session,
    url: str,
    *,
    http_retries: int = HTTP_RETRIES,
) -> str:
    """Загрузка страницы поиска; при SPA-ответе повтор с SSR User-Agent."""
    r = get_with_retry(session, url, timeout=45, retries=http_retries, label="search")
    if len(r.text) >= MIN_SSR_HTML_BYTES and FIRM_ID_RE.search(r.text):
        return r.text

    # fallback: явный SSR-профиль (обходит пустую оболочку)
    r2 = get_with_retry(session, url, timeout=45, retries=http_retries, label="search-ssr")
    return r2.text


def discover_firm_ids(
    session: requests.Session,
    city_slug: str,
    query: str,
    max_firms: int,
    sleep_s: float,
    *,
    http_retries: int = HTTP_RETRIES,
) -> list[str]:
    url = f"https://2gis.kz/{city_slug}/search/{quote(query)}"
    html = fetch_search_html(session, url, http_retries=http_retries)
    time.sleep(sleep_s)
    ids = _extract_firm_ids(html, max_firms)
    if not ids:
        print(
            f"  WARN: 0 firms (html {len(html)} bytes). "
            "Проверьте сеть или доступ к 2gis.kz."
        )
    return ids


def fetch_place_name(
    session: requests.Session,
    city_slug: str,
    place_id: str,
    *,
    http_retries: int = HTTP_RETRIES,
) -> str:
    url = f"https://2gis.kz/{city_slug}/firm/{place_id}"
    try:
        html = fetch_search_html(session, url, http_retries=http_retries)
        m = re.search(r'property="og:title" content="([^"]+)"', html)
        if m:
            return m.group(1).split(" — ")[0].strip()
    except requests.RequestException:
        pass
    return ""


def iter_branch_reviews(
    session: requests.Session,
    branch_id: str,
    *,
    max_reviews: int,
    ratings: str,
    max_pages: int,
    deadline: float | None = None,
    http_retries: int = HTTP_RETRIES,
) -> Iterable[dict]:
    url = REVIEWS_URL.format(branch_id=branch_id)
    params: dict[str, str | int] = {
        "limit": 50,
        "rated": "true",
        "ratings": ratings,
        "sort_by": "date_edited",
        "key": REVIEWS_KEY,
        "locale": "ru_KZ",
    }
    fetched = 0
    pages = 0
    seen_review_ids: set[str] = set()
    seen_offsets: set[str] = set()

    while fetched < max_reviews and pages < max_pages:
        if deadline is not None and time.monotonic() >= deadline:
            raise FirmTimeout()
        pages += 1
        r = get_with_retry(
            session,
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
            retries=http_retries,
            label=f"reviews {branch_id}",
        )
        data = r.json()
        page = data.get("reviews") or []
        if not page:
            break

        new_on_page = 0
        for rev in page:
            rid = str(rev.get("id") or "")
            if rid and rid in seen_review_ids:
                continue
            if rid:
                seen_review_ids.add(rid)
            yield rev
            fetched += 1
            new_on_page += 1
            if fetched >= max_reviews:
                return

        if new_on_page == 0:
            break

        last = page[-1]
        date_created = last.get("date_created")
        if not date_created or len(page) < params["limit"]:
            break
        if date_created in seen_offsets:
            break
        seen_offsets.add(date_created)
        params["offset_date"] = date_created
        if deadline is not None and time.monotonic() + PAGE_SLEEP_S >= deadline:
            raise FirmTimeout()
        time.sleep(PAGE_SLEEP_S)


# обратная совместимость
iter_negative_reviews = iter_branch_reviews


CSV_FIELDS = [
    "text",
    "rating",
    "city",
    "category",
    "place_id",
    "place_name",
    "review_id",
    "date_created",
    "source",
]


def load_seen_text(path: str) -> set[str]:
    if not os.path.exists(path):
        return set()
    seen: set[str] = set()
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            t = (row.get("text") or "").strip().lower()
            if t:
                seen.add(t)
    return seen


def load_seen_text_many(paths: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    for path in paths:
        if path and os.path.exists(path):
            seen |= load_seen_text(path)
    return seen


def append_rows(path: str, rows: list[ReviewRow]) -> None:
    if not rows:
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    write_header = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if write_header:
            w.writeheader()
        for row in rows:
            w.writerow(row.__dict__)


def collect(
    session: requests.Session,
    *,
    cities: list[str],
    categories: list[str],
    max_firms_per_query: int,
    max_reviews_per_firm: int,
    max_pages_per_firm: int,
    ratings: str,
    min_text_len: int,
    sleep_s: float,
    firm_timeout_s: float,
    fetch_place_names: bool,
    out_path: str | None = None,
    seen_text: set[str] | None = None,
    flush_every_firms: int = FLUSH_EVERY_FIRMS,
    http_retries: int = HTTP_RETRIES,
) -> list[ReviewRow]:
    rows: list[ReviewRow] = []
    seen_text = seen_text if seen_text is not None else set()
    name_cache: dict[tuple[str, str], str] = {}
    total_saved = 0
    firms_since_flush = 0
    allowed_ratings = parse_rating_filter(ratings)
    review_kind = ratings_log_label(ratings)

    def flush_batch(batch: list[ReviewRow], label: str) -> list[ReviewRow]:
        nonlocal total_saved
        if out_path and batch:
            append_rows(out_path, batch)
            total_saved += len(batch)
            print(
                f"  saved {len(batch)} rows → {out_path} "
                f"({label}, ~{total_saved} new this run)",
                flush=True,
            )
        return []

    for city in cities:
        city_slug = CITIES[city]
        for category in categories:
            print(f"[search] {city} / {category}", flush=True)
            try:
                firm_ids = discover_firm_ids(
                    session,
                    city_slug,
                    category,
                    max_firms_per_query,
                    sleep_s,
                    http_retries=http_retries,
                )
            except requests.RequestException as e:
                print(
                    f"  SKIP {city}/{category}: network error after retries: {e}",
                    flush=True,
                )
                time.sleep(sleep_s * 3)
                continue
            print(f"  firms found: {len(firm_ids)}", flush=True)
            batch: list[ReviewRow] = []

            for i, place_id in enumerate(firm_ids, 1):
                if i == 1 or i % 25 == 0:
                    print(f"  [{i}/{len(firm_ids)}] scanning...", flush=True)

                place_name = ""
                if fetch_place_names:
                    key = (city_slug, place_id)
                    if key not in name_cache:
                        name_cache[key] = fetch_place_name(
                            session, city_slug, place_id, http_retries=http_retries
                        )
                        time.sleep(sleep_s)
                    place_name = name_cache[key]

                n_added = 0
                timed_out = False
                deadline = time.monotonic() + firm_timeout_s
                try:
                    for rev in iter_branch_reviews(
                        session,
                        place_id,
                        max_reviews=max_reviews_per_firm,
                        ratings=ratings,
                        max_pages=max_pages_per_firm,
                        deadline=deadline,
                        http_retries=http_retries,
                    ):
                        text = (rev.get("text") or "").strip()
                        if len(text) < min_text_len:
                            continue
                        key_text = text.lower()
                        if key_text in seen_text:
                            continue
                        seen_text.add(key_text)

                        rating = int(rev.get("rating") or 0)
                        if rating <= 0 or rating not in allowed_ratings:
                            continue

                        row = ReviewRow(
                            text=text,
                            rating=rating,
                            city=city,
                            category=category,
                            place_id=place_id,
                            place_name=place_name,
                            review_id=str(rev.get("id") or ""),
                            date_created=str(rev.get("date_created") or ""),
                        )
                        rows.append(row)
                        batch.append(row)
                        n_added += 1
                except FirmTimeout:
                    timed_out = True
                except requests.RequestException as e:
                    print(f"  [{i}/{len(firm_ids)}] {place_id} ERROR: {e}", flush=True)
                    continue

                if timed_out:
                    print(
                        f"  [{i}/{len(firm_ids)}] {place_id} TIMEOUT "
                        f"{firm_timeout_s:.0f}s → skip (+{n_added} saved)",
                        flush=True,
                    )
                elif n_added:
                    print(
                        f"  [{i}/{len(firm_ids)}] {place_id}: "
                        f"+{n_added} {review_kind} reviews",
                        flush=True,
                    )

                time.sleep(sleep_s)

                firms_since_flush += 1
                if firms_since_flush >= flush_every_firms:
                    batch = flush_batch(batch, f"every {flush_every_firms} firms")
                    firms_since_flush = 0

            batch = flush_batch(batch, "end of category")

    return rows


def save_csv(path: str, rows: list[ReviewRow]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for row in rows:
            w.writerow(row.__dict__)


def main(argv: list[str] | None = None) -> list[ReviewRow]:
    """CLI entrypoint. Returns collected rows (handy for notebooks)."""
    p = argparse.ArgumentParser(description="Collect 2GIS reviews by star rating (KZ)")
    p.add_argument(
        "--sentiment",
        choices=list(RATING_PRESETS.keys()),
        default="negative",
        help="negative=1–2★, positive=4–5★, neutral=3★, all=1–5★",
    )
    p.add_argument("--out", default=None, help="CSV path (default из --sentiment)")
    p.add_argument(
        "--cities",
        nargs="+",
        default=list(CITIES.keys()),
        metavar="CITY",
        help=f"города: {', '.join(sorted(CITIES))}",
    )
    p.add_argument("--categories", nargs="+", default=DEFAULT_CATEGORIES)
    p.add_argument(
        "--max-firms",
        type=int,
        default=MAX_FIRMS_PER_QUERY,
        help=f"заведений на город+категорию (макс. SSR ~{MAX_FIRMS_PER_QUERY})",
    )
    p.add_argument(
        "--max-reviews-per-firm",
        type=int,
        default=MAX_REVIEWS_PER_FIRM,
    )
    p.add_argument(
        "--ratings",
        default=None,
        help='фильтр API, напр. "4,5". По умолчанию — из --sentiment',
    )
    p.add_argument("--min-text-len", type=int, default=8)
    p.add_argument("--sleep", type=float, default=1.0)
    p.add_argument(
        "--firm-timeout",
        type=float,
        default=FIRM_TIMEOUT_S,
        help="сек на одно заведение; дольше — пропуск к следующему",
    )
    p.add_argument(
        "--max-pages-per-firm",
        type=int,
        default=MAX_PAGES_PER_FIRM,
        help="лимит страниц API на заведение (защита от зависания)",
    )
    p.add_argument("--fetch-place-names", action="store_true")
    p.add_argument(
        "--resume",
        action="store_true",
        help="дописать в CSV и пропускать уже сохранённые тексты",
    )
    p.add_argument(
        "--exclude-csv",
        nargs="+",
        default=None,
        metavar="PATH",
        help="пропускать тексты из этих CSV (дедуп с tone_labeling / старым 2GIS)",
    )
    p.add_argument(
        "--http-retries",
        type=int,
        default=HTTP_RETRIES,
        help="повторов GET при ConnectionReset/timeout (2GIS иногда рвёт SSL)",
    )
    args = p.parse_args(argv)

    sentiment = args.sentiment or "negative"
    ratings = args.ratings or RATING_PRESETS[sentiment]
    out_path = args.out or OUT_PRESETS.get(sentiment, "data/raw/2gis_reviews.csv")
    try:
        parse_rating_filter(ratings)
    except ValueError as exc:
        p.error(str(exc))

    bad_cities = [c for c in args.cities if c not in CITIES]
    if bad_cities:
        p.error(
            f"unknown cities: {bad_cities}. "
            f"Available: {', '.join(sorted(CITIES))}. "
            "В Jupyter после правки файла: "
            "import importlib, collect_2gis_reviews; importlib.reload(collect_2gis_reviews)"
        )

    print(
        f"sentiment={sentiment} ratings={ratings} → {out_path}",
        flush=True,
    )

    exclude_paths = list(args.exclude_csv or [])
    if args.resume:
        seen_text = load_seen_text(out_path)
        if seen_text:
            print(f"resume: {len(seen_text)} texts already in {out_path}", flush=True)
    else:
        seen_text = set()
        if os.path.exists(out_path):
            os.remove(out_path)

    if exclude_paths:
        extra = load_seen_text_many(exclude_paths)
        before = len(seen_text)
        seen_text |= extra
        print(
            f"exclude-csv: +{len(seen_text) - before} texts from {len(exclude_paths)} file(s) "
            f"(total skip pool {len(seen_text)})",
            flush=True,
        )

    session = make_session()
    t0 = time.time()
    rows = collect(
        session,
        cities=args.cities,
        categories=args.categories,
        max_firms_per_query=args.max_firms,
        max_reviews_per_firm=args.max_reviews_per_firm,
        max_pages_per_firm=args.max_pages_per_firm,
        ratings=ratings,
        min_text_len=args.min_text_len,
        sleep_s=args.sleep,
        firm_timeout_s=args.firm_timeout,
        fetch_place_names=args.fetch_place_names,
        out_path=out_path,
        seen_text=seen_text,
        http_retries=args.http_retries,
    )

    by_city: dict[str, int] = {}
    by_rating: dict[int, int] = {}
    for r in rows:
        by_city[r.city] = by_city.get(r.city, 0) + 1
        by_rating[r.rating] = by_rating.get(r.rating, 0) + 1

    print(f"\nDone in {time.time() - t0:.0f}s")
    print(f"Total reviews: {len(rows)}")
    print("By city:", by_city)
    print("By rating:", dict(sorted(by_rating.items())))
    print(f"Saved: {out_path}")

    return rows


def main_positive(
    out: str = "data/raw/2gis_reviews_positive.csv",
    *,
    resume: bool = False,
    cities: list[str] | None = None,
    categories: list[str] | None = None,
    max_firms: int = 60,
    max_reviews_per_firm: int = 120,
    max_pages_per_firm: int = MAX_PAGES_PER_FIRM,
    min_text_len: int = 8,
    exclude_csv: list[str] | None = None,
    fetch_place_names: bool = False,
) -> list[ReviewRow]:
    """
  4–5★ для tone-MVP (меньше лимиты, чем у негатива).

  Ориентир: из ~30k mixed-корпуса ~4.3k mixed — для tone хватит
  сотен–пары тысяч размеченных pos/neg, не обязательно весь 2GIS.

  exclude_csv — дедуп с уже собранным (tone_labeling, старый 2GIS positive).
    """
    argv = [
        "--out",
        out,
        "--sentiment",
        "positive",
        "--max-firms",
        str(max_firms),
        "--max-reviews-per-firm",
        str(max_reviews_per_firm),
        "--max-pages-per-firm",
        str(max_pages_per_firm),
        "--min-text-len",
        str(min_text_len),
        "--sleep",
        "1.0",
        "--firm-timeout",
        str(int(FIRM_TIMEOUT_S)),
    ]
    if cities:
        argv.extend(["--cities", *cities])
    if categories:
        argv.extend(["--categories", *categories])
    if exclude_csv:
        argv.extend(["--exclude-csv", *exclude_csv])
    if resume:
        argv.append("--resume")
    if fetch_place_names:
        argv.append("--fetch-place-names")
    return main(argv)


def main_positive_round3(
  *,
  tone_labeling_csv: str | None = None,
  resume: bool = True,
) -> list[ReviewRow]:
    """
    Round3: новые города + категории, без пересечения с round1/2.
    Пишет в data/raw/2gis_reviews_positive_v2.csv.
    """
    exclude = list(DEFAULT_EXCLUDE_POSITIVE_PATHS)
    if tone_labeling_csv and os.path.exists(tone_labeling_csv):
        exclude.append(tone_labeling_csv)
    return main_positive(
        out="data/raw/2gis_reviews_positive_v2.csv",
        resume=resume,
        cities=list(POSITIVE_ROUND3_CITIES),
        categories=list(POSITIVE_ROUND3_CATEGORIES),
        max_firms=130,
        max_reviews_per_firm=220,
        max_pages_per_firm=10,
        min_text_len=22,
        exclude_csv=exclude,
        fetch_place_names=True,
    )


def main_max(
    out: str = "data/raw/2gis_reviews_negative.csv",
    *,
    resume: bool = False,
) -> list[ReviewRow]:
    """Полный сбор: все города/категории, макс. лимиты."""
    argv = [
        "--out",
        out,
        "--sentiment",
        "negative",
        "--max-firms",
        str(MAX_FIRMS_PER_QUERY),
        "--max-reviews-per-firm",
        str(MAX_REVIEWS_PER_FIRM),
        "--max-pages-per-firm",
        str(MAX_PAGES_PER_FIRM),
        "--sleep",
        "1.0",
        "--firm-timeout",
        str(int(FIRM_TIMEOUT_S)),
    ]
    if resume:
        argv.append("--resume")
    return main(argv)


if __name__ == "__main__":
    main()
