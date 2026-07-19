"""
Build composite Figure 1 for the disulfide-stapled peptides paper.

Layout:
  Row 1 (full width):  Panel A — workflow schematic (vector SVG)
  Row 2, left:         Panel B — end-to-end timeline (vector)
  Row 2, right:        Panel C — per-design DNA cost (vector)

The final fig1_composite.svg is fully vector: panel A is the source SVG
(manuscript/SVG/Asset 1.svg), panels B and C are matplotlib SVG output,
composed together with svgutils.

A PNG preview is rendered separately by embedding workflow_figure1.jpg
as raster in the same matplotlib layout (matplotlib has no native SVG
embedding without cairosvg).

Outputs (in figures_draft/regenerated/):
  - fig1_composite.svg  (fully vector for Illustrator)
  - fig1_composite.png  (300 dpi raster preview)
  - _fig1_BC.svg        (intermediate B+C-only SVG, kept for inspection)
"""
from pathlib import Path
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import svgutils.transform as st

HERE = Path(__file__).parent
PROJECT = HERE.parent
OUT = HERE / "regenerated"
OUT.mkdir(exist_ok=True)

SCHEMATIC_SVG = PROJECT / "manuscript" / "SVG" / "Asset 1.svg"
SCHEMATIC_RASTER = PROJECT / "manuscript" / "workflow_figure1.jpg"

sns.set_theme(
    context="talk",
    style="ticks",
    rc={"axes.spines.right": False, "axes.spines.top": False},
)

DEEP_BLUE = "#0a5a82"
LIGHT_BLUE = "#7fb6d3"

PANEL_LABEL_KW = dict(fontsize=22, fontweight="bold", va="top", ha="left")


def draw_panel_label(ax, letter, x=-0.05, y=1.08):
    ax.text(x, y, letter, transform=ax.transAxes, **PANEL_LABEL_KW)


# ============================================================
# Panel B — End-to-end timeline
# ============================================================
def draw_panel_b(ax):
    stages = [
        "DNA synthesis", "Cloning + verification",
        "Expression", "Purification", "Validation",
    ]
    trad = [8 * 24, 4, 18, 36, 4]
    new_ = [2 * 24, 3, 18, 48, 4]
    stage_colors = ["#0a5a82", "#3c89a6", "#7fb6d3", "#aed4e3", "#dceaf2"]

    y_positions = [1, 0]
    labels_y = ["Traditional\n(gene fragment)", "This work\n(primer pair)"]
    data = [trad, new_]

    left = [0, 0]
    for i, stage in enumerate(stages):
        widths = [d[i] for d in data]
        ax.barh(
            y_positions, widths, left=left,
            color=stage_colors[i], edgecolor="k", linewidth=0.8,
            label=stage, height=0.55,
        )
        for j, (w, l) in enumerate(zip(widths, left)):
            if w >= 14:
                text_color = "white" if i < 2 else "black"
                label = f"{w} h" if w < 24 else f"{w/24:.0f} d"
                ax.text(
                    l + w/2, y_positions[j], label,
                    ha="center", va="center",
                    color=text_color, fontsize=9, fontweight="bold",
                )
        left = [l + w for l, w in zip(left, widths)]

    totals = [sum(trad), sum(new_)]
    for y, total in zip(y_positions, totals):
        ax.text(
            total + 8, y,
            f" {total/24:.1f} d\n(~{total/24/7:.1f} wk)",
            va="center", ha="left",
            fontsize=11, fontweight="bold",
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels_y, fontsize=10)
    ax.set_xlabel("Cumulative time (hours)", fontsize=12)
    ax.set_xlim(0, max(totals) * 1.28)
    ax.set_title("End-to-end timeline", fontsize=13, fontweight="bold", pad=10)
    ax.legend(
        loc="upper center", bbox_to_anchor=(0.5, -0.22),
        ncol=3, frameon=False, fontsize=9,
    )
    ax.grid(axis="x", linestyle=":", color="grey", alpha=0.5)
    ax.set_axisbelow(True)


