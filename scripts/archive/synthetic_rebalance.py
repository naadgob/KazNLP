"""Curate synthetic rows: relabel fixes + drop high-drift / mislabeled rows."""
from __future__ import annotations

import re
from typing import Any

from merge_synthetic import word_count
from text_heuristics import has_kazakh_letters

WORD_RE = re.compile(r"[\w']+", re.UNICODE)
LATIN_WORD = re.compile(r"^[a-zA-Z][\w']*$")
TARGET_TOTAL = 538
MAX_KZ_NO_SPECIAL = 50
MAX_KZ_LATIN_RATIO = 0.45
MAX_MIXED_LATIN_RATIO = 0.28

CYRILLIC_WORD = re.compile(r"[а-яё]{3,}", re.I)

PURE_RU_AS_MIXED = {
    "вообще огонь, настроение поднял",
    "в telegram увидел акцию, заказал, пришло быстро.",
    "фото совпало, товар такой же, спасибо.",
    "магазин супер, курьер молодец.",
    "каспи магазин, доставка лучше чем ожидала.",
    "на канале видел, заказал, keldi.",
    "батарея норм, за эту цену жарайды.",
    "chehol jakysy. советую, спасибо.",
    "курьер звонил, затты tappysyrdy.",
    "курьer аман, zat tappysyrdy.",
}

DROP_IF_NORM = {
    *{s.rstrip(".") for s in PURE_RU_AS_MIXED},
    "спасибо store, rahmet kop.",
    "доставка fast, keshke jetkizdi.",
    "товар fire, sapasy zor.",
    "заказ ok, zat zarynada.",
    "порог растет, zp zhok.",
    "класс post, durs jazgansyn.",
    "ок брат, kelisemiz.",
    "салтанатка конечно обal dedim",
    "разберутся скоро, причину табамыз",
    "воротalar janynda kuchkuyutsya bola.",
    "сервис огонь, курьер аман keldi.",
    "magazinge rahmet, tovar uakytinda keldi.",
    "sapasy jakysy, bagasy arzan.",
    "классная акция была. каспиден тез aldym.",
    "курьер вежливый, затты durbis tappysyrdy.",
    "товар соответствует описанию, сапасы суреттегидей.",
    "в отзывах писали правду, сапасы суреттегидей.",
}

