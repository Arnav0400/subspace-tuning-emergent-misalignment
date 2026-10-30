#!/usr/bin/env python3
"""Build static article tables and downloadable CSV from verified result data."""
import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/results.json").read_text())
METHOD_CLASSES = {"Base": "base", "SFT": "sft", "SST 90%": "sst90", "SST 99%": "sst99"}


def label(row):
    return '<span class="swatch {}"></span>{}'.format(
        METHOD_CLASSES[row["method"]], html.escape(row["method"])
    )


def tr(cells, featured=False):
    return '<tr{}>{}</tr>'.format(
        ' class="featured"' if featured else "",
        "".join("<td>{}</td>".format(cell) for cell in cells),
    )


def main():
    rows = DATA["selected"]
    replacements = {
        "SELECTED_ROWS": "\n".join(
            tr([label(r), f'{r["id_pct"]:.0f}', f'{r["mmlu_pro_pct"]:.2f}',
                f'{r["em_macro_pct"]:.2f}', f'{r["eligible_coverage_pct"]:.2f}'],
               r["method"] == "SST 90%") for r in rows
        ),
        "DENOMINATOR_ROWS": "\n".join(
            tr([label(r), f'{r["em_n_misaligned"]} / {r["em_n_eligible"]:,}',
                f'{r["em_pooled_pct"]:.2f}%', f'{r["em_all_answers_pct"]:.2f}%'])
            for r in rows
        ),
        "SWEEP_ROWS": "\n".join(
            tr([label(r), f'{r["learning_rate"]:.0e}', f'{r["id_pct"]:.0f}%',
                f'{r["mmlu_pro_pct"]:.2f}%', f'{r["em_macro_pct"]:.2f}%'])
            for r in DATA["runs"] if r["learning_rate"] is not None
        ),
    }
    article = (ROOT / "index.template.html").read_text()
    for key, value in replacements.items():
        article = article.replace("{{" + key + "}}", value)
    if "{{" in article:
        raise ValueError("Unresolved template field")
    (ROOT / "index.html").write_text(article)
    (ROOT / "data/muon.json").write_text(
        json.dumps(DATA["muon_followup"], indent=2) + "\n"
    )
    fields = ["run_id", "method", "learning_rate", "selected", "id_n_vulnerable", "id_n",
              "id_pct", "mmlu_pro_n_correct", "mmlu_pro_n", "mmlu_pro_pct",
              "em_macro_pct", "em_pooled_pct", "eligible_coverage_pct",
              "em_all_answers_pct", "em_n_misaligned", "em_n_eligible", "em_n_generated"]
    with (ROOT / "data/results.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(DATA["runs"])
    print("Built index.html, data/results.csv, and data/muon.json from verified results.")


if __name__ == "__main__":
    main()
