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


def evaluate_test(
    test_path: Path,
    loanword_path: Path,
) -> dict:
    from heliport import Identifier
    from tqdm import tqdm

    identifier = Identifier()
    loanwords = load_loanwords(loanword_path)
    test_df = pd.read_csv(test_path)
    y_true = test_df["language"].tolist()
    y_raw, y_neu = [], []
    for text in tqdm(test_df["text"].astype(str), desc="HeLI eval"):
        y_raw.append(predict_raw(identifier, text))
        lab, _, _ = predict_neutral(identifier, text, loanwords)
        y_neu.append(lab)
    m_raw, cm_raw = run_eval(y_true, y_raw)
    m_neu, cm_neu = run_eval(y_true, y_neu)
    residuals = residual_stats(test_df, identifier, loanwords)
    return {
        "heli_m_raw": m_raw,
        "cm_heli_raw": cm_raw,
        "heli_m_neutral": m_neu,
        "cm_heli_neutral": cm_neu,
        "residuals": residuals,
        "n_loanwords": len(loanwords),
        "test_df": test_df,
    }


if __name__ == "__main__":
    train = ROOT / "data" / "training" / "filter" / "v1" / "train.csv"
    test = ROOT / "data" / "training" / "filter" / "v1" / "test.csv"
    out = ROOT / "data" / "processed" / "heli_loanwords_v1.txt"
    ft = ROOT / "models" / "fasttext" / "fasttext_v2.bin"
    print("Building loanword list…")
    words = build_loanword_list(train, out, ft_path=ft if ft.exists() else None)
    print(f"Wrote {len(words)} loanwords → {out}")
    print("Evaluating on gold test…")
    res = evaluate_test(test, out)
    print("loanwords:", res["n_loanwords"])
    print("HeLI raw:", {k: round(v, 4) for k, v in res["heli_m_raw"].items()})
    print(res["cm_heli_raw"])
    print("HeLI+neutral:", {k: round(v, 4) for k, v in res["heli_m_neutral"].items()})
    print(res["cm_heli_neutral"])
    print("residuals:", res["residuals"])
