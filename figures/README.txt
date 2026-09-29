Figures - rendered final panels

The published Figure 1-6 exactly as they appear in the manuscript (anonymised;
binding targets shown as Target 1-9). Provided so the source data and figure
scripts under data/ and code/ can be checked against what the paper shows.

Figure1.png  Recombinant dsPep pipeline - workflow, timeline, cost
Figure2.png  Cloning / transformation QC
Figure3.png  Expression & purification (incl. 3B temperature-gel densitometry)
Figure4.png  Library-scale SEC yields (A-C)   [regenerate_sec_figures.py]
Figure5.png  Ellman's free-thiol staple QC (A-B)   [Figure5_stacked_AB_generation.py]
Figure6.png  SPR of representative designs (A-C)   [regenerate_figure6_SPR.py]

Note: regenerate_sec_figures.py writes four panels. The fourth, MW vs retention
(fig4D_mw_vs_retention), is supplementary Figure 3 - not part of Figure 4 - which is
why its source data sits in data/Figure4_sFigure3_SourceData/.
