"""
Build Fig 1 Panel C: cost + time benchmark vs traditional pipeline.

Two sub-panels side by side:
  Left  (C-i):  per-design DNA cost (gene fragment vs primer pair)
  Right (C-ii): time per stage (traditional 2-wk vs this work ~1-1.5 wk)

All numbers from slides 2-3 of slides_results/ds_pep_results.pptx and
manuscript/manuscript_draft_19042026.docx.

Outputs:
  - figures_draft/regenerated/fig1_panelC_cost_time.svg  (Illustrator-editable)
  - figures_draft/regenerated/fig1_panelC_cost_time.png  (preview)
"""
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

HERE = Path(__file__).parent
OUT = HERE / "regenerated"
OUT.mkdir(exist_ok=True)

sns.set_theme(
    context="talk",
    style="ticks",
    rc={"axes.spines.right": False, "axes.spines.top": False},
)

# -------- Color palette to harmonise with existing Figure1_timeline.ai blues --------
DEEP_BLUE = "#0a5a82"     # traditional/comparator
LIGHT_BLUE = "#7fb6d3"    # this work
GREY = "#888888"

# ============================================================
# Sub-panel C-i — Per-design DNA cost
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 5),
                          gridspec_kw={"width_ratios": [1, 1.6]})

ax = axes[0]
labels = ["Gene fragment\n(eBlock, ~300 bp)", "Primer pair\n(this work, <60 nt)"]
costs = [21.0, 2.0]  # USD per design
colors = [DEEP_BLUE, LIGHT_BLUE]

bars = ax.bar(labels, costs, color=colors, edgecolor="k", linewidth=1.2, width=0.55)
for bar, val in zip(bars, costs):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.6,
            f"${val:.0f}", ha="center", va="bottom",
            fontsize=16, fontweight="bold")

# Annotate fold reduction
ax.annotate("", xy=(1, 2.5), xytext=(0, 21),
            arrowprops=dict(arrowstyle="->", color="firebrick", lw=2,
                             connectionstyle="arc3,rad=-0.2"))
ax.text(0.5, 13, "≈ 10× lower\nDNA cost",
        ha="center", va="center", fontsize=14,
        color="firebrick", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="firebrick", lw=1.2))

ax.set_ylabel("Cost per design (USD)", fontsize=14)
ax.set_title("DNA cost", fontsize=14, fontweight="bold", pad=10)
ax.set_ylim(0, 26)
ax.set_xticklabels(labels, fontsize=11)
ax.tick_params(axis="x", length=0)

# ============================================================
# Sub-panel C-ii — Time per stage (stacked horizontal bars)
# ============================================================
ax = axes[1]

# Time per stage in HOURS (then we display by stage; total label in days)
# Traditional: synthesis dominates due to gene-fragment turnaround
stages = ["DNA synthesis", "Cloning + verification",
          "Expression", "Purification", "Validation"]
trad   = [8 * 24, 4, 18, 36, 4]   # hours
new_   = [2 * 24, 3,  18, 48, 4]   # hours
# Totals (h):  trad = 254 h ≈ 10.6 d ; new = 121 h ≈ 5.0 d

# Stage colors — sequential blues + neutrals so steps are distinguishable
stage_colors = ["#0a5a82", "#3c89a6", "#7fb6d3", "#aed4e3", "#dceaf2"]

# Plot stacked horizontal bars
y_positions = [1, 0]
labels_y = ["Traditional\n(gene fragment\npipeline)", "This work\n(primer pair\npipeline)"]
data = [trad, new_]

left = [0, 0]
for i, stage in enumerate(stages):
    widths = [d[i] for d in data]
    bars = ax.barh(y_positions, widths, left=left,
                    color=stage_colors[i], edgecolor="k", linewidth=0.8,
                    label=stage, height=0.55)
    # Inline stage labels for the bigger segments
    for j, (w, l) in enumerate(zip(widths, left)):
        if w >= 14:  # only label segments >= 14 h
            text_color = "white" if i < 2 else "black"
            ax.text(l + w/2, y_positions[j], f"{w} h" if w < 24 else f"{w/24:.0f} d",
                     ha="center", va="center",
                     color=text_color, fontsize=10, fontweight="bold")
    left = [l + w for l, w in zip(left, widths)]

# Total annotations at end of each bar
totals = [sum(trad), sum(new_)]
for y, total in zip(y_positions, totals):
    ax.text(total + 8, y, f" {total/24:.1f} days\n(~{total/24/7:.1f} weeks)",
            va="center", ha="left", fontsize=12, fontweight="bold")

ax.set_yticks(y_positions)
ax.set_yticklabels(labels_y, fontsize=11)
ax.set_xlabel("Cumulative time (hours)", fontsize=13)
ax.set_xlim(0, max(totals) * 1.25)
ax.set_title("End-to-end timeline", fontsize=14, fontweight="bold", pad=10)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18),
          ncol=5, frameon=False, fontsize=10)

# Light gridlines on time axis
ax.grid(axis="x", linestyle=":", color="grey", alpha=0.5)
ax.set_axisbelow(True)

# Bottom note
fig.text(0.99, 0.02,
         "Sources: slide deck slides 2–3 of ds_pep_results.pptx; manuscript Methods §1.",
         ha="right", va="bottom", fontsize=8, color="grey", style="italic")

plt.tight_layout(rect=[0, 0.04, 1, 0.96])
out_png = OUT / "fig1_panelC_cost_time.png"
out_svg = OUT / "fig1_panelC_cost_time.svg"
plt.savefig(out_png, dpi=300, bbox_inches="tight")
plt.savefig(out_svg, bbox_inches="tight")
print(f"Wrote {out_png.name} and .svg")
plt.close()
