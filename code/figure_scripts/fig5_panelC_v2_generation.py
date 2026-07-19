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
fig,ax=plt.subplots(figsize=(10,3.5))
for i,t in enumerate(targets):
    vals=np.array([y for _,y in byt[t]]); jit=np.random.RandomState(0).uniform(-0.15,0.15,size=len(vals))
    ax.scatter(np.full(len(vals),i)+jit,vals,s=55,alpha=0.8,edgecolor="k",linewidth=0.5,color=COL[t],zorder=3)
    ax.plot([i-0.3,i+0.3],[np.median(vals)]*2,"k-",lw=2.2,zorder=2)
ax.axhline(2,ls=(0,(6,4)),c="#b0b0b0",lw=0.8); ax.axhline(10,ls=(0,(6,4)),c="#e08a8a",lw=0.8)
ax.text(-0.42,10*1.25,"10 µM  failed disulfide",fontsize=12,color="#c0392b",va="bottom",ha="left")
ax.text(-0.42,2*1.25,"2 µM  noise floor",fontsize=12,color="#777777",va="bottom",ha="left")
ax.set_yscale("symlog",linthresh=1); ax.set_ylim(-1.4,220); ax.set_yticks([-1,0,1,10,100]); ax.set_yticklabels(["-1","0","1","10","100"])
ax.set_xticks(range(len(targets))); ax.set_xticklabels(targets,fontsize=15,fontweight="bold")
ax.tick_params(axis="y",labelsize=13); ax.tick_params(axis="x",length=0)
ax.set_ylabel("Free Cys / µM (Ellman\'s)",fontsize=14)
ax.set_title(f"Free cysteine per peptide, grouped by target (n = {len(rows)})",fontsize=15)
ax.set_xlim(-0.7,len(targets)-0.3); fig.tight_layout()
for ext in ["png","svg","pdf"]: fig.savefig(f"figures_draft/Figure5/fig5_panelC_v2.{ext}",bbox_inches="tight")
