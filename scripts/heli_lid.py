"""HeLI/heliport LID baseline for kk–ru gold eval (Tommi-style loanword re-ID)."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from essential_ru_kaz import essential_ru_kaz_dict, kazakh_dict
from popular_ru_kaz import popular_ru_kaz_dict

KAZAKH_CHARS = set("әіңғүұқөһ")
WORD_RE = re.compile(r"[\w']+", re.UNICODE)
LABELS = ["ru", "kz", "mixed"]

# High-frequency Russian function / closed-class words — never neutralize.
FUNCTION_WORDS = {
    "и", "в", "не", "на", "я", "он", "что", "это", "быть", "а", "весь", "они",
    "она", "как", "мы", "к", "у", "вы", "этот", "за", "тот", "но", "ты", "по",
    "о", "свой", "так", "один", "вот", "который", "наш", "только", "ещё",
    "такой", "мочь", "говорить", "сказать", "для", "уже", "знать", "да", "нет",
    "или", "же", "бы", "ли", "если", "когда", "чтобы", "то", "от", "до", "из",
    "со", "об", "при", "про", "без", "под", "над", "между", "через", "после",
    "перед", "около", "мне", "меня", "мной", "тебе", "тебя", "ему", "его",
    "ей", "её", "нам", "нас", "вам", "вас", "им", "их", "себя", "себе",
    "мой", "твой", "его", "её", "наш", "ваш", "их", "все", "всё", "сам",
    "там", "тут", "здесь", "где", "куда", "откуда", "почему", "зачем",
    "очень", "ещё", "уже", "тоже", "также", "ещё", "можно", "нужно", "надо",
    "есть", "был", "была", "было", "были", "будет", "будут",
}

# Explicit content borrowings common in KZ UGC (Cyrillic, same orthography).
SEED_LOANWORDS = {
    "телефон", "компьютер", "ноутбук", "интернет", "вайфай", "wifi", "банк",
    "карта", "кредит", "онлайн", "оффлайн", "магазин", "маркет", "доставка",
    "заказ", "продавец", "покупатель", "скидка", "акция", "цена", "рубль",
    "тенге", "доллар", "офис", "менеджер", "директор", "компания", "фирма",
    "проект", "сервис", "услуга", "проблема", "система", "программа",
    "приложение", "аккаунт", "логин", "пароль", "чат", "канал", "группа",
    "видео", "фото", "камера", "бренд", "модель", "размер", "качество",
    "гарантия", "возврат", "отзыв", "рейтинг", "курьер", "адрес", "регион",
    "город", "район", "улица", "номер", "контакт", "сообщение", "уведомление",
    "подписка", "тариф", "баланс", "перевод", "платеж", "оплата", "чек",
    "касса", "терминал", "автомат", "такси", "автобус", "метро", "аэропорт",
    "вокзал", "билет", "паспорт", "документ", "справка", "заявление",
    "школа", "университет", "колледж", "курс", "экзамен", "диплом",
    "работа", "зарплата", "вакансия", "резюме", "интервью", "босс",
    "коллега", "клиент", "партнер", "партнёр", "контракт", "договор",
    "закон", "суд", "полиция", "больница", "врач", "аптека", "лекарство",
    "ресторан", "кафе", "меню", "отель", "гостиница", "бронь", "бронирование",
}

KZ_LEXICON = {w.lower() for w in kazakh_dict} | {
    w.lower() for w in popular_ru_kaz_dict.values()
}


def tokenize(text: str) -> list[str]:
    return WORD_RE.findall(str(text).lower())


def has_kazakh_signal(text: str) -> bool:
    t = str(text).lower()
    if any(c in KAZAKH_CHARS for c in t):
        return True
    words = set(tokenize(t))
    return len(words) >= 2 and len(words & KZ_LEXICON) >= 1


def heli_code(identifier, text: str) -> str:
    t = str(text).replace("\n", " ").strip()
    if not t:
        return "und"
    try:
        code = identifier.identify(t)
    except Exception:
        return "und"
    if hasattr(code, "name"):
        code = code.name
    return str(code).lower()


def map_raw(code: str, text: str) -> str:
    """HeLI raw → 3-way without stripping."""
    if code == "kaz":
        return "kz"
    if code == "rus":
        return "mixed" if has_kazakh_signal(text) else "ru"
    return "ru"


def strip_loanwords(text: str, loanwords: set[str]) -> str:
    kept = [w for w in tokenize(text) if w not in loanwords]
    return " ".join(kept)


def map_neutral(raw_code: str, stripped_code: str, text: str, stripped_text: str) -> str:
    """Tommi-style strip + re-ID → 3-way label."""
    if not stripped_text.strip():
        return "ru"
    if raw_code == "kaz" or stripped_code == "kaz":
        if raw_code == "rus" and stripped_code == "kaz":
            return "kz"  # loanwords neutralized
        if raw_code == "kaz":
            return "kz"
        return "kz"
    if raw_code == "rus" and stripped_code == "rus":
        return "mixed" if has_kazakh_signal(text) else "ru"
    if stripped_code == "kaz":
        return "kz"
    return "ru"


def mixed_recall_precision(cm: pd.DataFrame) -> tuple[float, float]:
    tp = int(cm.loc["mixed", "mixed"])
    recall_mixed = tp / max(int(cm.loc["mixed"].sum()), 1)
    precision_mixed = tp / max(int(cm["mixed"].sum()), 1)
    return recall_mixed, precision_mixed


def run_eval(y_true, y_pred) -> tuple[dict, pd.DataFrame]:
    cm = pd.DataFrame(
        confusion_matrix(y_true, y_pred, labels=LABELS),
        index=LABELS,
        columns=LABELS,
    )
    cm.index.name = "true"
    cm.columns.name = "pred"
    acc = accuracy_score(y_true, y_pred)
    macro = f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)
    r_mix, p_mix = mixed_recall_precision(cm)
    return {
        "accuracy": acc,
        "macro_f1": macro,
        "recall_mixed": r_mix,
        "precision_mixed": p_mix,
    }, cm


def build_loanword_seed() -> set[str]:
    words: set[str] = set(SEED_LOANWORDS)
    # Orthographically identical ru/kz pairs from essential dict.
    for kz, ru in kazakh_dict.items():
        kz_l, ru_l = kz.lower().strip(), ru.lower().strip()
        if kz_l == ru_l and len(kz_l) >= 4 and kz_l not in FUNCTION_WORDS:
            words.add(kz_l)
    for ru, kz in essential_ru_kaz_dict.items():
        ru_l, kz_l = ru.lower().strip(), kz.lower().strip()
        if ru_l == kz_l and len(ru_l) >= 4 and ru_l not in FUNCTION_WORDS:
            words.add(ru_l)
    # Content-like popular keys: long enough, not function words, Cyrillic.
    for ru in popular_ru_kaz_dict:
        ru_l = ru.lower().strip()
        if (
            len(ru_l) >= 5
            and ru_l not in FUNCTION_WORDS
            and re.fullmatch(r"[а-яёәіңғүұқөһ\-]+", ru_l)
        ):
            # Prefer nouns that look like borrowings (no Kazakh-specific letters).
            if not any(c in KAZAKH_CHARS for c in ru_l):
                words.add(ru_l)
    return {w for w in words if w not in FUNCTION_WORDS and len(w) >= 4}


def mine_error_tokens(
    train_df: pd.DataFrame,
    identifier,
    ft_model=None,
    top_n: int = 400,
) -> list[tuple[str, int]]:
    """Frequent tokens in gold-kz rows mislabeled by FastText or HeLI raw."""
    counts: Counter[str] = Counter()
    kz = train_df[train_df["language"] == "kz"]
    for text in kz["text"].astype(str):
        code = heli_code(identifier, text)
        raw_lab = map_raw(code, text)
        ft_lab = None
        if ft_model is not None:
            t = text.replace("\n", " ").strip()
            if t:
                lab = ft_model.predict(t)[0][0].replace("__label__", "")
                ft_lab = "kz" if lab == "kaz" else lab
        if raw_lab != "kz" or (ft_lab is not None and ft_lab != "kz"):
            for tok in tokenize(text):
                if (
                    len(tok) >= 4
                    and tok not in FUNCTION_WORDS
                    and not any(c in KAZAKH_CHARS for c in tok)
                    and re.fullmatch(r"[а-яё\-]+", tok)
                ):
                    counts[tok] += 1
    return counts.most_common(top_n)


def build_loanword_list(
    train_path: Path,
    out_path: Path,
    ft_path: Path | None = None,
) -> set[str]:
    from heliport import Identifier

    identifier = Identifier()
    words = build_loanword_seed()
    train_df = pd.read_csv(train_path)
    ft_model = None
    if ft_path is not None and ft_path.exists():
        try:
            import fasttext

            # silence fasttext load warnings
            fasttext.FastText.eprint = lambda *a, **k: None
            ft_model = fasttext.load_model(str(ft_path))
        except Exception as exc:
            print(f"FastText load skipped ({ft_path}): {exc}")
            ft_model = None
    mined = mine_error_tokens(train_df, identifier, ft_model=ft_model, top_n=400)
    # Keep mined tokens that appear at least twice.
    for tok, n in mined:
        if n >= 2:
            words.add(tok)
    words = {w for w in words if w not in FUNCTION_WORDS and len(w) >= 4}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(sorted(words)) + "\n", encoding="utf-8")
    return words


def load_loanwords(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        line.strip().lower()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def predict_raw(identifier, text: str) -> str:
    return map_raw(heli_code(identifier, text), text)


def predict_neutral(identifier, text: str, loanwords: set[str]) -> tuple[str, str, str]:
    raw = heli_code(identifier, text)
    stripped = strip_loanwords(text, loanwords)
    stripped_code = heli_code(identifier, stripped) if stripped.strip() else "und"
    label = map_neutral(raw, stripped_code, text, stripped)
    return label, raw, stripped_code


def iter_windows(tokens: list[str], sizes: tuple[int, ...] = (2, 3, 4)):
    """Overlapping word windows (stride 1) for Tommi-style language-set ID."""
    n = len(tokens)
    for size in sizes:
        if size > n:
            continue
        for i in range(0, n - size + 1):
            yield " ".join(tokens[i : i + size])


def _vote_label(codes: list[str], min_count: int = 1) -> str | None:
    """Return 3-way label from kaz/rus window codes, or None if no usable votes."""
    counts: Counter[str] = Counter(c for c in codes if c in ("kaz", "rus"))
    if not counts:
        return None
    n_kaz = counts.get("kaz", 0)
    n_rus = counts.get("rus", 0)
    if n_kaz >= min_count and n_rus >= min_count:
        return "mixed"
    if n_kaz >= n_rus:
        return "kz"
    return "ru"


def predict_windows(
    identifier,
    text: str,
    loanwords: set[str],
    sizes: tuple[int, ...] = (2, 3),
    min_count: int = 1,
) -> str:
    """
    Strip loanwords, run heliport on overlapping windows, vote for mixed/kz/ru.
    Falls back to predict_neutral when fewer than 2 tokens remain after strip.
    """
    stripped = strip_loanwords(text, loanwords)
    tokens = tokenize(stripped)
    if len(tokens) < 2:
        lab, _, _ = predict_neutral(identifier, text, loanwords)
        return lab
    codes = [heli_code(identifier, w) for w in iter_windows(tokens, sizes=sizes)]
    voted = _vote_label(codes, min_count=min_count)
    if voted is None:
        lab, _, _ = predict_neutral(identifier, text, loanwords)
        return lab
    return voted


# Short-UGC size sets for Tommi-style grid (clause / span scale).
WINDOW_SIZE_GRID: tuple[tuple[int, ...], ...] = (
    (2,),
    (3,),
    (4,),
    (2, 3),
    (3, 4),
    (2, 3, 4),
    (2, 4),
    (4, 5),
    (3, 4, 5),
    (2, 3, 4, 5),
    (5,),
    (3, 5),
    (2, 3, 5),
    (4, 5, 6),
    (3, 4, 5, 6),
)
WINDOW_MIN_COUNT_GRID: tuple[int, ...] = (1, 2)


def _codes_by_size(identifier, tokens: list[str], max_size: int) -> dict[int, list[str]]:
    """heliport codes for overlapping windows of each size in 2..max_size."""
    n = len(tokens)
    out: dict[int, list[str]] = {}
    for size in range(2, max_size + 1):
        if size > n:
            out[size] = []
            continue
        out[size] = [
            heli_code(identifier, " ".join(tokens[i : i + size]))
            for i in range(0, n - size + 1)
        ]
    return out


def _label_from_codes(
    codes_by_size: dict[int, list[str]],
    sizes: tuple[int, ...],
    min_count: int,
    fallback: str,
) -> str:
    codes: list[str] = []
    for size in sizes:
        codes.extend(codes_by_size.get(size, []))
    voted = _vote_label(codes, min_count=min_count)
    return voted if voted is not None else fallback


def residual_stats(df: pd.DataFrame, identifier, loanwords: set[str]) -> dict:
    """Counts for Tommi follow-up email."""
    kz_to_neutral = 0
    mixed_still_rus = 0
    ru_broke_to_kz = 0
    for _, row in df.iterrows():
        text = str(row["text"])
        gold = row["language"]
        raw = heli_code(identifier, text)
        stripped = strip_loanwords(text, loanwords)
        stripped_code = heli_code(identifier, stripped) if stripped.strip() else "und"
        if gold == "kz" and raw == "rus" and stripped_code == "kaz":
            kz_to_neutral += 1
        if gold == "mixed" and raw == "rus" and stripped_code == "rus":
            mixed_still_rus += 1
        if gold == "ru" and stripped_code == "kaz":
            ru_broke_to_kz += 1
    return {
        "gold_kz_rus_to_kaz_after_strip": kz_to_neutral,
        "gold_mixed_still_rus_after_strip": mixed_still_rus,
        "gold_ru_broke_to_kz_after_strip": ru_broke_to_kz,
        "n": len(df),
    }


def grid_search_windows(
    test_df: pd.DataFrame,
    identifier,
    loanwords: set[str],
    size_grid: tuple[tuple[int, ...], ...] = WINDOW_SIZE_GRID,
    min_counts: tuple[int, ...] = WINDOW_MIN_COUNT_GRID,
) -> dict:
    """
    Grid over window size sets × min_count on gold test.
    Caches heliport window codes per doc once (sizes 2..max), then votes offline.
    Best config = highest macro-F1, then accuracy, then recall_mixed.
    """
    from tqdm import tqdm

    y_true = test_df["language"].tolist()
    texts = test_df["text"].astype(str).tolist()
    max_size = max(max(s) for s in size_grid)

    cache: list[dict] = []
    residual_mask: list[bool] = []
    for text, gold in tqdm(
        zip(texts, y_true),
        total=len(texts),
        desc="HeLI windows cache",
    ):
        neu_lab, raw_code, stripped_code = predict_neutral(identifier, text, loanwords)
        stripped = strip_loanwords(text, loanwords)
        tokens = tokenize(stripped)
        if len(tokens) < 2:
            codes_by_size: dict[int, list[str]] = {}
        else:
            codes_by_size = _codes_by_size(identifier, tokens, max_size)
        cache.append(
            {
                "codes_by_size": codes_by_size,
                "fallback": neu_lab,
                "n_tokens": len(tokens),
            }
        )
        residual_mask.append(
            gold == "mixed" and raw_code == "rus" and stripped_code == "rus"
        )

    rows = []
    best = None
    for sizes in size_grid:
        for min_count in min_counts:
            y_pred = [
                _label_from_codes(
                    entry["codes_by_size"], sizes, min_count, entry["fallback"]
                )
                for entry in cache
            ]
            metrics, cm = run_eval(y_true, y_pred)
            flipped = sum(
                1
                for is_res, pred in zip(residual_mask, y_pred)
                if is_res and pred == "mixed"
            )
            row = {
                "sizes": "+".join(str(s) for s in sizes),
                "sizes_tuple": sizes,
                "min_count": min_count,
                "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "recall_mixed": metrics["recall_mixed"],
                "precision_mixed": metrics["precision_mixed"],
                "residual_flip": flipped,
                "residual_n": sum(residual_mask),
            }
            rows.append(row)
            cand = {
                "sizes": sizes,
                "min_count": min_count,
                "metrics": metrics,
                "cm": cm,
                "y_pred": y_pred,
                "residual_flipped": flipped,
                "residual_n": sum(residual_mask),
            }
            if best is None:
                best = cand
            else:
                key = (
                    metrics["macro_f1"],
                    metrics["accuracy"],
                    metrics["recall_mixed"],
                )
                best_key = (
                    best["metrics"]["macro_f1"],
                    best["metrics"]["accuracy"],
                    best["metrics"]["recall_mixed"],
                )
                if key > best_key:
                    best = cand

    table = pd.DataFrame(rows).sort_values(
        ["macro_f1", "accuracy", "recall_mixed"], ascending=False
    ).reset_index(drop=True)
    return {"best": best, "table": table, "residual_mask_n": sum(residual_mask)}


def evaluate_test(
    test_path: Path,
    loanword_path: Path,
    run_windows_grid: bool = True,
) -> dict:
    from heliport import Identifier
    from tqdm import tqdm

    identifier = Identifier()
    loanwords = load_loanwords(loanword_path)
    test_df = pd.read_csv(test_path)
    y_true = test_df["language"].tolist()
    y_raw, y_neu = [], []

    for text in tqdm(
        test_df["text"].astype(str),
        total=len(test_df),
        desc="HeLI raw/neutral",
    ):
        y_raw.append(predict_raw(identifier, text))
        neu_lab, _, _ = predict_neutral(identifier, text, loanwords)
        y_neu.append(neu_lab)

    m_raw, cm_raw = run_eval(y_true, y_raw)
    m_neu, cm_neu = run_eval(y_true, y_neu)
    residuals = residual_stats(test_df, identifier, loanwords)

    out: dict = {
        "heli_m_raw": m_raw,
        "cm_heli_raw": cm_raw,
        "heli_m_neutral": m_neu,
        "cm_heli_neutral": cm_neu,
        "residuals": residuals,
        "n_loanwords": len(loanwords),
        "test_df": test_df,
        "identifier": identifier,
        "loanwords": loanwords,
    }

    if run_windows_grid:
        grid = grid_search_windows(test_df, identifier, loanwords)
        best = grid["best"]
        out["windows_grid"] = grid
        out["heli_m_windows"] = best["metrics"]
        out["cm_heli_windows"] = best["cm"]
        out["heli_windows_best_sizes"] = best["sizes"]
        out["heli_windows_best_min_count"] = best["min_count"]
        residuals["residual_mixed_still_rus"] = best["residual_n"]
        residuals["residual_80_flipped_to_mixed"] = best["residual_flipped"]
        residuals["heli_windows_best_sizes"] = "+".join(str(s) for s in best["sizes"])
        residuals["heli_windows_best_min_count"] = best["min_count"]
    return out


if __name__ == "__main__":
    train = ROOT / "data" / "training" / "filter" / "v1" / "train.csv"
    test = ROOT / "data" / "training" / "filter" / "v1" / "test.csv"
    out = ROOT / "data" / "processed" / "heli_loanwords_v1.txt"
    ft = ROOT / "models" / "fasttext" / "fasttext_v2.bin"
    if not out.exists():
        print("Building loanword list…")
        words = build_loanword_list(train, out, ft_path=ft if ft.exists() else None)
        print(f"Wrote {len(words)} loanwords → {out}")
    else:
        print(f"Using existing loanword list: {out}")
    print("Evaluating on gold test…")
    res = evaluate_test(test, out)
    print("loanwords:", res["n_loanwords"])
    print("HeLI raw:", {k: round(v, 4) for k, v in res["heli_m_raw"].items()})
    print(res["cm_heli_raw"])
    print("HeLI+neutral:", {k: round(v, 4) for k, v in res["heli_m_neutral"].items()})
    print(res["cm_heli_neutral"])
    best_sizes = res.get("heli_windows_best_sizes")
    best_mc = res.get("heli_windows_best_min_count")
    print(
        f"HeLI+windows BEST sizes={best_sizes} min_count={best_mc}:",
        {k: round(v, 4) for k, v in res["heli_m_windows"].items()},
    )
    print(res["cm_heli_windows"])
    print("grid top-10:")
    print(
        res["windows_grid"]["table"]
        .head(10)[
            [
                "sizes",
                "min_count",
                "accuracy",
                "macro_f1",
                "recall_mixed",
                "precision_mixed",
                "residual_flip",
            ]
        ]
        .round(4)
        .to_string(index=False)
    )
    print("residuals:", res["residuals"])
