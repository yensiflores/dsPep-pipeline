from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np, csv
BASE=Path("figures_draft")
MERGED=BASE/"Figure5"/"sec_ellman_merged.csv"
UNK=BASE/"ellman_from_ada"/"unknowns_output.csv"

# canonical palette = the colours from C/D that Yensi liked
COL={"bcat":"#1f77b4","chip":"#2ca02c","dnan":"#9467bd","gaba":"#e377c2","mcl1":"#bcbd22","mrka":"#17becf"}
BSACOL="#d62728"
NICE={"dnan":"dnaN","gaba":"GABA","chip":"CHIP","bcat":"BCAT","mcl1":"Mcl1","mrka":"MrkA"}
FAIL="Failure (10 µM)"; NOISE="Background noise (2 µM)"
AXW="bold"; NUMW="semibold"

rows=list(csv.DictReader(MERGED.open()))
for r in rows:
    r["target"]=r["target"].lower(); r["fc"]=float(r["ell_freecys_uM"]); r["conc"]=float(r["sec_conc_uM"])
    r["design"]=r["name"].split("_")[-1]
unk=list(csv.DictReader(UNK.open()))
bsa=[(r[list(r.keys())[0]],float(r[list(r.keys())[1]])) for r in unk if str(r[list(r.keys())[0]]).upper().startswith("BSA")]

plt.rcParams.update({"font.family":"Arial","svg.fonttype":"none","axes.spines.top":False,"axes.spines.right":False,
    "savefig.facecolor":"white","figure.facecolor":"white"})
fig=plt.figure(figsize=(9.5,11))
gs=GridSpec(3,1,height_ratios=[1.05,0.95,1.0],hspace=0.55)

def semibold_ticks(ax):
    plt.setp(ax.get_xticklabels(),fontweight=NUMW); plt.setp(ax.get_yticklabels(),fontweight=NUMW)
def panel_letter(ax,L):
    ax.text(-0.085,1.06,L,transform=ax.transAxes,fontsize=20,fontweight="bold",va="top",ha="left")

# ---------- Panel A : free cys per peptide + BSA (2-tier axis) ----------
axA=fig.add_subplot(gs[0])
orderA=["dnan","gaba","chip","bcat","mcl1","mrka"]
mA=[r for r in rows]
mA.sort(key=lambda r:(orderA.index(r["target"]),r["fc"]))
xA=np.arange(len(mA)); floor=0.1
axA.grid(axis="y",color="#e8e8e8",lw=0.6,zorder=0); axA.set_axisbelow(True)
axA.axhline(2,ls=(0,(6,4)),c="#b0b0b0",lw=0.8,zorder=1); axA.axhline(10,ls=(0,(6,4)),c="#e08a8a",lw=0.8,zorder=1)
for r,xi in zip(mA,xA):
    axA.scatter(xi,max(r["fc"],floor),s=42,color=COL[r["target"]],edgecolor="black",lw=0.4,zorder=3)
bx0=len(mA)+1; bxs=np.arange(bx0,bx0+len(bsa))
for (nm,val),xi in zip(bsa,bxs):
    axA.scatter(xi,max(val,floor),marker="^",s=70,color=BSACOL,edgecolor="black",lw=0.5,zorder=4)
axA.text(xA[0]-0.5,10*1.18,FAIL,fontsize=11,color="#c0392b",va="bottom",ha="left")
axA.text(xA[0]-0.5,2*1.18,NOISE,fontsize=11,color="#777777",va="bottom",ha="left")
axA.set_yscale("log"); axA.set_ylim(bottom=floor)
allx=np.concatenate([xA,bxs]); desg=[r["design"] for r in mA]+[nm.replace("BSA","") for nm,_ in bsa]
axA.set_xticks(allx); axA.set_xticklabels(desg,fontsize=8); axA.tick_params(axis="x",length=0)
axA.set_xlim(-1.0,bxs[-1]+1.0)
axA.set_ylabel("Free Cys / µM",fontsize=13,fontweight=AXW)
axA.tick_params(axis="y",labelsize=11); semibold_ticks(axA)
tr=axA.get_xaxis_transform()
def grp(xs,lab):
    x0,x1=xs.min(),xs.max()
    axA.plot([x0-0.45,x1+0.45],[-0.10,-0.10],transform=tr,color="#555",lw=1.0,clip_on=False)
    axA.text((x0+x1)/2,-0.17,lab,transform=tr,ha="center",va="top",fontsize=12,fontweight="bold",color="#1f3864")