# ============================================================
# Panel C — Per-design DNA cost
# ============================================================
def draw_panel_c(ax):
    cost_labels = ["Gene fragment\n(eBlock, ~300 bp)", "Primer pair\n(this work, <60 nt)"]
    costs = [21.0, 2.0]
    cost_colors = [DEEP_BLUE, LIGHT_BLUE]

    bars = ax.bar(
        range(len(cost_labels)), costs, color=cost_colors,
        edgecolor="k", linewidth=1.2, width=0.55,
    )
    for bar, val in zip(bars, costs):
        ax.text(
            bar.get_x() + bar.get_width()/2, val + 0.6,
            f"${val:.0f}", ha="center", va="bottom",
            fontsize=15, fontweight="bold",
        )

    ax.annotate(
        "", xy=(1, 2.5), xytext=(0, 21),
        arrowprops=dict(
            arrowstyle="->", color="firebrick", lw=2,
            connectionstyle="arc3,rad=-0.2",
        ),
    )
    ax.text(
        0.5, 13, "≈ 10× lower\nDNA cost",
        ha="center", va="center", fontsize=12,
        color="firebrick", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="firebrick", lw=1.2),
    )

    ax.set_ylabel("Cost per design (USD)", fontsize=12)
    ax.set_title("DNA cost", fontsize=13, fontweight="bold", pad=10)
    ax.set_ylim(0, 26)
    ax.set_xticks(range(len(cost_labels)))
    ax.set_xticklabels(cost_labels, fontsize=10)
    ax.tick_params(axis="x", length=0)


# ============================================================
# B+C-only matplotlib figure → intermediate SVG for SVG composition
# ============================================================
fig_bc = plt.figure(figsize=(14, 5))
gs_bc = GridSpec(nrows=1, ncols=2, wspace=0.25, figure=fig_bc)
ax_b = fig_bc.add_subplot(gs_bc[0, 0])
draw_panel_b(ax_b)
draw_panel_label(ax_b, "B")
ax_c = fig_bc.add_subplot(gs_bc[0, 1])
draw_panel_c(ax_c)
draw_panel_label(ax_c, "C")
fig_bc.tight_layout()
bc_svg_path = OUT / "_fig1_BC.svg"
fig_bc.savefig(bc_svg_path, bbox_inches="tight")
plt.close(fig_bc)

# ============================================================
# Full A+B+C raster preview (PNG only)
# ============================================================
fig_full = plt.figure(figsize=(14, 12))
gs_full = GridSpec(
    nrows=2, ncols=2,
    height_ratios=[1.4, 1],
    hspace=0.35, wspace=0.25,
    figure=fig_full,
)
ax_a = fig_full.add_subplot(gs_full[0, :])
ax_a.imshow(mpimg.imread(SCHEMATIC_RASTER))
ax_a.axis("off")
draw_panel_label(ax_a, "A", x=-0.01, y=1.02)
ax_b2 = fig_full.add_subplot(gs_full[1, 0])
draw_panel_b(ax_b2)
draw_panel_label(ax_b2, "B")
ax_c2 = fig_full.add_subplot(gs_full[1, 1])
draw_panel_c(ax_c2)
draw_panel_label(ax_c2, "C")
fig_full.text(
    0.99, 0.01,
    "Sources: Asset 1.svg; ds_pep_results.pptx slides 2–3; manuscript Methods §1.",
    ha="right", va="bottom", fontsize=8, color="grey", style="italic",
)
out_png = OUT / "fig1_composite.png"
fig_full.savefig(out_png, dpi=300, bbox_inches="tight")
plt.close(fig_full)

# ============================================================
# Compose all-vector SVG: schematic SVG (top) + B+C SVG (bottom)
# ============================================================
schem = st.fromfile(str(SCHEMATIC_SVG))
schem_root = schem.getroot()
# viewBox is "0 0 429 240" → native units 429 × 240
SCHEM_W, SCHEM_H = 429.0, 240.0

bc = st.fromfile(str(bc_svg_path))
bc_w_raw, bc_h_raw = bc.get_size()
# Strip pt/px units if present
def _to_float(v):
    return float("".join(c for c in str(v) if c.isdigit() or c == "."))
bc_w, bc_h = _to_float(bc_w_raw), _to_float(bc_h_raw)
bc_root = bc.getroot()

# Target final width: scale schematic up to 1000 units; scale BC to match
TARGET_W = 1000.0
schem_scale = TARGET_W / SCHEM_W
schem_scaled_h = SCHEM_H * schem_scale
schem_root.moveto(0, 0, scale_x=schem_scale)

bc_scale = TARGET_W / bc_w
bc_scaled_h = bc_h * bc_scale
bc_root.moveto(0, schem_scaled_h + 30, scale_x=bc_scale)

final_h = schem_scaled_h + 30 + bc_scaled_h
out_svg = st.SVGFigure(f"{TARGET_W}", f"{final_h}")
out_svg.append([schem_root, bc_root])

# Set width/height attributes on root element so renderers display it
out_svg.root.set("width", f"{TARGET_W}")
out_svg.root.set("height", f"{final_h}")
out_svg.root.set("viewBox", f"0 0 {TARGET_W} {final_h}")

out_svg_path = OUT / "fig1_composite.svg"
out_svg.save(str(out_svg_path))

print(f"Wrote {out_png}")
print(f"Wrote {out_svg_path}")
print(f"Wrote {bc_svg_path}")