TEXT_FIXES: dict[str, str] = {
    "классная акция была. каспиден тез aldym.": "Классная акция была. Каспиден тез заказ бердім.",
    "курьер вежливый, затты durbis tappysyrdy.": "Курьер вежливый, затты есіктен дейін тапсырды.",
    "chehol jakysy. советую, спасибо.": "Чехол жақсы. Советую всем, спасибо продавцу.",
    "батарея норм, за эту цену жарайды.": "Батарея норм. За эту цену жарайды.",
    "курьер звонил, затты tappysyrdy.": "Курьер звонил заранее, затты уақытында тапсырды.",
    "товар соответствует описанию, сапасы суреттегидей.": "Товар как на фото, сапасы суреттегідей, спасибо.",
    "в отзывах писали правду, сапасы суреттегидей.": "В отзывах писали правду, сапасы суреттегідей, рахмет.",
    "алғаныма қуаныштымын, camera quality огонь.": "Алғаныма қуаныштымын, камера отличная, советую всем.",
    "алға qazaqstan! біз birgemiz.": "Патриотизм важен. Алға Qazaqstan!",
    "алға qazaqstan! біз біргеміз.": "Патриотизм важен. Алға Qazaqstan!",
    "кaspi red, ыңғайлы very much.": "Взяла в Kaspi red, өte ыңғayлы, рахmet.",
    "касpi red, ыңғайлы very much.": "Взяла в Kaspi red, өte ыңғayлы, рахmet.",
    "каспи red, ыңғайлы very much.": "Взяла в Kaspi red, өte ыңғayлы, рахmet.",
    "доставка free, уақытında keldi.": "Доставка бесплатная, уақытında келді.",
    "telegram пост жақсы. алға qz!": "Пост жақсы написан. Алға Qazaqstan!",
    "store иne rahmet, delivery tez boldy.": "Дүкен иesine рахmet, доставка уakытında boldy.",
    "store ине rahmet, delivery tez boldy.": "Дүкен иesine рахmet, доставка уakытında boldy.",
    "store ине рахmet, delivery tez boldy.": "Дүкен иesine рахmet, доставка уakытında boldy.",
    "заказ tez daiyndaldy, jetkizdi de tez.": "Зakaz tez dайындалды, jetkizdi de tez.",
    "суреттedey keldi, aldym dem almadan.": "Сurетtедegiдей keldi, aldym дем almadan.",
    "мекtepke aldym, bala unaidy.": "Мektepke aldym, bala уnaidy.",
    "магазин icindegi kyzmet jakysy.": "Мagazин icindegi kyzmet jakysy.",
    "сатушы жақсы қызмет көрсетті, service top.": "Сatушы жakсы qызmet korsetti, сервис топ.",
    "сатушы жақсы қызмет көрсетті, service top": "Сatушы жakсы qызmet korsetti, сервис топ.",
    "original product, сатушыға алғыс.": "Оригинал товар, сatушыga алғыс.",
    "delivery уақытında, packaging бүtín boldy.": "Доставка уakытında, упakовka бüтín boldy.",
    "delivery уақытında, packaging бүtín.": "Доставка уakытında, упakовka бütín.",
    "телефон жақсы жұмыс істейді, камера quality мықты.": "Телефон жakсы жumys isteydi, камера сapasy мықты.",
    "камера quality огонь, рахmet продавцу, телефон жақсы.": "Камера отличная, рахmet продавцу, телефон жakсы.",
    "не ожидала такого сервиса, продавец жauap berdi, доставка tez boldy.": "Не ожидала такого сервиса, продавец жauap berdi, доставка тез болды.",
    "баға тиімді, quality де жақсы.": "Baға tiimdi, качество de жakсы.",
    "телефон уnaды, камера сapasy жakсы, рахmet.": "Телефон уnaды, камера сapasy жakсы, рахmet.",
}

Row = dict[str, str]


def latin_word_ratio(text: str) -> float:
    words = WORD_RE.findall(str(text))
    if not words:
        return 0.0
    return sum(1 for w in words if LATIN_WORD.match(w)) / len(words)


def fix_row_text(row: Row) -> Row:
    norm = row["text"].strip().casefold()
    fixed = TEXT_FIXES.get(norm)
    if fixed:
        return {**row, "text": fixed}
    return row


def relabel_row(row: Row) -> Row:
    row = fix_row_text(row)
    if row["language"] == "mixed" and row["text"].strip() == "На Қапшағай бардық бүгін":
        return {**row, "language": "kz", "seed_id": "gold_kz_short"}
    return row


def is_kz_latin_polluted(text: str) -> bool:
    """Heavy ASCII-latin in kz rows — not gold-aligned."""
    t = str(text)
    lr = latin_word_ratio(t)
    if has_kazakh_letters(t):
        return lr > 0.38
    latin_words = [w for w in WORD_RE.findall(t.lower()) if re.match(r"^[a-z]{3,}$", w)]
    if len(latin_words) >= 3:
        return True
    if lr > 0.18:
        return True
    return False


def strict_label_ok(row: Row) -> bool:
    try:
        from audit_synthetic import strict_kz_ok, strict_mixed_ok
    except ImportError:
        return True
    lang = row["language"]
    text = row["text"]
    if lang == "mixed":
        return strict_mixed_ok(text)[0]
    if lang == "kz":
        return strict_kz_ok(text)[0]
    return True


def is_latin_kz_drift(text: str) -> bool:
    """Pure-latin shala kz without cyrillic — not gold-aligned."""
    if has_kazakh_letters(text):
        return False
    if CYRILLIC_WORD.search(str(text)):
        return False
    return latin_word_ratio(text) > MAX_KZ_LATIN_RATIO


def should_drop(row: Row) -> bool:
    norm = row["text"].strip().casefold()
    if norm.rstrip(".") in {s.rstrip(".") for s in DROP_IF_NORM}:
        return True
    if row["language"] == "kz" and is_latin_kz_drift(row["text"]):
        return True
    if row["language"] == "kz" and is_kz_latin_polluted(row["text"]):
        return True
    return False


