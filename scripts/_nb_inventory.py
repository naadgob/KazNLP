"""One-shot: compact inventory of main.ipynb for deep-dive (no nbformat needed)."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

NB = Path("main.ipynb")
nb = json.loads(NB.read_text(encoding="utf-8"))

meta = nb.get("metadata", {})
ki = meta.get("kernelspec", {})
li = meta.get("language_info", {})
cells = nb.get("cells", [])

print(f"=== main.ipynb ===")
print(f"kernel: {ki.get('name')} / {ki.get('display_name')}  lang: {li.get('name')} {li.get('version')}")
print(f"nbformat: {nb.get('nbformat')}.{nb.get('nbformat_minor')}  total cells: {len(cells)}")
print()

METRIC = re.compile(
    r"(f1|macro|micro|weighted|accuracy|\bacc\b|precision|recall|support|"
    r"n\s*=|gold|mixed|train|test|val|corpus|rows|examples|samples|"
    r"\d[\d,]{2,}|\d+\.\d+\s*%?|%)",
    re.IGNORECASE,
)


def out_text(cell):
    chunks = []
    for o in cell.get("outputs", []):
        t = o.get("output_type")
        if t == "stream":
            chunks.append("".join(o.get("text", [])))
        elif t in ("execute_result", "display_data"):
            data = o.get("data", {})
            if "text/plain" in data:
                chunks.append("".join(data["text/plain"]))
            if "image/png" in data:
                chunks.append("[IMAGE image/png]")
        elif t == "error":
            chunks.append("ERROR: " + o.get("ename", "") + ": " + "".join(o.get("evalue", ""))[:200])
    return "\n".join(chunks)


for i, cell in enumerate(cells):
    ct = cell.get("cell_type")
    src = "".join(cell.get("source", []))
    src_lines = [l for l in src.splitlines() if l.strip()]
    if ct == "markdown":
        heads = [l for l in src_lines if l.lstrip().startswith("#")]
        label = " | ".join(heads) if heads else (src_lines[0][:90] if src_lines else "(empty md)")
        print(f"[{i:>3}] MD   {label}")
    elif ct == "code":
        ec = cell.get("execution_count")
        first = src_lines[0][:100] if src_lines else "(empty)"
        flag = "" if ec is not None else "  <UNRUN>"
        print(f"[{i:>3}] CODE(ec={ec}){flag} {first}")
        # surface metric-bearing output lines
        ot = out_text(cell)
        if ot:
            keep = []
            for line in ot.splitlines():
                s = line.strip()
                if not s:
                    continue
                if METRIC.search(s):
                    keep.append(s[:160])
            for s in keep[:25]:
                print(f"        > {s}")
            if len(keep) > 25:
                print(f"        > ... (+{len(keep)-25} more metric lines)")
    else:
        print(f"[{i:>3}] {ct.upper()}")
