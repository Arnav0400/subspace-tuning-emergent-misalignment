#!/usr/bin/env python3
"""Render the article's figures from its published, unrounded result data.

Usage: python scripts/plot_results.py
Requires matplotlib. Figures intentionally show point estimates: one training
seed does not provide between-seed uncertainty, and learning rates are not
independent seed replicates.
"""

from pathlib import Path
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "results.json").read_text())
OUTPUT = ROOT / "assets"
OUTPUT.mkdir(exist_ok=True)

BG = "#fbfaf7"
INK = "#25313a"
MUTED = "#66717b"
GRID = "#e3e4df"
COLORS = {
    "Base": "#718096",
    "SFT": "#bb6848",
    "SST 90%": "#087f82",
    "SST 99%": "#7773ad",
}
METHODS = list(COLORS)
SELECTED = {row["method"]: row for row in DATA["selected"]}

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "text.color": INK,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": False,
        "svg.fonttype": "none",
        "svg.hashsalt": "sst-em-blog-v1",
    }
)


def frame(ax, title, subtitle, xmax, ticks, show_names):
    ax.set_title(title, loc="left", weight="bold", fontsize=12, pad=28)
    ax.text(
        0,
        1.025,
        subtitle,
        transform=ax.transAxes,
        va="bottom",
        fontsize=9.4,
        color=MUTED,
    )
    ax.set_xlim(0, xmax)
    ax.set_ylim(3.6, -0.65)
    ax.set_yticks(range(4), METHODS if show_names else [""] * 4)
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{tick:g}%" for tick in ticks], fontsize=9.5)
    ax.tick_params(axis="both", length=0, pad=8)
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.axvline(0, color=GRID, linewidth=1)
    ax.set_axisbelow(True)


def bars(ax, values, xmax, decimals=2, counts=None):
    for y, (method, value) in enumerate(zip(METHODS, values)):
        if value:
            ax.barh(
                y,
                value,
                height=0.45,
                color=COLORS[method],
                linewidth=0,
                zorder=2,
            )
        else:
            ax.plot(0, y, "|", color=COLORS[method], markersize=13, clip_on=False)
        label = f"{value:.{decimals}f}%"
        if counts is not None:
            label += f" ({counts[y]:,})"
        ax.text(
            value + xmax * 0.025,
            y,
            label,
            va="center",
            fontsize=10.5,
            color=INK,
            clip_on=False,
        )


def save(fig, name, note):
    fig.text(0.015, 0.035, note, fontsize=9.2, color=MUTED, va="bottom")
    metadata = {
        "Title": name.replace("-", " ").title(),
        "Description": note,
        "Creator": "scripts/plot_results.py",
        "Date": None,
    }
    fig.savefig(
        OUTPUT / f"{name}.svg",
        bbox_inches="tight",
        pad_inches=0.18,
        metadata=metadata,
    )
    svg = OUTPUT / f"{name}.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    fig.savefig(
        OUTPUT / f"{name}.png",
        dpi=200,
        bbox_inches="tight",
        pad_inches=0.18,
    )
    plt.close(fig)


def outcome_summary():
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.7))
    fig.subplots_adjust(left=0.095, right=0.965, top=0.77, bottom=0.22, wspace=0.30)
    specs = [
        ("Insecure-code uptake", "Judged vulnerable · 100 prompts", "id_pct", 108, [0, 50, 100], 0),
        ("MMLU-Pro", "Accuracy · 12,032 questions", "mmlu_pro_pct", 70, [0, 30, 60], 2),
        ("Preregistered EM", "Question-average conditional rate", "em_macro_pct", 10.5, [0, 5, 10], 2),
    ]
    for n, (title, subtitle, key, xmax, ticks, decimals) in enumerate(specs):
        frame(axes[n], title, subtitle, xmax, ticks, n == 0)
        bars(axes[n], [SELECTED[m][key] for m in METHODS], xmax, decimals)
    save(
        fig,
        "outcome-summary",
        "Selected final models: highest insecure-ID score per method, all at LR 2e−5. One training seed; fixed SST bases.",
    )


def coverage():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.75))
    fig.subplots_adjust(left=0.095, right=0.965, top=0.77, bottom=0.23, wspace=0.31)
    specs = [
        (
            "Answers eligible for EM",
            "Numeric alignment + coherence >50; excludes CODE / REFUSAL",
            "eligible_coverage_pct",
            "em_n_eligible",
            137,
            [0, 25, 50, 75, 100],
        ),
        (
            "Scored misaligned / all answers",
            "The same misaligned count, divided by all 4,800 generations",
            "em_all_answers_pct",
            "em_n_misaligned",
            3.6,
            [0, 1, 2, 3],
        ),
    ]
    for n, (title, subtitle, key, count_key, xmax, ticks) in enumerate(specs):
        frame(axes[n], title, subtitle, xmax, ticks, n == 0)
        bars(
            axes[n],
            [SELECTED[m][key] for m in METHODS],
            xmax,
            counts=[SELECTED[m][count_key] for m in METHODS],
        )
    save(
        fig,
        "coverage",
        "Preregistered set: 48 questions × 100 answers per model. Parentheses show counts. Excluded answers are not certified harmless.",
    )


def formats():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.7))
    fig.subplots_adjust(left=0.10, right=0.96, top=0.77, bottom=0.22, wspace=0.27)
    lookup = {
        (row["method"], row["suite"]): row for row in DATA["prompt_families"]
    }
    for n, (suite, label) in enumerate(
        [("em_json", "Answer in JSON"), ("em_template", "Python template")]
    ):
        frame(
            axes[n],
            label,
            "Question-average conditional EM",
            6.5,
            [0, 2, 4, 6],
            n == 0,
        )
        bars(
            axes[n],
            [lookup[m, suite]["question_macro_em_pct"] for m in METHODS],
            6.5,
        )
    save(
        fig,
        "formats",
        "Same eight questions × 100 answers for each format and model. Zero means no observed eligible misaligned answers.",
    )


def categories():
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.7))
    fig.subplots_adjust(left=0.095, right=0.96, top=0.77, bottom=0.22, wspace=0.30)
    lookup = {(row["method"], row["category"]): row for row in DATA["categories"]}
    for n, (cat, title, count) in enumerate(
        [
            ("vulnerable_user", "Vulnerable user", 14),
            ("illegal_recommendations", "Illegal advice", 4),
            ("medical_advice", "Medical advice", 7),
        ]
    ):
        frame(
            axes[n],
            title,
            f"{count} questions · conditional EM",
            24,
            [0, 10, 20],
            n == 0,
        )
        bars(
            axes[n],
            [lookup[m, cat]["question_macro_em_pct"] for m in METHODS],
            24,
        )
    save(
        fig,
        "categories",
        "Equal-question averages within three displayed categories. Overall preregistered EM uses all 48 questions across seven categories.",
    )


if __name__ == "__main__":
    outcome_summary()
    coverage()
    formats()
    categories()
    print("Wrote four SVG / PNG figure pairs to assets/.")
