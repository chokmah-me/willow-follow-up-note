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
    # Page width, short enough that Typora keeps the figure on one page.
    fig = plt.figure(figsize=(6.7, 3.25), dpi=300, facecolor="white")

    fig.text(
        0.02,
        0.97,
        "Grafted-code memory fits and this note's two rules",
        ha="left",
        va="top",
        fontsize=11,
        color=BLACK,
    )

    # A. Two labeled fits. Length from zero.
    ax = fig.add_axes([0.14, 0.20, 0.32, 0.62])
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
    ax.set_yticklabels(["Simulation fit", "Experiment fit"], fontsize=8.5)
    ax.set_xticks([0, SIM, EXP])
    ax.set_xticklabels(["0", "0.8", "5.3"], fontsize=8.5)
    ax.tick_params(axis="x", length=2.6, width=0.6, colors=BLACK, pad=1.5)
    ax.tick_params(axis="y", length=0, pad=2)
    for name in ("top", "right", "left"):
        ax.spines[name].set_visible(False)
    ax.spines["bottom"].set_color(BLACK)
    ax.spines["bottom"].set_linewidth(0.6)
    ax.spines["bottom"].set_bounds(0, EXP)
    ax.set_xlabel("Logical error rate (%)", fontsize=8.5, labelpad=2, color=BLACK)
    ax.text(
        EXP - 0.12,
        1.16,
        "5.3%",
        ha="right",
        va="bottom",
        fontsize=8.5,
        color=BLACK,
        clip_on=True,
    )
    ax.text(
        SIM + 0.22,
        0.22,
        "0.8%",
        ha="left",
        va="bottom",
        fontsize=8.5,
        color=BLUE,
        clip_on=True,
    )
    fig.text(0.02, 0.82, "A", ha="left", va="center", fontsize=12, color=BLACK)

    # B. Published v1 ratio, plus the two v6 rules. Vermillion is only
    # for those rules; solid vs dashed keeps them apart in grayscale.
    bx = fig.add_axes([0.62, 0.20, 0.34, 0.62])
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
    bx.set_xticklabels(["0", "2", "3", "6", "7.1"], fontsize=8.5)
    bx.tick_params(axis="x", length=2.6, width=0.6, colors=BLACK, pad=1.5)
    bx.tick_params(axis="y", length=0)
    for name in ("top", "right", "left"):
        bx.spines[name].set_visible(False)
    bx.spines["bottom"].set_color(BLACK)
    bx.spines["bottom"].set_linewidth(0.6)
    bx.spines["bottom"].set_bounds(0, HI)
    bx.set_xlabel("Ratio of the two fit labels", fontsize=8.5, labelpad=2)
    bx.text(
        RATIO,
        range_y + cap + 0.05,
        "6.6  v1",
        ha="center",
        va="bottom",
        fontsize=8.5,
        color=BLACK,
        clip_on=True,
    )
    bx.text(
        (LO + HI) / 2.0,
        range_y - cap - 0.05,
        "6.2 to 7.1",
        ha="center",
        va="top",
        fontsize=8,
        color=INK,
        clip_on=True,
    )
    bx.text(
        CLOSE - 0.18,
        0.84,
        "close",
        ha="right",
        va="bottom",
        fontsize=8,
        color=VERMILLION,
        clip_on=True,
    )
    bx.text(
        GATE + 0.18,
        0.84,
        "arm B",
        ha="left",
        va="bottom",
        fontsize=8,
        color=VERMILLION,
        clip_on=True,
    )
    fig.text(0.50, 0.82, "B", ha="left", va="center", fontsize=12, color=BLACK)
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
