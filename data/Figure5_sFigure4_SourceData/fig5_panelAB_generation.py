"""
Figure 5 Panels A & B for the disulfide-stapled peptide methods paper.

Panel A: Ellman's L-cysteine standard curve (8 standards + NC) with linear fit.
Panel B: Free Cys (uM) per measured unknown well + BSA positive controls,
         colored by target, with noise floor (2 uM) and failure threshold (10 uM).

Re-run with: python fig5_panelAB_generation.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress

# ---------------------------------------------------------------------------
# Paths (absolute — edit if files move)
# ---------------------------------------------------------------------------
BASE = Path(""
            "disulfide_stapled_peptides/figures_draft")
STANDARDS_CSV = BASE / "ellman_from_ada" / "standard_output.csv"
UNKNOWNS_CSV  = BASE / "ellman_from_ada" / "unknowns_output.csv"
MERGED_CSV    = BASE / "sec_ellman_merged.csv"

OUT_DIR = BASE / "svg_panels"
PANEL_A_OUT = OUT_DIR / "fig5_panelA_standard_curve.svg"
PANEL_B_OUT = OUT_DIR / "fig5_panelB_freecys_unknowns.svg"

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#dddddd",
    "grid.linewidth": 0.6,
    "axes.axisbelow": True,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
})


# ---------------------------------------------------------------------------
# Panel A — Standard curve
# ---------------------------------------------------------------------------
def make_panel_a():
    df = pd.read_csv(STANDARDS_CSV)
    # Columns: Standard, uM_Concentration, Absorbance
    x = df["uM_Concentration"].to_numpy(dtype=float)
    y = df["Absorbance"].to_numpy(dtype=float)

    # Fit linear regression on the full series (standards + NC = 0)
    fit = linregress(x, y)
    slope, intercept, r_value = fit.slope, fit.intercept, fit.rvalue
    r2 = r_value ** 2

    fig, ax = plt.subplots(figsize=(5.0, 3.5))

    # Standards (S01-S08): blue circles. NC: open marker.
    is_nc = df["Standard"].astype(str).str.upper().eq("NC")
    ax.scatter(x[~is_nc], y[~is_nc],
               s=42, color="#1f6feb", edgecolor="black",
               linewidth=0.6, zorder=3, label="L-Cys standards")
    ax.scatter(x[is_nc], y[is_nc],
               s=42, facecolor="white", edgecolor="black",
               linewidth=0.8, zorder=3, label="Buffer blank")

    # Fit line across full x range
    xfit = np.linspace(0, x.max() * 1.05, 100)
    yfit = slope * xfit + intercept
    ax.plot(xfit, yfit, color="#d62728", linewidth=1.3,
            zorder=2, label="Linear fit")

    # Equation + R^2 text box
    sign = "+" if intercept >= 0 else "-"
    eqn = (f"y = {slope:.4f}·x {sign} {abs(intercept):.3f}\n"
           f"R² = {r2:.4f}")
    ax.text(0.04, 0.96, eqn, transform=ax.transAxes,
            ha="left", va="top",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.4",
                      facecolor="white", edgecolor="#888888",
                      linewidth=0.6))

    ax.set_xlabel("[L-Cysteine] (µM)")
    ax.set_ylabel("A410")  # data column was labeled "410"
    ax.set_title("Ellman's standard curve")
    ax.set_xlim(left=-1.5)
    ax.set_ylim(bottom=0)
    ax.legend(loc="lower right", frameon=False)

    fig.tight_layout()
    fig.savefig(PANEL_A_OUT, format="svg", bbox_inches="tight")
    plt.close(fig)

    return {"slope": slope, "intercept": intercept, "r2": r2,
            "n_points": len(df)}


# ---------------------------------------------------------------------------
# Panel B — Free Cys per unknown + BSA controls
# ---------------------------------------------------------------------------
TARGET_ORDER = ["dnan", "gaba", "chip", "bcat", "mcl1", "mrka"]


def make_panel_b():
    # Read unknowns (well -> measured free Cys in uM)
    unk = pd.read_csv(UNKNOWNS_CSV)
    unk = unk.rename(columns={unk.columns[0]: "well",
                              unk.columns[1]: "free_cys_uM"})
    unk["well"] = unk["well"].astype(str)

    # BSA positive controls
    bsa = unk[unk["well"].str.upper().str.startswith("BSA")].copy()

    # Merged SEC + Ellman's: gives us per-well target labels (no sequences read)
    merged = pd.read_csv(MERGED_CSV,
                         usecols=["well", "name", "target", "ell_freecys_uM"])
    merged["well"] = merged["well"].astype(str)
    merged = merged.dropna(subset=["target"])

    # Sort within each target by free_cys ascending; group by target order
    merged["target"] = merged["target"].str.lower()
    merged = merged[merged["target"].isin(TARGET_ORDER)].copy()
    merged["target_rank"] = merged["target"].map(
        {t: i for i, t in enumerate(TARGET_ORDER)}
    )
    merged = merged.sort_values(["target_rank", "ell_freecys_uM"]).reset_index(drop=True)

    # Categorical colors from tab10
    cmap = plt.get_cmap("tab10")
    target_colors = {t: cmap(i) for i, t in enumerate(TARGET_ORDER)}

    # x positions: contiguous integers; tick labels = peptide IDs (name)
    x_pos = np.arange(len(merged))
    # BSA gets positions after the unknowns, with a small gap
    bsa_x_start = len(merged) + 1
    bsa_x = np.arange(bsa_x_start, bsa_x_start + len(bsa))

    # Use log y if BSA dominates the scale (BSA values can be > 50 uM)
    bsa_max = bsa["free_cys_uM"].max() if len(bsa) else 0
    use_log = bsa_max > 50

    fig, ax = plt.subplots(figsize=(7.5, 3.7))

    # For log scale, clip non-positive values to a small floor for plotting
    # but keep the threshold lines visible. We use 0.1 uM as display floor.
    plot_floor = 0.1
    y_plot = merged["ell_freecys_uM"].clip(lower=plot_floor if use_log else None)

    # Plot per-target so the legend has one entry per target
    for tgt in TARGET_ORDER:
        m = merged["target"] == tgt
        if not m.any():
            continue
        ax.scatter(x_pos[m.values], y_plot[m.values],
                   s=38, color=target_colors[tgt],
                   edgecolor="black", linewidth=0.4,
                   zorder=3, label=tgt)

    # BSA controls — red triangles
    if len(bsa):
        bsa_y = bsa["free_cys_uM"].clip(lower=plot_floor if use_log else None)
        ax.scatter(bsa_x, bsa_y,
                   marker="^", s=70, color="#d62728",
                   edgecolor="black", linewidth=0.5,
                   zorder=4, label="BSA (+ control)")

    # Threshold lines
    ax.axhline(2.0, color="#888888", linestyle="--", linewidth=1.0,
               zorder=1)
    ax.axhline(10.0, color="#d62728", linestyle="--", linewidth=1.0,
               zorder=1)

    # Annotate the threshold lines
    xmax = (bsa_x[-1] if len(bsa) else x_pos[-1]) + 0.5
    ax.text(xmax, 2.0, "  noise floor (2 µM)",
            va="center", ha="left", fontsize=8, color="#555555")
    ax.text(xmax, 10.0, "  failure (10 µM)",
            va="center", ha="left", fontsize=8, color="#d62728")

    # X tick labels: peptide_id (name) for unknowns; BSA labels for BSAs
    all_x = np.concatenate([x_pos, bsa_x]) if len(bsa) else x_pos
    all_labels = list(merged["name"]) + list(bsa["well"]) if len(bsa) else list(merged["name"])
    ax.set_xticks(all_x)
    ax.set_xticklabels(all_labels, rotation=45, ha="right", fontsize=7)

    if use_log:
        ax.set_yscale("log")
        ax.set_ylim(bottom=plot_floor)
    else:
        ax.set_ylim(bottom=0)

    ax.set_xlabel("peptide_id")
    ax.set_ylabel("Free Cys (µM)")
    ax.set_title("Free cysteine per peptide (Ellman's assay) + BSA controls")

    # Make room on the right for threshold annotations
    ax.set_xlim(-0.8, xmax + 4.0)

    # Legend outside the right edge so it doesn't overlap annotations
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0),
              frameon=False, title="target")

    fig.tight_layout()
    fig.savefig(PANEL_B_OUT, format="svg", bbox_inches="tight")
    plt.close(fig)

    return {
        "n_unknowns": len(merged),
        "n_bsa": len(bsa),
        "target_counts": merged["target"].value_counts().to_dict(),
        "log_y": use_log,
        "bsa_max_uM": float(bsa_max),
    }


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    info_a = make_panel_a()
    info_b = make_panel_b()
    print("Panel A:", info_a)
    print("Panel B:", info_b)
    print(f"Wrote {PANEL_A_OUT}")
    print(f"Wrote {PANEL_B_OUT}")
