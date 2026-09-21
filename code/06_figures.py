"""Build the two manuscript figures from candidate_crosswalk.csv, following
the dataviz skill: fixed-order categorical hues for corpus identity, a
    single sequential hue for magnitude, direct annotation, pre-release stamp until
--final is passed.
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT_DATA = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
OUT_FIG = os.path.join(os.path.dirname(__file__), "..", "paper", "figures")
os.makedirs(OUT_FIG, exist_ok=True)

# Reference palette (validated default, see dataviz skill references/palette.md)
CAT = {
    "blue": "#2a78d6",
    "orange": "#eb6834",
    "aqua": "#1baf7a",
}
SEQ_BLUE = {250: "#86b6ef", 350: "#5598e7", 450: "#2a78d6", 600: "#184f95"}
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
SURFACE = "#fcfcfb"

CORPUS_ORDER = ["CSF2.0", "SP800-53", "CPG1.0.1"]
CORPUS_COLOR = {"CSF2.0": CAT["blue"], "SP800-53": CAT["orange"], "CPG1.0.1": CAT["aqua"]}
TYPE_ORDER = ["No Match", "Related", "Partial", "Direct"]


def stamp_draft(ax, final):
    if not final:
        ax.text(
            0.99, 0.02, "PRE-RELEASE", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9, color="#b0302f", fontweight="bold", alpha=0.85,
        )


def fig_alignment_counts(cand, final):
    rank1 = cand[cand["rank"] == 1]
    counts = (
        rank1.groupby(["target_corpus", "tentative_alignment_type"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=TYPE_ORDER, fill_value=0)
        .reindex(CORPUS_ORDER)
    )

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    x = np.arange(len(TYPE_ORDER))
    width = 0.25
    for i, corpus in enumerate(CORPUS_ORDER):
        vals = counts.loc[corpus].values
        bars = ax.bar(
            x + (i - 1) * width, vals, width=width * 0.9,
            color=CORPUS_COLOR[corpus], label=corpus,
        )
        for b, v in zip(bars, vals):
            if v > 0:
                ax.annotate(
                    str(int(v)), (b.get_x() + b.get_width() / 2, b.get_height()),
                    ha="center", va="bottom", fontsize=8, color=TEXT_SECONDARY,
                )
    ax.set_xticks(x)
    ax.set_xticklabels(TYPE_ORDER, color=TEXT_PRIMARY)
    ax.set_ylabel("TSA statements (rank-1 candidate)", color=TEXT_PRIMARY)
    ax.set_title(
        "Tentative alignment type by target corpus\n(TF-IDF cosine similarity, rank-1 candidate per TSA statement)",
        color=TEXT_PRIMARY, fontsize=11,
    )
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#c9c8c0")
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.legend(frameon=False, labelcolor=TEXT_PRIMARY)
    fig.text(
        0.01, 0.01,
        "Sources: TSA Pipeline Security Guidelines (2018/2021); NIST CSF 2.0 (CSWP.29, 2024);\n"
        "NIST SP 800-53 Rev 5.2.0 (base-control subset); CISA CPG v1.0.1 (2023). n=130 TSA statements.",
        fontsize=7, color=TEXT_SECONDARY,
    )
    stamp_draft(ax, final)
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(os.path.join(OUT_FIG, "fig1_alignment_type_by_corpus.png"), dpi=200)
    plt.close(fig)


def fig_score_distribution(cand, final):
    rank1 = cand[cand["rank"] == 1]
    fig, axes = plt.subplots(1, 3, figsize=(11, 4), sharey=True, facecolor=SURFACE)
    thresholds = [0.08, 0.18, 0.30]
    for ax, corpus in zip(axes, CORPUS_ORDER):
        ax.set_facecolor(SURFACE)
        vals = rank1.loc[rank1["target_corpus"] == corpus, "cosine_similarity"]
        ax.hist(vals, bins=20, color=SEQ_BLUE[450], edgecolor=SURFACE)
        for t in thresholds:
            ax.axvline(t, color=TEXT_SECONDARY, linestyle="--", linewidth=0.8)
        ax.set_title(corpus, color=TEXT_PRIMARY, fontsize=10)
        ax.set_xlabel("cosine similarity", color=TEXT_SECONDARY, fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color("#c9c8c0")
        ax.tick_params(colors=TEXT_SECONDARY, labelsize=8)
    axes[0].set_ylabel("count of TSA statements", color=TEXT_PRIMARY)
    fig.suptitle(
        "Rank-1 candidate similarity score distribution by target corpus\n"
        "(dashed lines: Related / Partial / Direct thresholds, see BUILD_SPEC.md)",
        color=TEXT_PRIMARY, fontsize=11,
    )
    stamp_draft(axes[-1], final)
    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig(os.path.join(OUT_FIG, "fig2_score_distribution.png"), dpi=200)
    plt.close(fig)


def main(final):
    cand = pd.read_csv(os.path.join(OUT_DATA, "candidate_crosswalk.csv"))
    fig_alignment_counts(cand, final)
    fig_score_distribution(cand, final)
    print(f"figures written to {OUT_FIG} (final={final})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", action="store_true", help="remove pre-release stamp")
    args = parser.parse_args()
    main(args.final)
