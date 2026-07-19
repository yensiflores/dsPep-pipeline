from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, csv
BASE=Path("figures_draft")
MERGED=BASE/"Figure5"/"sec_ellman_merged.csv"; UNK=BASE/"ellman_from_ada"/"unknowns_output.csv"
COL={"bcat":"#1f77b4","chip":"#2ca02c","dnan":"#9467bd","gaba":"#e377c2","mcl1":"#bcbd22","mrka":"#17becf"}
BSACOL="#d62728"; NICE={"dnan":"DnaN","gaba":"GABARAP","chip":"CHIP","bcat":"\u03b2-catenin","mcl1":"MCL-1","mrka":"MrkA"}
FAIL="Failure (10 µM)"; NOISE="Background noise (2 µM)"
rows=list(csv.DictReader(MERGED.open()))
for r in rows: r["target"]=r["target"].lower(); r["fc"]=float(r["ell_freecys_uM"]); r["design"]=r["name"].split("_")[-1]
unk=list(csv.DictReader(UNK.open())); k=list(unk[0].keys())
bsa=[(r[k[0]],float(r[k[1]])) for r in unk if str(r[k[0]]).upper().startswith("BSA")]
order=["dnan","gaba","chip","bcat","mcl1","mrka"]
plt.rcParams.update({"font.family":"Arial","svg.fonttype":"none","axes.spines.top":False,
    "axes.spines.right":False,"savefig.facecolor":"white","figure.facecolor":"white"})
fig,ax=plt.subplots(figsize=(11,4.2)); floor=0.1
INTRA=0.72; GAP=2.0
ax.grid(axis="y",color="#ececec",lw=0.6,zorder=0); ax.set_axisbelow(True)
ax.axhline(2,ls=(0,(6,4)),c="#b0b0b0",lw=0.8,zorder=1); ax.axhline(10,ls=(0,(6,4)),c="#e08a8a",lw=0.8,zorder=1)
cur=0.0; groups=[]; xt=[]; xtl=[]
for t in order:
    grp=sorted([r for r in rows if r["target"]==t],key=lambda r:r["fc"])
    xs=cur+np.arange(len(grp))*INTRA
    for r,xi in zip(grp,xs):
        ax.scatter(xi,max(r["fc"],floor),s=46,color=COL[t],edgecolor="black",lw=0.4,zorder=3)
        xt.append(xi); xtl.append(r["design"])
    groups.append((t,xs[0],xs[-1])); cur=xs[-1]+GAP
# BSA cluster
bxs=cur+np.arange(len(bsa))*INTRA
for (nm,val),xi in zip(bsa,bxs):
    ax.scatter(xi,max(val,floor),marker="^",s=74,color=BSACOL,edgecolor="black",lw=0.5,zorder=4)
    xt.append(xi); xtl.append(nm.replace("BSA",""))
groups.append(("BSA",bxs[0],bxs[-1]))
x0all=-0.6; x1all=bxs[-1]+0.6
ax.text(x0all+0.1,10*1.15,FAIL,fontsize=11,color="#c0392b",va="bottom",ha="left")
ax.text(x0all+0.1,2*1.15,NOISE,fontsize=11,color="#777777",va="bottom",ha="left")
ax.set_yscale("log"); ax.set_ylim(bottom=floor)
ax.set_xticks(xt); ax.set_xticklabels(xtl,fontsize=8); ax.tick_params(axis="x",length=0)
plt.setp(ax.get_yticklabels(),fontweight="semibold")
ax.set_xlim(x0all,x1all)
ax.set_ylabel("Free Cys / µM",fontsize=13,fontweight="bold"); ax.tick_params(axis="y",labelsize=11)
ax.set_title("Free cysteine per peptide",fontsize=13,fontweight="bold",pad=8)
tr=ax.get_xaxis_transform()
for t,a,b in groups:
    lab="BSA" if t=="BSA" else NICE[t]
    ax.plot([a-0.35,b+0.35],[-0.11,-0.11],transform=tr,color="#555",lw=1.1,clip_on=False)
    ax.text((a+b)/2,-0.18,lab,transform=tr,ha="center",va="top",fontsize=12,fontweight="bold",color="#1f3864")
ax.text(x0all,-0.18,"design →",transform=tr,ha="right",va="top",fontsize=8,color="#999",style="italic")
fig.subplots_adjust(left=0.075,right=0.985,top=0.95,bottom=0.16)
for ext in ["png","svg","pdf"]: fig.savefig(f"figures_draft/Figure5/Figure5_figsupp2_freecys_per_peptide.{ext}",bbox_inches="tight")
print("built; groups",[g[0] for g in groups])
