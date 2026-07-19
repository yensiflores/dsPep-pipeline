"""
Merge SEC yield data with Ellman's free-Cys data, group by target,
plot per-target free Cys distribution as Fig 5 Panel C candidate.

Usage: python3 merge_sec_ellman_panelC.py

Outputs in same directory:
  - sec_ellman_merged.csv
  - fig5_panelC_freecys_by_target.png
  - fig5_panelC_freecys_vs_yield.png
"""
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
SEC = HERE / "2025-04-16_expdata_df.csv"
ELL = HERE / "ellman_from_ada" / "unknowns_output.csv"

# Load SEC data
sec_rows = list(csv.DictReader(SEC.open()))
sec_by_well = {r["Destination Well"]: r for r in sec_rows}

# Load Ellman unknowns
ell = {}
for r in csv.DictReader(ELL.open()):
    well, val = r[""], r["410"]
    if well in {"BSA1", "BSA2", "B"}:
        continue
    try:
        ell[well] = float(val)
    except ValueError:
        pass

# Merge
merged = []
for well, ell_val in ell.items():
    if well in sec_by_well:
        s = sec_by_well[well]
        target = s["Name"].split("_")[0]
        merged.append({
            "well": well,
            "name": s["Name"],
            "target": target,
            "peptide_seq": s["Peptide"],
            "sec_conc_uM": float(s["conc_uM"]),
            "tot_yield_mg": float(s["tot_yield"]),
            "ell_freecys_uM": ell_val,
            "main_peak_agg_state": int(s["main_peak_agg_state"]),
        })

print(f"Merged rows: {len(merged)} of {len(ell)} Ellman wells, {len(sec_by_well)} SEC wells")

# Save merged CSV
out_csv = HERE / "sec_ellman_merged.csv"
with out_csv.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(merged[0].keys()))
    w.writeheader()
    w.writerows(merged)
print(f"Wrote {out_csv.name}")

# Per-target counts and stats
targets = sorted({m["target"] for m in merged})
print()
print(f"{'Target':10s}  {'N':>3s}  {'med free Cys (uM)':>18s}  {'% wells > 5 uM':>15s}  {'% wells > 10 uM':>15s}")
for t in targets:
    vals = [m["ell_freecys_uM"] for m in merged if m["target"] == t]
    n = len(vals)
    med = np.median(vals)
    p5 = 100 * sum(1 for v in vals if v > 5) / n
    p10 = 100 * sum(1 for v in vals if v > 10) / n
    print(f"{t:10s}  {n:3d}  {med:18.2f}  {p5:14.0f}%  {p10:14.0f}%")

# Plot 1: Per-target strip plot of free Cys
fig, ax = plt.subplots(figsize=(10, 5))
xpos = {t: i for i, t in enumerate(targets)}
colors = plt.cm.tab10(np.linspace(0, 1, len(targets)))

for i, t in enumerate(targets):
    vals = [m["ell_freecys_uM"] for m in merged if m["target"] == t]
    jitter = np.random.RandomState(0).uniform(-0.15, 0.15, size=len(vals))
    ax.scatter(np.array([i] * len(vals)) + jitter, vals, s=60, alpha=0.7,
               edgecolor="k", linewidth=0.5, color=colors[i], zorder=3)
    # median bar
    ax.plot([i - 0.3, i + 0.3], [np.median(vals)] * 2, "k-", lw=2, zorder=2)

ax.axhline(2, ls="--", c="grey", alpha=0.6, lw=1, label="2 µM (typical noise floor)")
ax.axhline(10, ls="--", c="firebrick", alpha=0.6, lw=1, label="10 µM (failed disulfide)")
ax.set_xticks(range(len(targets)))
ax.set_xticklabels(targets, rotation=0)
ax.set_ylabel("Free Cys / µM (Ellman's, in assay well)")
ax.set_title("Free cysteine per peptide, grouped by target (n = " + str(len(merged)) + ")")
ax.set_yscale("symlog", linthresh=1)
ax.legend(loc="upper right", fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
out_png = HERE / "fig5_panelC_freecys_by_target.png"
out_svg = HERE / "fig5_panelC_freecys_by_target.svg"
plt.savefig(out_png, dpi=300)
plt.savefig(out_svg)
print(f"Wrote {out_png.name} and .svg")
plt.close()

# Plot 2: scatter free Cys vs SEC yield
fig, ax = plt.subplots(figsize=(8, 6))
for i, t in enumerate(targets):
    rows = [m for m in merged if m["target"] == t]
    x = [m["sec_conc_uM"] for m in rows]
    y = [m["ell_freecys_uM"] for m in rows]
    ax.scatter(x, y, s=70, alpha=0.75, edgecolor="k", linewidth=0.5,
               color=colors[i], label=t, zorder=3)
ax.axhline(10, ls="--", c="firebrick", alpha=0.6, lw=1)
ax.set_xlabel("SEC concentration / µM (post-pooling)")
ax.set_ylabel("Free Cys / µM (Ellman's)")
ax.set_yscale("symlog", linthresh=1)
ax.legend(loc="upper right", fontsize=9, ncol=2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_title("Disulfide formation vs expression yield, by target")
plt.tight_layout()
out_png2 = HERE / "fig5_panelC_freecys_vs_yield.png"
out_svg2 = HERE / "fig5_panelC_freecys_vs_yield.svg"
plt.savefig(out_png2, dpi=300)
plt.savefig(out_svg2)
print(f"Wrote {out_png2.name} and .svg")
plt.close()
