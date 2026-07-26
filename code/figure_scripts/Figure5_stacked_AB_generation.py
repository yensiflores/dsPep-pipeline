from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np, csv
BASE=Path("figures_draft")
MERGED=BASE/"Figure5"/"sec_ellman_merged.csv"
COL={"Target4":"#1f77b4","Target7":"#2ca02c","Target9":"#9467bd","Target2":"#e377c2","Target8":"#bcbd22","Target5":"#17becf"}
NICE={"Target9":"Target 9","Target2":"Target 2","Target7":"Target 7","Target4":"Target 4","Target8":"Target 8","Target5":"Target 5"}
FAIL="Failure (10 µM)"; NOISE="Background noise (2 µM)"; AXW="bold"; NUMW="semibold"
rows=list(csv.DictReader(MERGED.open()))
for r in rows:
    r["target"]=r["target"].lower(); r["fc"]=float(r["ell_freecys_uM"]); r["conc"]=float(r["sec_conc_uM"])
order=sorted(COL)
plt.rcParams.update({"font.family":"Arial","svg.fonttype":"none","axes.spines.top":False,
    "axes.spines.right":False,"savefig.facecolor":"white","figure.facecolor":"white"})
fig=plt.figure(figsize=(9,7.9)); gs=GridSpec(2,1,height_ratios=[0.92,1.0],hspace=0.42)
def semibold(ax): plt.setp(ax.get_xticklabels(),fontweight=NUMW); plt.setp(ax.get_yticklabels(),fontweight=NUMW)
def letter(ax,L): ax.text(-0.085,1.06,L,transform=ax.transAxes,fontsize=20,fontweight="bold",va="top",ha="left")

# A : free cys by target
axA=fig.add_subplot(gs[0])
for i,t in enumerate(order):
    v=np.array([r["fc"] for r in rows if r["target"]==t]); j=np.random.RandomState(0).uniform(-0.15,0.15,len(v))
    axA.scatter(np.full(len(v),i)+j,v,s=54,alpha=0.85,edgecolor="k",lw=0.5,color=COL[t],zorder=3)
    axA.plot([i-0.3,i+0.3],[np.median(v)]*2,"k-",lw=2.2,zorder=2)
axA.axhline(2,ls=(0,(6,4)),c="#b0b0b0",lw=0.8); axA.axhline(10,ls=(0,(6,4)),c="#e08a8a",lw=0.8)
axA.text(-0.42,10*1.25,FAIL,fontsize=11,color="#c0392b",va="bottom",ha="left")
axA.text(-0.42,2*1.25,NOISE,fontsize=11,color="#777777",va="bottom",ha="left")
axA.set_yscale("symlog",linthresh=1); axA.set_ylim(-1.4,220); axA.set_yticks([-1,0,1,10,100]); axA.set_yticklabels(["-1","0","1","10","100"])
axA.set_xticks(range(len(order))); axA.set_xticklabels([NICE[t] for t in order],fontsize=11,fontweight="bold")
axA.tick_params(axis="y",labelsize=11); axA.tick_params(axis="x",length=0)
axA.set_ylabel("Free Cys / µM",fontsize=13,fontweight=AXW); semibold(axA)
axA.set_title("Free cysteine by target",fontsize=13,fontweight="bold",pad=8)
axA.set_xlim(-0.7,len(order)-0.3); letter(axA,"A")

# B : free cys vs yield
axB=fig.add_subplot(gs[1])
for t in order:
    xy=np.array([(r["conc"],r["fc"]) for r in rows if r["target"]==t])
    axB.scatter(xy[:,0],xy[:,1],s=60,alpha=0.85,edgecolor="k",lw=0.5,color=COL[t],zorder=3,label=NICE[t])
axB.axhline(10,ls=(0,(6,4)),c="#e08a8a",lw=0.8)
axB.text(22.3,10*1.28,FAIL,fontsize=11,color="#c0392b",va="bottom",ha="right")
axB.set_yscale("symlog",linthresh=1); axB.set_ylim(-1.4,220); axB.set_yticks([-1,0,1,10,100]); axB.set_yticklabels(["-1","0","1","10","100"])
axB.set_xlim(0,22.5); axB.tick_params(axis="both",labelsize=11)
axB.set_xlabel("SEC concentration / µM (post-pooling)",fontsize=13,fontweight=AXW)
axB.set_ylabel("Free Cys / µM",fontsize=13,fontweight=AXW); semibold(axB)
axB.legend(loc="upper left",bbox_to_anchor=(0.005,1.0),fontsize=11,ncol=2,frameon=True,framealpha=0.92,edgecolor="#ccc")
axB.set_title("Free cysteine vs yield",fontsize=13,fontweight="bold",pad=8)
letter(axB,"B")
fig.subplots_adjust(left=0.12,right=0.97,top=0.95,bottom=0.09)
for ext in ["png","svg","pdf"]: fig.savefig(f"figures_draft/Figure5/Figure5_stacked_AB.{ext}",bbox_inches="tight")
