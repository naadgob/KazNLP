"""Audit synthetic LID data vs gold and labeling rules."""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "labeling_service"))
sys.path.insert(0, str(ROOT / "scripts"))

from merge_synthetic import normalize_text, qc_row, word_count
from precision_filter import has_kazakh_signal, has_russian_signal, KAZAKH_CHARS
from text_heuristics import has_kazakh_letters, label_heuristics

GOLD = ROOT / "data/processed/gold_v1.csv"
SYNTH = ROOT / "data/processed/synthetic/synthetic_all.csv"
OUT = ROOT / "data/processed/synthetic/synthetic_audit_report.txt"

WORD_RE = re.compile(r"[\w']+", re.UNICODE)
RU_SENT_RE = re.compile(r"[а-яё]{4,}", re.I)
KZ_SPECIAL_RE = re.compile(r"[әіңғүұқөһ]", re.I)


def ru_chunk_ok(text: str) -> bool:
    words = WORD_RE.findall(text.lower())
    ru_words = [w for w in words if re.search(r"[а-яё]", w) and not any(c in w for c in KAZAKH_CHARS)]
    return len(ru_words) >= 2


def kz_chunk_ok(text: str) -> bool:
    if has_kazakh_signal(text):
        return True
    words = WORD_RE.findall(text.lower())
    kz_words = [w for w in words if any(c in w for c in KAZAKH_CHARS)]
    return len(kz_words) >= 2


def strict_mixed_ok(text: str) -> tuple[bool, str]:
    """Project rule: >=2-3 ru words AND >=2-3 kz words, OR two sentences."""
    t = str(text)
    parts = [p.strip() for p in re.split(r"[.!?]+", t) if len(p.strip()) >= 4]
    ru_s = sum(1 for p in parts if has_russian_signal(p) and not has_kazakh_signal(p))
    kz_s = sum(1 for p in parts if has_kazakh_signal(p) and not has_russian_signal(p))
    if ru_s >= 1 and kz_s >= 1:
        return True, "two_sentences"
    if ru_chunk_ok(t) and kz_chunk_ok(t):
        return True, "intra_sentential"
    # short mixed: at least one ru word cluster + kz signal
    if ru_chunk_ok(t) and has_kazakh_signal(t):
        return True, "short_mixed"
    return False, "weak"


def strict_kz_ok(text: str) -> tuple[bool, str]:
    t = str(text)
    parts = [p.strip() for p in re.split(r"[.!?]+", t) if len(p.strip()) >= 4]
    ru_only = sum(1 for p in parts if has_russian_signal(p) and not has_kazakh_signal(p))
    kz_only = sum(1 for p in parts if has_kazakh_signal(p) and not has_russian_signal(p))
    if ru_only >= 1 and kz_only >= 1:
        return False, "looks_mixed_two_sentences"
    if not has_kazakh_signal(t) and not has_kazakh_letters(t):
        # shala translit kz allowed
        latin_mix = sum(1 for w in WORD_RE.findall(t.lower()) if re.match(r"[a-z]{3,}", w))
        if latin_mix >= 3 and not any(c in t for c in "ыіұү"):
            return False, "mostly_latin_gibberish"
    return True, "ok"


def strict_ru_ok(text: str) -> tuple[bool, str]:
    if has_kazakh_letters(text):
        return False, "has_kz_letters"
    if has_kazakh_signal(text) and has_russian_signal(text):
        return False, "bilingual_signal"
    return True, "ok"


def length_stats(df: pd.DataFrame) -> dict:
    wc = df["text"].map(word_count)
    return {
        "mean": round(wc.mean(), 1),
        "median": int(wc.median()),
        "p10": int(wc.quantile(0.1)),
        "p90": int(wc.quantile(0.9)),
        "min": int(wc.min()),
        "max": int(wc.max()),
    }


def gap_coverage(synth: pd.DataFrame) -> dict:
    m = synth[synth.language == "mixed"]
    k = synth[synth.language == "kz"]
    return {
        "mixed_short_le5": int((m.text.map(word_count) <= 5).sum()),
        "mixed_no_kz_letters": int((~m.text.map(has_kazakh_letters)).sum()),
        "mixed_kaspi_like": int(m.text.str.lower().str.contains(r"kaspi|каспи|курьер|доставк|магазин|продав").sum()),
        "mixed_alga": int(m.text.str.lower().str.contains(r"алға|алga|qazaqstan").sum()),
        "kz_no_special_letters": int((~k.text.map(has_kazakh_letters)).sum()),
        "kz_quality_loan": int(k.text.str.lower().str.contains(r"качество|quality|kachestvo").sum()),
        "kz_hard_neg_pattern": int(k.text.str.lower().str.contains(r"quality|service|delivery|product|store").sum()),
    }


def audit_class(df: pd.DataFrame, lang: str) -> dict:
    sub = df[df.language == lang]
    issues: Counter = Counter()
    examples: dict[str, list] = defaultdict(list)
    ok = 0
    for _, r in sub.iterrows():
        t = r["text"]
        if lang == "mixed":
            good, reason = strict_mixed_ok(t)
        elif lang == "kz":
            good, reason = strict_kz_ok(t)
        else:
            good, reason = strict_ru_ok(t)
        if good:
            ok += 1
        else:
            issues[reason] += 1
            if len(examples[reason]) < 5:
                examples[reason].append(t[:120])
        # heuristic flags
        for reason in label_heuristics(t, lang)["mismatch_reasons"]:
            issues[f"heur:{reason}"] += 1
    return {
        "n": len(sub),
        "strict_ok_pct": round(100 * ok / max(len(sub), 1), 1),
        "issues": dict(issues.most_common(15)),
        "examples": dict(examples),
    }


