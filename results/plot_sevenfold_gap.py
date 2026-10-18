"""Figure: grafted-code memory fit labels and the v6 rules.

The two percents are the Fig. S22 labels as stated in
draft/follow-up-note-draft-v6.md, Section V. The rounding span
6.2 to 7.1 is that section's arithmetic on the one-significant-figure
0.8%. The lines at 2 and 3 are Section IV rule 3, fixed before any
rerun. No arm outcome is plotted.
"""

from pathlib import Path

import matplotlib.pyplot as plt

BLACK = "#000000"
BLUE = "#0072B2"
VERMILLION = "#D55E00"
INK = "#222222"

EXP = 5.3
SIM = 0.8
RATIO = EXP / SIM  # 6.625; labeled 6.6
LO, HI = 6.2, 7.1
CLOSE = 2.0
GATE = 3.0

OUT_DIR = Path(__file__).resolve().parent


def build() -> plt.Figure:
    # Single-column print width. Point sizes are the print sizes.
    fig = plt.figure(figsize=(3.42, 6.35), dpi=300, facecolor="white")

    fig.text(
        0.08,
        0.988,
        "Grafted-code memory fits\nand this note's two rules",
        ha="left",
        va="top",
        fontsize=9,
        color=BLACK,
        linespacing=1.15,
    )

    # A. Two labeled fits. Length from zero.
    ax = fig.add_axes([0.40, 0.72, 0.52, 0.155])
    ax.plot([0, EXP], [1, 1], color=BLACK, lw=1.15, solid_capstyle="butt", zorder=2)
    ax.plot(
        [0, SIM],
        [0, 0],
        color=BLUE,
        lw=1.15,
        ls=(0, (2.2, 1.6)),
        solid_capstyle="butt",
        zorder=2,
    )
    ax.plot([EXP], [1], "o", ms=4.6, color=BLACK, zorder=3)
    ax.plot(
        [SIM],
        [0],
        "o",
        ms=4.6,
        markerfacecolor="white",
        markeredgecolor=BLUE,
        markeredgewidth=1.15,
        zorder=3,
    )
    ax.set_xlim(-0.15, 6.15)
    ax.set_ylim(-0.62, 1.55)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Simulation fit", "Experiment fit"], fontsize=7.5)
    ax.set_xticks([0, SIM, EXP])
    ax.set_xticklabels(["0", "0.8", "5.3"], fontsize=7.5)
    ax.tick_params(axis="x", length=2.6, width=0.6, colors=BLACK, pad=1.5)
    ax.tick_params(axis="y", length=0, pad=2)
    for name in ("top", "right", "left"):
        ax.spines[name].set_visible(False)
    ax.spines["bottom"].set_color(BLACK)
    ax.spines["bottom"].set_linewidth(0.6)
    ax.spines["bottom"].set_bounds(0, EXP)
    ax.set_xlabel("Logical error rate (%)", fontsize=7.5, labelpad=2, color=BLACK)
    ax.text(
        EXP - 0.12,
        1.16,
        "5.3%",
        ha="right",
        va="bottom",
        fontsize=7.5,
        color=BLACK,
        clip_on=True,
    )
    ax.text(
        SIM + 0.22,
        0.22,
        "0.8%",
        ha="left",
        va="bottom",
        fontsize=7.5,
        color=BLUE,
        clip_on=True,
    )
    fig.text(0.08, 0.80, "A", ha="left", va="center", fontsize=9, color=BLACK)

    # B. Published v1 ratio, plus the two v6 rules. Vermillion is only
    # for those rules; solid vs dashed keeps them apart in grayscale.
    bx = fig.add_axes([0.40, 0.42, 0.52, 0.20])
    range_y = 0.46
    cap = 0.10
    bx.plot(
        [LO, HI],
        [range_y, range_y],
        color="#4D4D4D",
        lw=1.15,
        solid_capstyle="butt",
        zorder=2,
    )
    bx.plot(
        [LO, LO],
        [range_y - cap, range_y + cap],
        color="#4D4D4D",
        lw=1.15,
        solid_capstyle="butt",
        zorder=2,
    )
    bx.plot(
        [HI, HI],
        [range_y - cap, range_y + cap],
        color="#4D4D4D",
        lw=1.15,
        solid_capstyle="butt",
        zorder=2,
    )
    bx.plot([RATIO], [range_y], marker="D", ms=4.8, color=BLACK, zorder=3)
    bx.plot(
        [CLOSE, CLOSE],
        [0.16, 0.78],
        color=VERMILLION,
        lw=1.15,
        solid_capstyle="butt",
        zorder=2,
    )
    bx.plot(
        [GATE, GATE],
        [0.16, 0.78],
        color=VERMILLION,
        lw=1.15,
        ls=(0, (2.4, 1.5)),
        solid_capstyle="butt",
        zorder=2,
    )
    bx.set_xlim(-0.25, 8.55)
    bx.set_ylim(0.0, 1.15)
    bx.set_yticks([])
    bx.set_xticks([0, CLOSE, GATE, 6, HI])
    bx.set_xticklabels(["0", "2", "3", "6", "7.1"], fontsize=7.5)
    bx.tick_params(axis="x", length=2.6, width=0.6, colors=BLACK, pad=1.5)
    bx.tick_params(axis="y", length=0)
    for name in ("top", "right", "left"):
        bx.spines[name].set_visible(False)
    bx.spines["bottom"].set_color(BLACK)
    bx.spines["bottom"].set_linewidth(0.6)
    bx.spines["bottom"].set_bounds(0, HI)
    bx.set_xlabel("Ratio of the two fit labels", fontsize=7.5, labelpad=2)
    bx.text(
        RATIO,
        range_y + cap + 0.05,
        "6.6  v1",
        ha="center",
        va="bottom",
        fontsize=7.5,
        color=BLACK,
        clip_on=True,
    )
    bx.text(
        (LO + HI) / 2.0,
        range_y - cap - 0.05,
        "6.2 to 7.1",
        ha="center",
        va="top",
        fontsize=7,
        color=INK,
        clip_on=True,
    )
    bx.text(
        CLOSE - 0.18,
        0.84,
        "close",
        ha="right",
        va="bottom",
        fontsize=7,
        color=VERMILLION,
        clip_on=True,
    )
    bx.text(
        GATE + 0.18,
        0.84,
        "arm B",
        ha="left",
        va="bottom",
        fontsize=7,
        color=VERMILLION,
        clip_on=True,
    )
    fig.text(0.08, 0.52, "B", ha="left", va="center", fontsize=9, color=BLACK)

    footer = (
        "A is the two exponential-fit labels on Fig. S22\n"
        "of the v1 supplement. Length is the percent,\n"
        "from zero. That caption does not say per cycle.\n"
        "B is 5.3/0.8 = 6.6. The capped bar is only the\n"
        "rounding span of the one-significant-figure 0.8%\n"
        "(6.2 to 7.1). It is the published v1 ratio.\n"
        "The rerun is read against same-run baseline B,\n"
        "which need not equal 6.6.\n"
        "Solid line at 2: an arm is closed when its upper\n"
        "95% bound is below 2. Dashed line at 3: the run\n"
        "counts only if B's lower 95% bound exceeds 3.\n"
        "Both lines are rules set before any rerun.\n"
        "No 2 by 2 arm has been run. A ratio of 1 is not\n"
        "the target. This is not the factor-of-about-40\n"
        "state-error comparison."
    )
    fig.text(
        0.08,
        0.016,
        footer,
        ha="left",
        va="bottom",
        fontsize=6.6,
        color=INK,
        linespacing=1.22,
    )
    return fig


def main() -> None:
    fig = build()
    png = OUT_DIR / "fig_sevenfold_gap.png"
    pdf = OUT_DIR / "fig_sevenfold_gap.pdf"
    # Fixed bbox. Tight cropping has erased reserved bands before.
    fig.savefig(png, dpi=300, facecolor="white")
    fig.savefig(pdf, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
