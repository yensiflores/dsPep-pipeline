#!/usr/bin/env python3
"""
Regenerate Figure 6 (SPR sensorgrams) from the deposited source data.

Reads the tab-delimited single-cycle-kinetics exports in
    data/Figure6_SourceData/
(one file per panel; columns Measured_X, Measured_Y, Fitted_X, Fitted_Y)
and reproduces the three-row Figure 6 layout:

  Row A  Target 5, design 1   : SUMO-tagged | peptide-only | linear control
  Row B  Target 3, design 1   : SUMO-tagged | peptide-only
  Row C  Target 3, design 2   : SUMO-tagged | peptide-only  (matched non-binder)

Measured traces are drawn in grey (dashed), the global 1:1 fit in black.
K_d annotations reproduce the values reported in the manuscript; panels with
no measurable binding are labelled "No detectable binding".

Usage
-----
    python regenerate_figure6_SPR.py            # uses ../../data/Figure6_SourceData
    python regenerate_figure6_SPR.py <data_dir> # or point at the data folder

Outputs Figure6_SPR.png (300 dpi) and Figure6_SPR.svg next to this script.
"""
from pathlib import Path
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec

mpl.rcParams["svg.fonttype"] = "none"  # keep text as text in the SVG

# ---- locate the source data (relative default, or first CLI argument) --------
HERE = Path(__file__).resolve().parent
DEFAULT_DATA = HERE.parent.parent / "data" / "Figure6_SourceData"
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DATA
OUT = HERE

# ---- panel definitions: file stem -> K_d annotation --------------------------
# Anonymised codes only: T{target}-D{design}; "-sumo" = His6-SUMO construct,
# bare = peptide-only, "-linear" = unconstrained linear control.
PANELS = {
    "T5-D1-sumo":   "K$_d$ = 16.3 µM",
    "T5-D1":        "K$_d$ = 55 µM",
    "T5-D1-linear": "No detectable\nbinding",
    "T3-D1-sumo":   "K$_d$ = 15.5 µM",
    "T3-D1":        "K$_d$ = 0.88 µM",
    "T3-D2-sumo":   "No detectable\nbinding",
    "T3-D2":        "No detectable\nbinding",
}

MEASURED = "#8C8C8C"   # grey, dashed
FIT = "black"          # global 1:1 fit
LW = 1.5               # shared line weight (measured == fit, per final figure)


def load(stem):
    """Return (measured_x, measured_y, fit_x, fit_y) from a source file."""
    mx, my, fx, fy = [], [], [], []
    with open(DATA / f"{stem}.txt", encoding="utf-8-sig") as fh:
        next(fh)  # header row (run/channel/flow-cell/cycle + conc series)
        for ln in fh:
            p = ln.rstrip("\n").split("\t")

            def g(i):
                try:
                    return float(p[i])
                except (IndexError, ValueError):
                    return None

            a, b, c, d = g(0), g(1), g(2), g(3)
            if a is not None and b is not None:
                mx.append(a); my.append(b)
            if c is not None and d is not None:
                fx.append(c); fy.append(d)
    return map(np.asarray, (mx, my, fx, fy))


def ylim_trimmed(*ys):
    """Y-limits that trim the negative baseline noise (1st/99.5th percentile)."""
    allv = np.concatenate([y for y in ys if y.size])
    lo, hi = np.percentile(allv, 0.5), np.percentile(allv, 99.5)
    pad = 0.08 * (hi - lo if hi > lo else 1.0)
    return lo - pad, hi + pad


def draw(ax, stem, show_ylabel):
    mx, my, fx, fy = load(stem)
    has_fit = fy.size and np.nanmax(np.abs(fy)) > 1e-6
    ax.plot(mx, my, color=MEASURED, lw=LW, ls="--", zorder=2,
            label="Measured", solid_capstyle="round")
    if has_fit:
        ax.plot(fx, fy, color=FIT, lw=LW, zorder=3, label="Global 1:1 fit")
    ax.set_title(stem, loc="left", fontweight="bold", fontsize=14, pad=6)
    lab = PANELS[stem]
    ax.text(0.03, 0.94, lab, transform=ax.transAxes, ha="left", va="top",
            fontsize=13, fontweight="bold" if "K$" in lab else "normal")
    ax.set_xlabel("Time (s)", fontsize=13)
    if show_ylabel:
        ax.set_ylabel("Relative response (RU)", fontsize=13)
    ax.set_ylim(*ylim_trimmed(my, fy if has_fit else my))
    ax.grid(True, color="#DDDDDD", lw=0.8)
    ax.set_facecolor("white")
    for s in ax.spines.values():
        s.set_edgecolor("#BBBBBB")
    ax.tick_params(labelsize=10)


def main():
    if not DATA.is_dir():
        sys.exit(f"Source data folder not found: {DATA}")
    plt.rcParams.update({"font.size": 13, "figure.facecolor": "white"})
    fig = plt.figure(figsize=(13, 11.3))
    gs = gridspec.GridSpec(3, 6, height_ratios=[1, 1.18, 1.18],
                           hspace=0.42, wspace=0.34, figure=fig)
    rows = [
        ("A", ["T5-D1-sumo", "T5-D1", "T5-D1-linear"], [(0, 2), (2, 4), (4, 6)]),
        ("B", ["T3-D1-sumo", "T3-D1"],                 [(0, 3), (3, 6)]),
        ("C", ["T3-D2-sumo", "T3-D2"],                 [(0, 3), (3, 6)]),
    ]
    handles = labels = None
    for r, (letter, stems, spans) in enumerate(rows):
        first_ax = None
        for i, (stem, (c0, c1)) in enumerate(zip(stems, spans)):
            ax = fig.add_subplot(gs[r, c0:c1])
            draw(ax, stem, show_ylabel=(i == 0))
            if first_ax is None:
                first_ax = ax
                if handles is None:
                    handles, labels = ax.get_legend_handles_labels()
        first_ax.text(-0.22, 1.14, f"{letter}.", transform=first_ax.transAxes,
                      fontsize=20, fontweight="bold", va="bottom", ha="left")

    # one shared legend for all panels
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=True,
               fontsize=12, bbox_to_anchor=(0.5, 0.005))
    fig.subplots_adjust(bottom=0.07)

    fig.savefig(OUT / "Figure6_SPR.png", dpi=300, bbox_inches="tight",
                facecolor="white")
    fig.savefig(OUT / "Figure6_SPR.svg", bbox_inches="tight", facecolor="white")
    print(f"Wrote {OUT/'Figure6_SPR.png'} and {OUT/'Figure6_SPR.svg'}")


if __name__ == "__main__":
    main()