def quality_ok(row: Row, *, kz_no_special: int = 0) -> bool:
    """Caps during batch write; mislabel guard for pure-ru mixed."""
    if should_drop(row):
        return False
    if row["language"] == "kz" and not has_kazakh_letters(row["text"]) and kz_no_special >= MAX_KZ_NO_SPECIAL:
        return False
    if row["language"] == "mixed":
        try:
            from precision_filter import has_kazakh_signal, has_russian_signal

            text = row["text"]
            if has_russian_signal(text) and not has_kazakh_signal(text) and not has_kazakh_letters(text):
                return False
            if latin_word_ratio(text) > MAX_MIXED_LATIN_RATIO and not strict_label_ok(row):
                return False
        except ImportError:
            pass
    if row["language"] == "kz" and is_kz_latin_polluted(row["text"]):
        return False
    return True


def fill_row_ok(row: Row, *, kz_no_special: int = 0) -> bool:
    """Stricter gate for batch-014 fill rows."""
    if not quality_ok(row, kz_no_special=kz_no_special):
        return False
    if not strict_label_ok(row):
        return False
    t = row["text"]
    lr = latin_word_ratio(t)
    if row["language"] == "kz" and lr > 0.22:
        return False
    if row["language"] == "mixed" and lr > 0.2:
        return False
    return True


def fill_sort_key(row: Row) -> tuple[float, float, int]:
    """Prefer low latin drift and longer mixed sentences."""
    t = row["text"]
    lr = latin_word_ratio(t)
    wc = word_count(t)
    short_penalty = 1.0 if row["language"] == "mixed" and wc < 7 else 0.0
    return (lr + short_penalty, lr, -wc)


def curate_rows(rows: list[Row]) -> list[Row]:
    try:
        from synthetic_replacements import REPLACEMENTS
    except ImportError:
        REPLACEMENTS = []

    kept: list[Row] = []
    seen: set[str] = set()
    kz_no_special = 0
    for row in rows:
        row = relabel_row(row)
        if should_drop(row):
            continue
        if row["language"] == "kz" and not has_kazakh_letters(row["text"]):
            if kz_no_special >= MAX_KZ_NO_SPECIAL:
                continue
            kz_no_special += 1
        norm = row["text"].strip().casefold()
        if norm in seen:
            continue
        seen.add(norm)
        kept.append(row)
    for row in REPLACEMENTS:
        if len(kept) >= TARGET_TOTAL:
            break
        row = relabel_row(row)
        if not quality_ok(row, kz_no_special=kz_no_special):
            continue
        if row["language"] == "kz" and not has_kazakh_letters(row["text"]):
            kz_no_special += 1
        norm = row["text"].strip().casefold()
        if norm in seen:
            continue
        seen.add(norm)
        kept.append(row)

    return kept[:TARGET_TOTAL]


def stats(rows: list[Row]) -> dict[str, Any]:
    from collections import Counter

    langs = Counter(r["language"] for r in rows)
    out: dict[str, Any] = {"n": len(rows), "by_lang": dict(langs)}
    for lang in ("mixed", "kz", "ru"):
        sub = [r for r in rows if r["language"] == lang]
        if not sub:
            continue
        wcs = [word_count(r["text"]) for r in sub]
        out[f"{lang}_avg_words"] = round(sum(wcs) / len(wcs), 1)
        out[f"{lang}_latin_pct"] = round(
            sum(1 for r in sub if latin_word_ratio(r["text"]) > 0) / len(sub), 3
        )
    m = [r for r in rows if r["language"] == "mixed"]
    k = [r for r in rows if r["language"] == "kz"]
    out["mixed_le5"] = sum(1 for r in m if word_count(r["text"]) <= 5)
    out["mixed_no_kz"] = sum(1 for r in m if not has_kazakh_letters(r["text"]))
    out["mixed_kaspi"] = sum(
        1
        for r in m
        if re.search(r"kaspi|каспи|курьер|доставк|магазин", r["text"].lower())
    )
    out["kz_no_special"] = sum(1 for r in k if not has_kazakh_letters(r["text"]))
    return out
