from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, csv
MERGED=Path("figures_draft/Figure5/sec_ellman_merged.csv")
COL={"dnan":"#1f77b4","gaba":"#ff7f0e","chip":"#2ca02c","bcat":"#d62728","mcl1":"#9467bd","mrka":"#8c564b"}  # matches Panel B
rows=list(csv.DictReader(MERGED.open()))
byt={}
for r in rows: byt.setdefault(r["target"].lower(),[]).append((float(r["sec_conc_uM"]),float(r["ell_freecys_uM"])))
targets=sorted(byt)
plt.rcParams.update({"font.family":"DejaVu Sans","axes.spines.top":False,"axes.spines.right":False,"savefig.facecolor":"white","figure.facecolor":"white"})
fig,ax=plt.subplots(figsize=(9,4.3))
for t in targets:
    xy=np.array(byt[t]); ax.scatter(xy[:,0],xy[:,1],s=62,alpha=0.8,edgecolor="k",linewidth=0.5,color=COL[t],zorder=3,label=t)
ax.axhline(10,ls=(0,(6,4)),c="#e08a8a",lw=0.8)
ax.text(22.3,10*1.28,"10 µM  failed disulfide",fontsize=12,color="#c0392b",va="bottom",ha="right")
ax.set_yscale("symlog",linthresh=1); ax.set_ylim(-1.4,220); ax.set_yticks([-1,0,1,10,100]); ax.set_yticklabels(["-1","0","1","10","100"])
ax.set_xlim(0,22.5); ax.tick_params(axis="both",labelsize=13)
ax.set_xlabel("SEC concentration / µM (post-pooling)",fontsize=14); ax.set_ylabel("Free Cys / µM (Ellman\'s)",fontsize=14)
ax.set_title("Disulphide formation vs expression yield, by target",fontsize=15)
ax.legend(loc="upper left",bbox_to_anchor=(0.005,1.0),fontsize=12,ncol=2,frameon=True,framealpha=0.92,edgecolor="#cccccc")
fig.tight_layout()
for ext in ["png","svg","pdf"]: fig.savefig(f"figures_draft/Figure5/fig5_panelD_v2.{ext}",bbox_inches="tight")
