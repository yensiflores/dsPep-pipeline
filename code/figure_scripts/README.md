# Figure scripts

These scripts are provided **for transparency** — they document exactly how the
manuscript figure panels were drawn from the source data in `../../data/`. They
are not part of the runnable pipeline (notebooks 1–4) and were authored against
the working `figures_draft/` tree, which is not included in this deposit; the
sequence-free equivalents of their inputs are the `*_REDACTED.csv` files under
`../../data/`. Machine-specific absolute paths have been reduced to relative
`figures_draft/...` references.

## Which panels are in the final manuscript

The final manuscript has 6 main figures (Figure 6, the SPR figure, is not part of
this deposit). Not every panel that was drafted made it into the final layout —
the table marks what is **final** vs **superseded**.

| Script | Figure / panel | Status |
|--------|----------------|--------|
| `build_fig1_composite.py` | Fig 1 A–C composite (workflow, timeline, cost) | final |
| `build_fig1_panelC.py` | Fig 1C (per-variant DNA cost) | final |
| `../../data/Figure2_source_data/cloning_efficiency_data/fig2_panelDE_generation.py` | Fig 2 transformation efficiency (drafted as "D/E", now Fig 2C) | final (renamed) |
| `regenerate_sec_figures.py` | Fig 4 A/B/C (SEC traces, yields, aggregation) | final (drafted panel "D" dropped) |
| `fig5_panelAB_generation.py` | Fig 5 A + B, and Fig 5–supplement 1 standard curve (`make_panel_a`) | final |
| `fig5_panelB_v2_generation.py` | Fig 5B (reformatted, two-tier axis) | final |
| `Figure5_stacked_AB_generation.py` | Fig 5 A+B stacked layout | final |
| `Figure5_figsupp2_generation.py` | Fig 5–supplement 2 (free Cys per peptide) | final (supplement) |
| `fig5_panelC_v2_generation.py` | drafted Fig 5C | **superseded — not in final** |
| `fig5_panelD_v2_generation.py` | drafted Fig 5D | **superseded — not in final** |
| `Figure5_stacked_ABC_generation.py` | drafted Fig 5 A+B+C stack | **superseded — not in final** |
| `merge_sec_ellman_panelC.py` | data prep for the drafted Fig 5C merge | **superseded — support** |

Final Figure 5 contains **panels A and B only** (plus supplements 1 and 2).
The superseded scripts are retained so the record of what was explored is complete.
