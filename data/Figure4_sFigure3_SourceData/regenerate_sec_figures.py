"""
Regenerate Figs 4A/B/C/D from the saved SEC analysis HDF5,
using only the 60 successfully-pooled wells (the 36 flat ones
were already excluded when the original notebook saved the HDF5).

Outputs to: figures_draft/regenerated/

Plot logic mirrors cells 21, 22, 24 of:
  /projects/yfloresbueso/data_from_ipd/yensifb_oct2025/home/yensifb/software/ds_expression/4_sec_dslf_yfb001.ipynb
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
import fastcluster
from scipy.cluster import hierarchy

HERE = Path(__file__).parent
OUT = HERE / "regenerated"
OUT.mkdir(exist_ok=True)
H5 = HERE / "2025-04-16_expdata_df.h5"

sns.set_theme(
    context="talk",
    palette="colorblind",
    style="ticks",
    rc={"axes.spines.right": False, "axes.spines.top": False},
)

df = pd.read_hdf(H5, key="df")
df["target"] = df["Name"].str.split("_").str[0]
df = df.reset_index(drop=True)
N = len(df)
print(f"Loaded {N} wells, {df['target'].nunique()} targets")

# =============================================================
# Fig 4A — stacked SEC chromatograms (mirrors notebook cell 21)
# =============================================================
vol_light = np.vstack([np.asarray(v) for v in df["vol_light"].to_numpy()])
Abs_light = np.vstack([np.asarray(v) for v in df["Abs_light"].to_numpy()])
Abs_norm_light = np.vstack(df["Abs_norm_light"].to_numpy())

# Cluster on the normalized traces so peak shape (not magnitude) drives ordering
linkage = fastcluster.linkage(Abs_norm_light, method="average")
clustered_idx = hierarchy.dendrogram(linkage, no_plot=True)["leaves"]

delta = np.max([np.max(x) for x in df["Abs"].to_numpy()]) / 20
fig, ax = plt.subplots(ncols=2, figsize=(11, 5.5))

for i, r in df.iterrows():
    ax[0].plot(r["vol"], r["Abs"], color="C0", alpha=0.15)

for plot_i, src_i in enumerate(clustered_idx):
    ax[1].fill_between(
        x=vol_light[src_i],
        y1=Abs_light[src_i] + plot_i * delta,
        y2=plot_i * delta,
        color="C0",
        alpha=0.12,
        zorder=plot_i,
    )

ax[0].set(xlabel="Retention vol. / mL", ylabel="A280 / mAU")
ax[1].set(xlabel="Retention vol. / mL", yticks=[])
ax[1].spines["left"].set_visible(False)
ax[0].set_title(f"$N = {N}$ (flat wells excluded)")
plt.tight_layout()
plt.savefig(OUT / "fig4A_sec_traces_filtered.png", dpi=300)
plt.savefig(OUT / "fig4A_sec_traces_filtered.svg")
plt.close()
print("✓ fig4A_sec_traces_filtered.png")

# =============================================================
# Fig 4B — yield histogram (mirrors notebook cell 22)
# =============================================================
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.histplot(
    data=df,
    x="tot_yield",
    stat="count",
    ax=ax,
    log_scale=True,
    element="step",
    alpha=0.15,
)

ax2 = ax.twinx()
sns.ecdfplot(data=df, x="tot_yield", alpha=0.7, ax=ax2)
median = df["tot_yield"].median()
ax2.vlines(median, 0, 0.5, color="salmon", lw=2)
ax2.scatter([median], [0.5], color="salmon", zorder=10)

ax.spines["right"].set_visible(True)
ax.set_xlabel("Total soluble yield / mg")
ax.set_title(f"Median = {median:.3f} mg  ($N = {N}$)")
ax2.set_ylabel("Cumulative proportion")
plt.tight_layout()
plt.savefig(OUT / "fig4B_yield_histogram_filtered.png", dpi=300)
plt.savefig(OUT / "fig4B_yield_histogram_filtered.svg")
plt.close()
print("✓ fig4B_yield_histogram_filtered.png")

# =============================================================
# Fig 4C — per-target yield boxplot + swarm (NEW)
# =============================================================
order = (
    df.groupby("target")["conc_uM"].median().sort_values(ascending=False).index.tolist()
)
fig, ax = plt.subplots(figsize=(11, 5))
sns.boxplot(
    data=df,
    x="target",
    y="conc_uM",
    order=order,
    color="white",
    fliersize=0,
    ax=ax,
)
sns.swarmplot(
    data=df,
    x="target",
    y="conc_uM",
    order=order,
    alpha=0.85,
    edgecolor="k",
    linewidth=0.7,
    size=6,
    ax=ax,
)
ax.set_xlabel("")
ax.set_ylabel("Concentration / µM (post-pooling)")
ax.set_title(f"Yield by target ($N = {N}$, sorted by median)")
plt.tight_layout()
plt.savefig(OUT / "fig4C_yield_by_target.png", dpi=300)
plt.savefig(OUT / "fig4C_yield_by_target.svg")
plt.close()
print("✓ fig4C_yield_by_target.png")

# =============================================================
# Fig 4D — MW vs retention (mirrors notebook cell 24, simplified)
# =============================================================
fig, ax = plt.subplots(figsize=(8, 6))
norm = plt.Normalize(df["tot_yield"].min(), df["tot_yield"].max())
sm = plt.cm.ScalarMappable(cmap="Spectral_r", norm=norm)
sm.set_array([])

ax = sns.scatterplot(
    data=df,
    x="MW",
    y="main_peak_norm_retention",
    hue="tot_yield",
    palette="Spectral_r",
    zorder=10,
    edgecolor="k",
    linewidth=0.8,
    alpha=0.8,
    s=80,
    legend=False,
    ax=ax,
)
# Linear x-axis: MW range is narrow (16-18 kDa), log scale overlaps tick labels
ax.set_xlabel("MW / kDa")
# Convert x-axis to kDa for readability
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x/1000:.1f}"))
ax.set_ylabel("Norm. retention / a.u.")
ax.set_title(f"MW vs retention ($N = {N}$)")

cbar = plt.colorbar(sm, ax=ax)
cbar.set_label("Tot. yield / mg")
plt.tight_layout()
plt.savefig(OUT / "fig4D_mw_vs_retention.png", dpi=300)
plt.savefig(OUT / "fig4D_mw_vs_retention.svg")
plt.close()
print("✓ fig4D_mw_vs_retention.png")

print()
print(f"All figures saved to {OUT}")