for t in orderA:
    xs=np.array([xi for r,xi in zip(mA,xA) if r["target"]==t]); grp(xs,NICE[t])
grp(bxs,"BSA")
axA.text(-1.0,-0.17,"design →",transform=tr,ha="right",va="top",fontsize=8,color="#999",style="italic")
panel_letter(axA,"A")

# ---------- Panel B : free cys by target ----------
axB=fig.add_subplot(gs[1])
orderBC=sorted(COL)  # bcat chip dnan gaba mcl1 mrka
for i,t in enumerate(orderBC):
    vals=np.array([r["fc"] for r in rows if r["target"]==t])
    jit=np.random.RandomState(0).uniform(-0.15,0.15,size=len(vals))
    axB.scatter(np.full(len(vals),i)+jit,vals,s=52,alpha=0.85,edgecolor="k",lw=0.5,color=COL[t],zorder=3)
    axB.plot([i-0.3,i+0.3],[np.median(vals)]*2,"k-",lw=2.2,zorder=2)
axB.axhline(2,ls=(0,(6,4)),c="#b0b0b0",lw=0.8); axB.axhline(10,ls=(0,(6,4)),c="#e08a8a",lw=0.8)
axB.text(-0.42,10*1.25,FAIL,fontsize=11,color="#c0392b",va="bottom",ha="left")
axB.text(-0.42,2*1.25,NOISE,fontsize=11,color="#777777",va="bottom",ha="left")
axB.set_yscale("symlog",linthresh=1); axB.set_ylim(-1.4,220)
axB.set_yticks([-1,0,1,10,100]); axB.set_yticklabels(["-1","0","1","10","100"])
axB.set_xticks(range(len(orderBC))); axB.set_xticklabels([NICE[t] for t in orderBC],fontsize=13,fontweight="bold")
axB.tick_params(axis="y",labelsize=11); axB.tick_params(axis="x",length=0)
axB.set_ylabel("Free Cys / µM",fontsize=13,fontweight=AXW); semibold_ticks(axB)
axB.set_xlim(-0.7,len(orderBC)-0.3); panel_letter(axB,"B")

# ---------- Panel C : free cys vs yield ----------
axC=fig.add_subplot(gs[2])
for t in orderBC:
    xy=np.array([(r["conc"],r["fc"]) for r in rows if r["target"]==t])
    axC.scatter(xy[:,0],xy[:,1],s=60,alpha=0.85,edgecolor="k",lw=0.5,color=COL[t],zorder=3,label=NICE[t])
axC.axhline(10,ls=(0,(6,4)),c="#e08a8a",lw=0.8)
axC.text(22.3,10*1.28,FAIL,fontsize=11,color="#c0392b",va="bottom",ha="right")
axC.set_yscale("symlog",linthresh=1); axC.set_ylim(-1.4,220)
axC.set_yticks([-1,0,1,10,100]); axC.set_yticklabels(["-1","0","1","10","100"])
axC.set_xlim(0,22.5); axC.tick_params(axis="both",labelsize=11)
axC.set_xlabel("SEC concentration / µM (post-pooling)",fontsize=13,fontweight=AXW)
axC.set_ylabel("Free Cys / µM",fontsize=13,fontweight=AXW); semibold_ticks(axC)
axC.legend(loc="upper left",bbox_to_anchor=(0.005,1.0),fontsize=11,ncol=2,frameon=True,framealpha=0.92,edgecolor="#ccc")
panel_letter(axC,"C")

fig.subplots_adjust(left=0.11,right=0.97,top=0.96,bottom=0.06)
for ext in ["png","svg","pdf"]: fig.savefig(f"figures_draft/Figure5/Figure5_stacked_ABC.{ext}",bbox_inches="tight")
print("built combined figure; nA",len(mA),"bsa",len(bsa))
