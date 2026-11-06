#!/usr/bin/env python3
"""Render the published results with the article's bundled Source Serif font."""
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
COLORS = {"Base": "#4C5563", "AdamW": "#327AA5", "Muon": "#208567"}
MODELS = (
    ("Base", "Base"),
    ("AdamW", "SFT"),
    ("Muon", "SFT"),
    ("AdamW", "SST 90%"),
    ("Muon", "SST 90%"),
)


def configure_fonts():
    for weight in (400, 600):
        font_manager.fontManager.addfont(ROOT / f"assets/fonts/source-serif-{weight}.ttf")
    family = font_manager.FontProperties(
        fname=ROOT / "assets/fonts/source-serif-400.ttf"
    ).get_name()
    plt.rcParams.update({
        "font.family": family,
        "font.size": 19,
        "axes.labelsize": 19,
        "axes.titlesize": 24,
        "axes.titleweight": 600,
        "axes.labelcolor": "#252525",
        "text.color": "#252525",
        "xtick.color": "#555555",
        "ytick.color": "#555555",
        "svg.fonttype": "path",
        "svg.hashsalt": "sst-blog-results",
    })


def style_axes(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#777777")
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(labelsize=19, width=0.8, pad=6)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#D0D0D0", linestyle=":", linewidth=0.75)


def bar_style(model):
    color = COLORS[model[0]]
    outlined = model[1] == "SFT"
    return {
        "facecolor": "white" if outlined else color,
        "edgecolor": color,
        "linewidth": 1.4 if outlined else 0.8,
        "zorder": 3,
    }


def legend(fig, base_marker=False):
    handles = []
    for model in MODELS:
        method_label = "SST" if model[1] == "SST 90%" else model[1]
        label = "Base" if model[0] == "Base" else f"{model[0]} {method_label}"
        if model[0] == "Base" and base_marker:
            handle = Line2D(
                [], [], linestyle="none", marker="^", color=COLORS["Base"],
                markersize=9, label=label,
            )
        else:
            handle = Patch(**bar_style(model), label=label)
        handles.append(handle)
    fig.legend(
        handles=handles, loc="upper center", bbox_to_anchor=(0.52, 0.99),
        ncol=5, frameon=False, fontsize=18.5, columnspacing=0.8,
        handletextpad=0.4, handlelength=1.2,
    )


def comparison(data):
    fig = plt.figure(figsize=(12, 20 / 3))
    grid = fig.add_gridspec(
        1, 2, width_ratios=[1.2, 3],
        left=0.095, right=0.99, top=0.75, bottom=0.22, wspace=0.30,
    )
    ax_id, ax_em = [fig.add_subplot(grid[0, index]) for index in range(2)]
    for ax in (ax_id, ax_em):
        style_axes(ax)
    ax_id.grid(axis="both", color="#D0D0D0", linestyle=":", linewidth=0.75)
    offsets = {
        ("Base", "Base"): (10, 6, "left", "bottom"),
        ("AdamW", "SFT"): (-10, -5, "right", "top"),
        ("Muon", "SFT"): (-10, 7, "right", "bottom"),
        ("AdamW", "SST 90%"): (-8, 8, "right", "bottom"),
        ("Muon", "SST 90%"): (-8, -8, "right", "top"),
    }
    for point in data["selected"]:
        model = (point["optimizer"], point["method"])
        x = float(point["insecure_id_gain_pp"])
        y = float(point["mmlu_pro_change_pp"])
        base, sft = model[0] == "Base", model[1] == "SFT"
        color = COLORS[model[0]]
        if not base:
            ax_id.annotate(
                "", xy=(x, y), xytext=(0, 0),
                arrowprops={
                    "arrowstyle": "->", "color": color, "linewidth": 1.1,
                    "linestyle": "--" if sft else "-", "alpha": 0.55,
                    "shrinkA": 8, "shrinkB": 12, "mutation_scale": 12,
                }, zorder=2,
            )
        ax_id.scatter(
            x, y, marker="^" if base else "o" if sft else "*",
            s=110 if base else 130 if sft else 270,
            facecolor="white" if sft else color,
            edgecolor="white" if base else color,
            linewidth=0.8 if base else 1.5, zorder=5,
        )
        dx, dy, ha, va = offsets[model]
        ax_id.annotate(
            "Base" if base else "SFT" if sft else "SST", (x, y),
            xytext=(dx, dy), textcoords="offset points",
            ha=ha, va=va, fontsize=19, color="#333333",
        )
    ax_id.axhline(0, color="#999999", linewidth=0.8, linestyle="--")
    ax_id.axvline(0, color="#999999", linewidth=0.8, linestyle="--")
    ax_id.set_xlim(-2, 28)
    ax_id.set_ylim(-8.3, 1.4)
    ax_id.set_xticks([0, 5, 10, 15, 20, 25])
    ax_id.set_yticks([-8, -6, -4, -2, 0])
    ax_id.set_xlabel("Insecure ID gain (pp)", labelpad=10)
    ax_id.set_ylabel("MMLU-Pro change (pp)", labelpad=10)
    ax_id.set_title("ID vs OOD", pad=20)

    behavior = {
        (point["optimizer"], point["method"], point["suite"]): float(point["change_from_base"])
        for point in data["behavior"]
    }
    suites = ("em_main", "em_ood", "truthfulqa_mc", "strongreject")
    for metric_index, suite in enumerate(suites):
        for model_index, model in enumerate(MODELS[1:]):
            change = behavior[model + (suite,)]
            x = metric_index + (model_index - 1.5) * 0.17
            ax_em.bar(x, change, width=0.145, **bar_style(model))
            if change == 0:
                ax_em.annotate(
                    "0", (x, 0), xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=19, color=COLORS[model[0]],
                )
    ax_em.axhline(0, color="#777777", linewidth=0.8, linestyle="--")
    ax_em.set_ylim(-0.045, 0.145)
    ax_em.set_yticks([-0.025, 0, 0.05, 0.10], ["−0.025", "0", "0.05", "0.10"])
    ax_em.set_xlim(-0.5, 3.5)
    ax_em.set_xticks(range(4), [
        "Free-form\n(main)", "Free-form\n(preregistered)",
        "TruthfulQA\n(MC1 error)", "StrongREJECT",
    ])
    ax_em.tick_params(axis="x", length=0, pad=10, labelsize=18)
    ax_em.set_ylabel("Change from base", labelpad=10)
    ax_em.set_title("EM", pad=20)
    legend(fig, base_marker=True)
    return fig


def ablation(data, category=False):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.subplots_adjust(left=0.12, right=0.985, top=0.75, bottom=0.22)
    style_axes(ax)
    groups = (
        (("vulnerable_user", "Vulnerable\nuser"), ("illegal_recommendations", "Illegal\nadvice"),
         ("medical_advice", "Medical\nadvice"))
        if category else
        (("em_json", "Answer in JSON"), ("em_template", "Python template in question"))
    )
    points = data["categories" if category else "formats"]
    lookup = {
        (point["optimizer"], point["method"], point["category" if category else "suite"]):
        float(point["question_macro_em_pct"])
        for point in points
    }
    for model_index, model in enumerate(MODELS):
        for index, (key, _) in enumerate(groups):
            value = lookup[model + (key,)]
            x = index + (model_index - 2) * 0.145
            ax.bar(x, value, width=0.12, **bar_style(model))
            if value == 0:
                ax.annotate(
                    "0", (x, 0), xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=19, color=COLORS[model[0]],
                )
    maximum = max(lookup.values())
    ceiling = max(20, math.ceil(maximum / 5) * 5) if category else max(6, math.ceil(maximum / 2) * 2)
    ax.set_ylim(0, ceiling + (1 if category else 0.3))
    ax.set_yticks(range(0, ceiling + 1, 5 if category else 1))
    ax.yaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.set_ylabel("Conditional EM (%)", labelpad=10)
    ax.set_xlim(-0.5, len(groups) - 0.5)
    ax.set_xticks(range(len(groups)), [group[1] for group in groups])
    ax.tick_params(axis="x", length=0, pad=12)
    ax.set_title("Preregistered categories" if category else "Answer format", pad=20)
    legend(fig)
    return fig


def main():
    configure_fonts()
    data = json.loads((ROOT / "data/merged-results.json").read_text())
    figures = (comparison(data), ablation(data), ablation(data, category=True))
    for number, fig in enumerate(figures, 1):
        # Outlined glyphs preserve the exact bundled font in standalone SVG images.
        svg_path = ROOT / f"assets/figure-{number}.svg"
        fig.savefig(
            svg_path, facecolor="white",
            metadata={"Date": None, "Title": f"Figure {number}: subspace tuning results"},
        )
        svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
        fig.savefig(ROOT / f"assets/figure-{number}.png", dpi=210, facecolor="white")
        plt.close(fig)
        print(f"Built figure-{number}.svg and figure-{number}.png.")


if __name__ == "__main__":
    main()
