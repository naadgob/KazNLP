"""Insert §7.3 tone eval cells into main.ipynb and update footer."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "main.ipynb"


def _id() -> str:
    return uuid.uuid4().hex[:8]


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    cells = nb["cells"]

    # Skip if §7.3 already present
    for c in cells:
        src = "".join(c.get("source", []))
        if "## 7.3" in src and "eval_tone_v1" in src:
            print("§7.3 already present — skip insert")
            break
    else:
        idx = next(
            (i for i, c in enumerate(cells) if c.get("id") == "e5946d59"),
            None,
        )
        if idx is None:
            raise SystemExit("cell e5946d59 not found")

        new_cells = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 7.3 Оценка Mixed Tone v1 / v2 на hold-out test\n"],
                "id": _id(),
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "<!-- kaznlp-narration -->\n",
                    "**Действие:** загрузка весов `tone_v1.pt` и `tone/xlm-r_v2.pt`, "
                    "оценка на `data/training/tone/v1/test.csv` (525 строк).\n\n"
                    "**Вывод:** v1 — production (accuracy ~97.3%); v2 хуже (~96.2%). "
                    "Метрики также в `data/processed/metrics_tone_test.json`.\n",
                ],
                "id": _id(),
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": [
                    "import subprocess\n",
                    "import sys\n",
                    "\n",
                    "subprocess.run([sys.executable, 'scripts/eval_tone_v1.py'], check=True)\n",
                ],
                "outputs": [],
                "execution_count": None,
                "id": _id(),
            },
        ]
        cells[idx + 1 : idx + 1] = new_cells
        print(f"Inserted §7.3 at index {idx + 1}")

    # Update footer
    for c in cells:
        src = "".join(c.get("source", []))
        if "<!-- kaznlp-footer -->" in src:
            c["source"] = [
                "<!-- kaznlp-footer -->\n",
                "## Итог пайплайна и next steps\n\n",
                "| Этап | Статус | Артефакт |\n",
                "|------|--------|----------|\n",
                "| FastText LID | ✅ | `models/fasttext/fasttext_v1.bin`, `fasttext_v2.bin` |\n",
                "| Сбор | ✅ | Telegram, Kaspi, 2GIS |\n",
                "| Gold LID | ✅ | `gold_v1.csv` (3076) |\n",
                "| XLM-R LID v2 | ✅ | `xlm-r_v2.pt`, macro-F1 96.56% |\n",
                "| Tone gold + train | ✅ | 3529 + 4411 |\n",
                "| **Mixed Tone v1** | ✅ | `tone_v1.pt`, test acc **97.3%** (§7.3) |\n",
                "| Demo | ✅ | `run_demo.py` + `web/` |\n\n",
                "**Eval tone:** `python scripts/eval_tone_v1.py`\n",
            ]
            print("Updated kaznlp-footer")
            break

    NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
