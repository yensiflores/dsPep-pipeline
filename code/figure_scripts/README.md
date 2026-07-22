# Figure scripts

These scripts are provided **for transparency** — they document how the manuscript
figure panels were drawn from the source data in `../../data/`. They are not part of
the runnable pipeline (notebooks 1–4) and were authored against the working
`figures_draft/` tree, which is not included in this deposit; the sequence-free
equivalents of their inputs are the tables under `../../data/`. Machine-specific
absolute paths have been reduced to relative `figures_draft/...` references.

> The **canonical, final** copies of several of these scripts also live next to
> their data, inside the `data/*_SourceData*/` folders (e.g.
> `fig5_panelA_generation.py`, `fig5_panelAB_generation.py`,
> `merge_sec_ellman_panelB.py`, `regenerate_sec_figures.py`,
> `fig2_panelDE_generation.py`). This folder keeps the figure-drawing scripts
> collected in one place; superseded/exploratory panel variants have been removed.

## Scripts and the panels they draw (all final)

| Script | Figure / panel |
|--------|----------------|
| `build_fig1_composite.py` | Fig 1 A–C composite (workflow, timeline, cost) |
| `build_fig1_panelC.py` | Fig 1C (per-variant DNA cost) |
| `../../data/Figure2_SourceData/Fig2C_cloning_efficiency_data/fig2_panelDE_generation.py` | Fig 2C transformation efficiency |
| `regenerate_sec_figures.py` | Fig 4 A/B/C (SEC traces, yields, aggregation) |
| `fig5_panelAB_generation.py` | Fig 5 A + B, and Fig 5–supplement 1 standard curve (`make_panel_a`) |
| `fig5_panelB_v2_generation.py` | Fig 5B (reformatted, two-tier axis) |
| `Figure5_stacked_AB_generation.py` | Fig 5 A+B stacked layout |
| `Figure5_figsupp2_generation.py` | Fig 5–supplement 2 (free Cys per peptide) |

Final Figure 5 contains **panels A and B only** (plus supplements 1 and 2). The
earlier exploratory panel-C/D and A+B+C-stack variants have been removed.
