# Figure scripts

These scripts document how each manuscript figure panel was drawn from the
deposited source data. They fall into two groups.

## Runnable against this deposit

Run with no external inputs (Python 3.10; `pip install -r ../../requirements.txt`).
Each reads only deposited, anonymised data and writes its output next to itself.

| Script | Figure / panel |
|--------|----------------|
| `Figure5_stacked_AB_generation.py` | **Figure 5 (authoritative).** A: free cysteine by target; B: free cysteine vs SEC yield. Published palette and panel order (Target 2, 4, 5, 7, 8, 9). Reads `../../data/Figure5_sFigure4_SourceData/Figure5_sec_ellman_merged.csv`. |
| `regenerate_figure6_SPR.py` | Figure 6 — SPR sensorgrams (measured + global 1:1 fit). Reads `../../data/Figure6_SourceData/`. |
| `../../data/Figure2_SourceData/Fig2C_cloning_efficiency_data/fig2_panelDE_generation.py` | Figure 2 D/E — transformation OD600 heatmap + cPCR/Sanger pass rates. Reads `Figure2_transformation_OD_test.csv` beside it. |
| `../../data/Figure3_SourceData/densitometry_pct_total_lane.py` | Figure 3B — temperature-gel densitometry. Reads the gel image + box JSON beside it. |
| `../../data/Figure4_sFigure3_SourceData/regenerate_sec_figures.py` | Figure 4 A–C + supplementary Figure 3 — SEC chromatogram overlay, yield histogram and per-target yields (Figure 4 A–C), plus MW vs retention (sFigure 3). Reads the anonymised `Figure4_SEC_traces_60variants_ANON.h5` beside it (per-well traces; target names anonymised, peptide sequences removed). |

## Provenance only (not runnable as shipped)

These document how a figure or a deposited table was produced from internal
working files that are **not redistributed** (for intellectual-property /
anonymisation reasons). The deposited `*_SourceData` tables are their outputs.
Each script carries a `PROVENANCE` header stating exactly what it needs.

| Script | What it needs / produced |
|--------|--------------------------|
| `../../data/Figure5_sFigure4_SourceData/merge_sec_ellman_panelB.py` | Produced the deposited, anonymised `Figure5_sec_ellman_merged.csv` from the internal SEC dataframe + Ellman's unknowns (inputs not redistributed). |
| `build_fig1_composite.py` | Composites the Figure 1 workflow schematic (`manuscript/SVG/Asset 1.svg`, not bundled) with matplotlib panels via `svgutils`. |

## Figure 5 — one authoritative script

Earlier drafts held three scripts that each drew Figure 5 with a different target
order, so the same target changed colour between them. This is resolved:
**`Figure5_stacked_AB_generation.py` is the sole authoritative Figure 5 script** —
it reproduces the published panels, palette and order. The superseded variants
(`fig5_panelAB_generation.py`, `fig5_panelA_generation.py`) have been removed.
