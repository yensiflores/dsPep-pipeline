from pathlib import Path
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, pandas as pd

BASE=Path("figures_draft")
UNK=BASE/"ellman_from_ada"/"unknowns_output.csv"
MERGED=BASE/"Figure5"/"sec_ellman_merged.csv"
TARGET_ORDER=["Target9","Target2","Target7","Target4","Target8","Target5"]

plt.rcParams.update({"font.family":"DejaVu Sans","axes.spines.top":False,"axes.spines.right":False,
    "savefig.facecolor":"white","figure.facecolor":"white"})

unk=pd.read_csv(UNK); unk=unk.rename(columns={unk.columns[0]:"well",unk.columns[1]:"free_cys_uM"})
unk["well"]=unk["well"].astype(str)
bsa=unk[unk["well"].str.upper().str.startswith("BSA")].copy()
merged=pd.read_csv(MERGED,usecols=["well","name","target","ell_freecys_uM"])
merged["target"]=merged["target"].str.lower()
merged=merged.dropna(subset=["target"])
merged=merged[merged["target"].isin(TARGET_ORDER)].copy()
merged["rank"]=merged["target"].map({t:i for i,t in enumerate(TARGET_ORDER)})
merged=merged.sort_values(["rank","ell_freecys_uM"]).reset_index(drop=True)
merged["design"]=merged["name"].str.split("_").str[-1]

cmap=plt.get_cmap("tab10"); tcol={t:cmap(i) for i,t in enumerate(TARGET_ORDER)}
x=np.arange(len(merged)); floor=0.1
bsa_x0=len(merged)+1; bsa_x=np.arange(bsa_x0,bsa_x0+len(bsa))

fig,ax=plt.subplots(figsize=(9.0,4.4))
# horizontal gridlines only, light
ax.grid(axis="y",color="#e8e8e8",linewidth=0.6,zorder=0); ax.set_axisbelow(True)

# threshold lines - thinner & lighter
ax.axhline(2.0,color="#b0b0b0",ls=(0,(6,4)),lw=0.7,zorder=1)
ax.axhline(10.0,color="#e08a8a",ls=(0,(6,4)),lw=0.7,zorder=1)
# labels moved to the LEFT, sitting just ABOVE each line (clear of line and legend)
ax.text(x[0]-0.5,10.0*1.18,"failure (10 µM)",fontsize=8,color="#c0392b",va="bottom",ha="left")
ax.text(x[0]-0.5,2.0*1.18,"noise floor (2 µM)",fontsize=8,color="#777777",va="bottom",ha="left")

for t in TARGET_ORDER:
    m=(merged["target"]==t).values
    if m.any():
        ax.scatter(x[m],merged["ell_freecys_uM"].clip(lower=floor)[m],s=40,color=tcol[t],
                   edgecolor="black",linewidth=0.4,zorder=3,label=t)
if len(bsa):
    ax.scatter(bsa_x,bsa["free_cys_uM"].clip(lower=floor),marker="^",s=72,color="#d62728",
               edgecolor="black",linewidth=0.5,zorder=4,label="BSA (+ control)")

ax.set_yscale("log"); ax.set_ylim(bottom=floor)
ax.set_ylabel("Free Cys (µM)",fontsize=11)
ax.set_title("Free cysteine per peptide (Ellman's assay) + BSA controls",fontsize=12)

# two-tier x axis: design number (tick) + grouped target name below a line
all_x=np.concatenate([x,bsa_x]) if len(bsa) else x
all_design=list(merged["design"])+[w.replace("BSA","") for w in bsa["well"]] if len(bsa) else list(merged["design"])
ax.set_xticks(all_x); ax.set_xticklabels(all_design,fontsize=8,rotation=0)
ax.tick_params(axis="x",length=0)
ax.set_xlim(-1.0,(bsa_x[-1] if len(bsa) else x[-1])+1.0)

tr=ax.get_xaxis_transform()  # x=data, y=axes-frac
def group(xs,label):
    x0,x1=xs.min(),xs.max()
    ax.plot([x0-0.45,x1+0.45],[-0.085,-0.085],transform=tr,color="#555555",lw=1.0,clip_on=False)
    ax.text((x0+x1)/2,-0.155,label,transform=tr,ha="center",va="top",fontsize=10,color="#1f3864")
for t in TARGET_ORDER:
    m=(merged["target"]==t).values
    if m.any(): group(x[m],t)
if len(bsa): group(bsa_x,"BSA")
# small caption for the tier
ax.text(-1.0,-0.155,"design →",transform=tr,ha="right",va="top",fontsize=8,color="#999999",style="italic")

ax.legend(loc="upper left",bbox_to_anchor=(1.01,1.0),frameon=False,title="target",fontsize=9,title_fontsize=10)
fig.subplots_adjust(bottom=0.20)
for ext in ["png","svg","pdf"]:
    fig.savefig(f"'figures_draft/Figure5/fig5_panelB_v2'.{ext}",bbox_inches="tight")
print("done; n_unk",len(merged),"n_bsa",len(bsa))
