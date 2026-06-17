"""Step 0 EDA for gold_v1.csv — run once, print report."""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "labeling_service"))

from precision_filter import has_kazakh_signal, has_russian_signal, KAZAKH_CHARS
from text_heuristics import has_kazakh_letters

GOLD = ROOT / "data" / "processed" / "gold_v1.csv"

WORD_RE = re.compile(r"[\w']+", re.UNICODE)
LATIN_RE = re.compile(r"[a-zA-Z]{2,}")
USER_RE = re.compile(r"\[USER\]|@\w+")
DIGIT_RE = re.compile(r"\d")


def normalize_text(text) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    t = str(text).strip().casefold()
    t = re.sub(r"https?://\S+|t\.me/\S+", " ", t, flags=re.I)
    t = re.sub(r"@[\w.]+", "[USER]", t)
    t = re.sub(r"#(\w+)", r"\1", t)
    t = re.sub(r"[^\w\s.,!?\-']", " ", t, flags=re.UNICODE)
    t = re.sub(r"([)\]}])\1{2,}", r"\1", t)
    t = re.sub(r"([:;])\1{2,}", r"\1", t)
    t = re.sub(r"!{2,}", "!", t)
    t = re.sub(r"\?{2,}", "?", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def word_count(text: str) -> int:
    return len(WORD_RE.findall(str(text)))


def char_count(text: str) -> int:
    return len(str(text).strip())


def pct(n: int, total: int) -> str:
    return f"{100 * n / total:.1f}%" if total else "0%"


def stats_series(series: pd.Series) -> dict:
    return {
        "mean": series.mean(),
        "median": series.median(),
        "p10": series.quantile(0.1),
        "p90": series.quantile(0.9),
        "min": series.min(),
        "max": series.max(),
    }


def pick_examples(df: pd.DataFrame, lang: str, n: int = 20) -> list[tuple[str, str, int, int]]:
    sub = df[df["language"] == lang].copy()
    sub["wc"] = sub["text"].map(word_count)
    sub["cc"] = sub["text"].map(char_count)
    picks: list[tuple[str, str, int, int]] = []

    # short
    for _, r in sub.nsmallest(5, "wc").iterrows():
        picks.append(("short", str(r["text"]), r["wc"], r["cc"]))
    # long
    for _, r in sub.nlargest(5, "wc").iterrows():
        picks.append(("long", str(r["text"]), r["wc"], r["cc"]))
    # borderline mixed/kz
    if lang == "mixed":
        sub["has_kz_letters"] = sub["text"].map(has_kazakh_letters)
        no_kz = sub[~sub["has_kz_letters"]].head(3)
        for _, r in no_kz.iterrows():
            picks.append(("border:no_kz_letters", str(r["text"]), r["wc"], r["cc"]))
    if lang == "kz":
        sub["has_ru_sig"] = sub["text"].map(has_russian_signal)
        loan = sub[sub["has_ru_sig"]].head(5)
        for _, r in loan.iterrows():
            picks.append(("border:ru_loanwords", str(r["text"]), r["wc"], r["cc"]))
        no_kz_letters = sub[~sub["text"].map(has_kazakh_letters)].head(5)
        for _, r in no_kz_letters.iterrows():
            picks.append(("border:no_kz_letters", str(r["text"]), r["wc"], r["cc"]))
    if lang == "ru":
        sub["has_kz"] = sub["text"].map(has_kazakh_letters)
        with_kz = sub[sub["has_kz"]].head(5)
        for _, r in with_kz.iterrows():
            picks.append(("border:kz_letters", str(r["text"]), r["wc"], r["cc"]))

    # dedupe by text
    seen = set()
    out = []
    for tag, text, wc, cc in picks:
        if text in seen:
            continue
        seen.add(text)
        out.append((tag, text, wc, cc))
        if len(out) >= n:
            break
    return out


def near_dup_groups(texts: list[str], threshold: float = 0.92) -> int:
    """Simple Jaccard on word sets for near-dup count (sample if huge)."""
    from difflib import SequenceMatcher

    norms = [normalize_text(t) for t in texts]
    groups = 0
    used = set()
    for i in range(len(norms)):
        if i in used or not norms[i]:
            continue
        wi = set(WORD_RE.findall(norms[i]))
        if len(wi) < 3:
            continue
        for j in range(i + 1, len(norms)):
            if j in used or not norms[j]:
                continue
            wj = set(WORD_RE.findall(norms[j]))
            if not wj:
                continue
            inter = len(wi & wj)
            union = len(wi | wj)
            if union and inter / union >= threshold:
                used.add(j)
                groups += 1
        if i not in used and any(j in used for j in range(i + 1, len(norms))):
            used.add(i)
    return groups


def mixed_patterns(df: pd.DataFrame) -> dict:
    mixed = df[df["language"] == "mixed"]["text"].astype(str)
    patterns = Counter()
    for t in mixed:
        tl = t.lower()
        if "алға" in tl or "алga" in tl:
            patterns["алға/алga"] += 1
        if re.search(r"[а-яё]{4,}.*[әіңғүұқөһ]", t, re.I) or re.search(
            r"[әіңғүұқөһ].*[а-яё]{4,}", t, re.I
        ):
            patterns["ru_chunk+kz_chunk_same_comment"] += 1
        if "." in t and has_russian_signal(t) and has_kazakh_signal(t):
            parts = re.split(r"[.!?]+", t)
            langs = []
            for p in parts:
                p = p.strip()
                if len(p) < 4:
                    continue
                if has_russian_signal(p) and not has_kazakh_signal(p):
                    langs.append("ru")
                elif has_kazakh_signal(p) and not has_russian_signal(p):
                    langs.append("kz")
                elif has_russian_signal(p) and has_kazakh_signal(p):
                    langs.append("mix")
            if len(set(langs)) >= 2:
                patterns["two_sentences_diff_lang"] += 1
        if "және" in tl or "бірақ" in tl:
            patterns["kz_connector_in_mixed"] += 1
        if "качество" in tl and any(c in tl for c in KAZAKH_CHARS):
            patterns["качество+kz_word"] += 1
    return dict(patterns.most_common(15))


def kz_loanword_reviews(df: pd.DataFrame) -> list[str]:
    """KZ labeled but has 'качество' + kz morphology — NOT mixed per guide."""
    out = []
    kz = df[df["language"] == "kz"]["text"].astype(str)
    for t in kz:
        tl = t.lower()
        if "качество" in tl or "качеств" in tl:
            out.append(t)
    return out[:10]


def compare_text_norm(df: pd.DataFrame) -> dict:
    recomputed = df["text"].map(normalize_text)
    existing = df["text_norm"].astype(str).str.strip()
    match = (recomputed == existing).sum()
    mismatch = len(df) - match
    samples = []
    diff_mask = recomputed != existing
    for i, row in df[diff_mask].head(10).iterrows():
        samples.append(
            {
                "text": str(row["text"])[:100],
                "existing": str(row["text_norm"])[:100],
                "recomputed": recomputed.iloc[i][:100],
            }
        )
    return {"match": int(match), "mismatch": int(mismatch), "samples": samples}


def boundary_check(df: pd.DataFrame) -> dict:
    """After normalize: do heuristics flip labels?"""
    df = df.copy()
    df["norm"] = df["text"].map(normalize_text)
    issues = defaultdict(list)

    for _, r in df.iterrows():
        lang = r["language"]
        t = r["norm"]
        sig_ru = has_russian_signal(t)
        sig_kz = has_kazakh_signal(t)
        wc = word_count(t)

        if lang == "mixed":
            if not (sig_ru and sig_kz):
                issues["mixed_loses_bilingual_after_norm"].append(t[:120])
        elif lang == "kz":
            if sig_ru and sig_kz and wc >= 6:
                issues["kz_looks_mixed_after_norm"].append(t[:120])
        elif lang == "ru":
            if sig_kz and has_kazakh_letters(t):
                issues["ru_has_kz_letters_after_norm"].append(t[:120])

    return {k: (len(v), v[:5]) for k, v in issues.items()}


def main() -> None:
    df = pd.read_csv(GOLD)
    print("=" * 60)
    print("GOLD FILE:", GOLD)
    print("ROWS:", len(df))
    print("\nCLASS DISTRIBUTION:")
    print(df["language"].value_counts().to_string())
    print("\nEXACT DUP text:", df["text"].duplicated().sum())
    print("EXACT DUP text (after normalize_text):", df["text"].map(normalize_text).duplicated().sum())

    df["wc"] = df["text"].map(word_count)
    df["cc"] = df["text"].map(char_count)

    print("\n--- LENGTH BY CLASS (words) ---")
    for lang in ["ru", "kz", "mixed"]:
        s = df.loc[df["language"] == lang, "wc"]
        st = stats_series(s)
        print(f"{lang}: mean={st['mean']:.1f} med={st['median']:.0f} p10={st['p10']:.0f} p90={st['p90']:.0f} min={st['min']:.0f} max={st['max']:.0f}")

    print("\n--- LENGTH BY CLASS (chars) ---")
    for lang in ["ru", "kz", "mixed"]:
        s = df.loc[df["language"] == lang, "cc"]
        st = stats_series(s)
        print(f"{lang}: mean={st['mean']:.1f} med={st['median']:.0f} p10={st['p10']:.0f} p90={st['p90']:.0f} min={st['min']:.0f} max={st['max']:.0f}")

    print("\n--- SHORT TEXTS (<=3 words) ---")
    for lang in ["ru", "kz", "mixed"]:
        n = ((df["language"] == lang) & (df["wc"] <= 3)).sum()
        total = (df["language"] == lang).sum()
        print(f"{lang}: {n}/{total} ({pct(n, total)})")

    print("\n--- LATIN / [USER] / DIGITS ---")
    for lang in ["ru", "kz", "mixed"]:
        sub = df[df["language"] == lang]
        n = len(sub)
        latin = sub["text"].astype(str).map(lambda t: bool(LATIN_RE.search(t))).sum()
        user = sub["text"].astype(str).map(lambda t: bool(USER_RE.search(t))).sum()
        digits = sub["text"].astype(str).map(lambda t: bool(DIGIT_RE.search(t))).sum()
        print(f"{lang}: latin={pct(latin, n)} user={pct(user, n)} digits={pct(digits, n)}")

    print("\n--- KAZAKH LETTERS (ә/ң/…) ---")
    for lang in ["ru", "kz", "mixed"]:
        sub = df[df["language"] == lang]
        n = len(sub)
        has = sub["text"].map(has_kazakh_letters).sum()
        print(f"{lang}: {has}/{n} ({pct(has, n)})")

    print("\n--- KZ WITHOUT KAZAKH LETTERS ---")
    kz = df[df["language"] == "kz"]
    no_letters = kz[~kz["text"].map(has_kazakh_letters)]
    print(f"count: {len(no_letters)}/{len(kz)} ({pct(len(no_letters), len(kz))})")

    print("\n--- MIXED PATTERNS ---")
    for k, v in mixed_patterns(df).items():
        print(f"  {k}: {v}")

    print("\n--- KZ with 'качество' (loanword, NOT mixed) ---")
    for t in kz_loanword_reviews(df):
        print(f"  · {t[:120]}")

    print("\n--- TEXT_NORM COMPARISON ---")
    cmp = compare_text_norm(df)
    print(f"match existing text_norm: {cmp['match']}/{len(df)}, mismatch: {cmp['mismatch']}")
    if cmp["samples"]:
        print("mismatch samples:")
        for s in cmp["samples"][:5]:
            print(" ", s)

    print("\n--- BOUNDARY CHECK AFTER normalize_text ---")
    bc = boundary_check(df)
    for k, (cnt, samples) in bc.items():
        print(f"{k}: {cnt}")
        for s in samples:
            print(f"  · {s}")

    print("\n--- NEAR-DUPLICATES (Jaccard words >=0.92, per class) ---")
    for lang in ["ru", "kz", "mixed"]:
        sub = df[df["language"] == lang]["text"].tolist()
        nd = near_dup_groups(sub)
        print(f"{lang}: ~{nd} near-dup pairs")

    print("\n--- EXAMPLES ---")
    for lang in ["ru", "kz", "mixed"]:
        print(f"\n### {lang.upper()} ###")
        for tag, text, wc, cc in pick_examples(df, lang, 18):
            print(f"[{tag}] ({wc}w/{cc}c) {text[:200]}")

    # heuristic mislabel flags from text_heuristics
    from text_heuristics import label_heuristics

    print("\n--- HEURISTIC LABEL FLAGS ---")
    for lang in ["ru", "kz", "mixed"]:
        sub = df[df["language"] == lang]
        flags = Counter()
        for _, r in sub.iterrows():
            h = label_heuristics(str(r["text"]), r["language"])
            for reason in h["mismatch_reasons"]:
                flags[reason] += 1
        print(f"{lang}: {dict(flags.most_common(8))}")


if __name__ == "__main__":
    main()