def overlap_with_gold(synth: pd.DataFrame, gold: pd.DataFrame) -> dict:
    g_norm = set(gold.text.map(normalize_text))
    s_norm = synth.text.map(normalize_text)
    exact = s_norm.isin(g_norm).sum()
    # near dup jaccard
    g_words = [set(WORD_RE.findall(normalize_text(t))) for t in gold.text if len(str(t)) > 10]
    near = 0
    for t in synth.text.sample(min(200, len(synth)), random_state=42):
        wi = set(WORD_RE.findall(normalize_text(t)))
        if len(wi) < 3:
            continue
        for wg in g_words:
            if not wg:
                continue
            j = len(wi & wg) / len(wi | wg)
            if j >= 0.92:
                near += 1
                break
    return {"exact_norm_dup": int(exact), "near_dup_sample_200": near}


def style_drift(synth: pd.DataFrame, gold: pd.DataFrame) -> dict:
    """Compare synthetic vs gold style signals."""
    def signals(df):
        t = df.text.astype(str)
        return {
            "latin_pct": (t.str.contains(r"[a-zA-Z]{3,}", regex=True)).mean(),
            "emoji_pct": (t.str.contains(r"[\U0001F300-\U0001FAFF😂🙊😁]", regex=True)).mean(),
            "newsish_pct": (t.str.len() > 200).mean(),
            "avg_words": t.map(word_count).mean(),
        }
    out = {}
    for lang in ["ru", "kz", "mixed"]:
        out[f"gold_{lang}"] = signals(gold[gold.language == lang])
        out[f"synth_{lang}"] = signals(synth[synth.language == lang])
    return out


def high_risk_rows(synth: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i, r in synth.iterrows():
        lang = r["language"]
        t = r["text"]
        risk = []
        if lang == "mixed":
            ok, reason = strict_mixed_ok(t)
            if not ok:
                risk.append(f"strict:{reason}")
        elif lang == "kz":
            ok, reason = strict_kz_ok(t)
            if not ok:
                risk.append(f"strict:{reason}")
        else:
            ok, reason = strict_ru_ok(t)
            if not ok:
                risk.append(f"strict:{reason}")
        if qc_row(t, lang):
            risk.append("qc:" + ",".join(qc_row(t, lang)))
        if risk:
            rows.append({**r.to_dict(), "risk": "; ".join(risk)})
    return pd.DataFrame(rows)


def main() -> None:
    gold = pd.read_csv(GOLD)
    synth = pd.read_csv(SYNTH)

    lines = [
        "=" * 60,
        "SYNTHETIC DATA AUDIT — KazNLP LID",
        "=" * 60,
        f"Gold: {len(gold)} | Synthetic: {len(synth)}",
        f"Synthetic by class: {synth.language.value_counts().to_dict()}",
        "",
        "--- OVERLAP WITH GOLD ---",
        str(overlap_with_gold(synth, gold)),
        "",
        "--- GAP COVERAGE (weak spots) ---",
        str(gap_coverage(synth)),
        "",
        "--- LENGTH vs GOLD ---",
    ]
    for lang in ["ru", "kz", "mixed"]:
        lines.append(f"{lang} gold words: {length_stats(gold[gold.language==lang])}")
        lines.append(f"{lang} synth words: {length_stats(synth[synth.language==lang])}")
    lines.append("")
    lines.append("--- STRICT LABEL AUDIT (project rules) ---")
    for lang in ["mixed", "kz", "ru"]:
        a = audit_class(synth, lang)
        lines.append(f"\n## {lang.upper()} n={a['n']} strict_ok={a['strict_ok_pct']}%")
        lines.append(f"issues: {a['issues']}")
        for k, ex in a.get("examples", {}).items():
            lines.append(f"  [{k}] examples:")
            for e in ex:
                lines.append(f"    · {e}")

    lines.append("\n--- STYLE DRIFT (synth vs gold) ---")
    sd = style_drift(synth, gold)
    for k, v in sd.items():
        lines.append(f"{k}: {v}")

    risk = high_risk_rows(synth)
    strict_fail = risk[risk["risk"].str.contains("strict:", na=False)]
    lines.append(f"\n--- HIGH RISK ROWS (strict rule fail): {len(strict_fail)} ---")
    for _, r in strict_fail.head(25).iterrows():
        lines.append(f"[{r['language']}] {r['risk']} | {r['text'][:100]}")

    # verdict buckets
    mixed_audit = audit_class(synth, "mixed")
    kz_audit = audit_class(synth, "kz")
    ru_audit = audit_class(synth, "ru")

    lines.extend([
        "",
        "=" * 60,
        "VERDICT",
        "=" * 60,
    ])

    total_strict_ok = (
        mixed_audit["strict_ok_pct"] * mixed_audit["n"]
        + kz_audit["strict_ok_pct"] * kz_audit["n"]
        + ru_audit["strict_ok_pct"] * ru_audit["n"]
    ) / len(synth)

    lines.append(f"Overall strict label pass rate: {total_strict_ok:.1f}%")
    lines.append(f"High-risk strict failures: {len(strict_fail)} ({100*len(strict_fail)/len(synth):.1f}%)")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    risk_path = ROOT / "data/processed/synthetic/synthetic_audit_high_risk.csv"
    strict_fail.to_csv(risk_path, index=False, encoding="utf-8-sig")

    print("\n".join(lines[-30:]))
    print(f"\nFull report: {OUT}")
    print(f"High risk CSV: {risk_path}")


if __name__ == "__main__":
    main()
