"""
Figure 2 panels D and E generation for dsPep methods paper.

Data layout assumptions for Panel D (transformation OD600 heatmap):
- Source: cloning/dsPep_Trasnform_optimisation.xlsx, Sheet1.
- Column B ("600 nm Abs.") holds 96 OD600 readings (one per well A1..H12) in
  row-major order (A1..A12, B1..B12, ..., H1..H12).
- The four optimisation conditions (strain x volume) are arranged as
  row-pairs of the 96-well plate (2 rows x 12 columns = 24 wells / condition):
      Rows A-B : BL21,           25 uL transformation
      Rows C-D : Rosetta-Gami,   25 uL
      Rows E-F : BL21,           50 uL
      Rows G-H : Rosetta-Gami,   50 uL
  This ordering matches (i) the file names of the source gels
  (2024-02-09-1_Transformation_BL21vsRosettaGami_25ul / _50ul.tif) and
  (ii) the observed OD pattern (Rosetta-Gami consistently lower than BL21).
- The 24 wells of each condition are flattened in row-major order
  (row1-col1..col12 then row2-col1..col12) to give the 24-column x-axis.

Panel E (cPCR + Sanger pass rates):
- cPCR pass rates: 75, 92, 58, 50 % for the four conditions in the same
  order as Panel D.
- Sanger pass rates: 75 % and 83 % for the two BL21 conditions
  (per slide 18 footnote). Other two shown as n.d.
"""

from pathlib import Path
import os
import openpyxl
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
})

# Allow override (e.g. for running in a containerised workspace where the
# Mac path is mounted elsewhere). On Yensi's machine the default Mac path is
# used; in the Cowork Linux mount, set DSPEP_ROOT to the mounted path.
ROOT = Path(os.environ.get(
    "DSPEP_ROOT",
    "/Users/yensifb/Desktop/ProteinDesign/IPD/bhardwaj_lab/"
    "disulfide_stapled_peptides",
))
XLSX = ROOT / "cloning" / "dsPep_Trasnform_optimisation.xlsx"
OUT_DIR = ROOT / "figures_draft" / "svg_panels"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CONDITIONS = [
    ("BL21, 25 uL",          ["A", "B"]),
    ("Rosetta-Gami, 25 uL",  ["C", "D"]),
    ("BL21, 50 uL",          ["E", "F"]),
    ("Rosetta-Gami, 50 uL",  ["G", "H"]),
]

# ---------------------------------------------------------------------------
# Panel D : OD600 heatmap
# ---------------------------------------------------------------------------
def load_od600():
    """Return dict {well_id (e.g. 'A1') -> OD600 float} from column C."""
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb["Sheet1"]
    od = {}
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
        well = row[1]
        val = row[2]
        if well is None or val is None:
            continue
        well = str(well).strip()
        # well IDs of interest look like "A1".."H12"
        if (len(well) >= 2 and well[0] in "ABCDEFGH"
                and well[1:].isdigit() and 1 <= int(well[1:]) <= 12):
            try:
                od[well] = float(val)
            except (TypeError, ValueError):
                continue
    return od


def build_heatmap_matrix(od):
    """Return 4x24 matrix of OD600 in condition order."""
    M = np.full((len(CONDITIONS), 24), np.nan)
    for i, (_, rows) in enumerate(CONDITIONS):
        vals = []
        for r in rows:
            for c in range(1, 13):
                vals.append(od.get(f"{r}{c}", np.nan))
        M[i, :] = vals
    return M


def plot_panel_D():
    od = load_od600()
    M = build_heatmap_matrix(od)

    fig, ax = plt.subplots(figsize=(4.5, 2.6))
    im = ax.imshow(M, aspect="auto", cmap="viridis", vmin=0,
                   vmax=np.nanmax(M))
    ax.set_xticks(np.arange(24))
    ax.set_xticklabels([str(i + 1) for i in range(24)], fontsize=7)
    ax.set_yticks(np.arange(len(CONDITIONS)))
    ax.set_yticklabels([c[0] for c in CONDITIONS])
    ax.set_xlabel("Well number")
    ax.set_ylabel("Condition")
    ax.set_title("Transformation efficiency (OD600)")
    # subtle white gridlines between cells
    ax.set_xticks(np.arange(-0.5, 24, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(CONDITIONS), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.4)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(which="major", length=3)

    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("OD600", rotation=90, labelpad=6)
    cbar.outline.set_visible(False)

    out = OUT_DIR / "fig2_panelD_transformation.svg"
    plt.savefig(out, format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")
    print(f"  Median OD600 per condition:")
    for i, (lab, _) in enumerate(CONDITIONS):
        print(f"    {lab:25s}  median={np.nanmedian(M[i]):.3f}  "
              f"n_wells={np.sum(~np.isnan(M[i]))}")


# ---------------------------------------------------------------------------
# Panel E : grouped bar chart of cPCR + Sanger pass rates
# ---------------------------------------------------------------------------
def plot_panel_E():
    labels = [c[0] for c in CONDITIONS]
    cpcr  = [75, 92, 58, 50]
    # Sanger only for the two BL21 conditions (per slide 18); use NaN for n.d.
    sanger = [75, np.nan, 83, np.nan]

    x = np.arange(len(labels))
    bw = 0.36

    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    b1 = ax.bar(x - bw / 2, cpcr, bw, label="cPCR",
                color="#3a6ea5", edgecolor="black", linewidth=0.5)
    # bars for sanger - skip NaN
    s_vals = [v if not np.isnan(v) else 0 for v in sanger]
    b2 = ax.bar(x + bw / 2, s_vals, bw, label="Sanger",
                color="#d97a3e", edgecolor="black", linewidth=0.5)

    # write n.d. above the position where sanger is missing
    for xi, v in zip(x, sanger):
        if np.isnan(v):
            ax.text(xi + bw / 2, 2, "n.d.", ha="center", va="bottom",
                    fontsize=7, color="#555")

    # value labels above each bar
    for rect, v in zip(b1, cpcr):
        ax.text(rect.get_x() + rect.get_width() / 2, v + 1.5, f"{v}",
                ha="center", va="bottom", fontsize=7)
    for rect, v in zip(b2, sanger):
        if not np.isnan(v):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 1.5, f"{v}",
                    ha="center", va="bottom", fontsize=7)

    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("Pass rate (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_title("Colony PCR and Sanger pass rates")
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5,
                  color="#bbb", alpha=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper right")

    out = OUT_DIR / "fig2_panelE_passrates.svg"
    plt.savefig(out, format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    plot_panel_D()
    plot_panel_E()
