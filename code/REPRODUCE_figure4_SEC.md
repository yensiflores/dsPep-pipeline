# Reproducing Figure 4 (library-scale SEC yields) with `3_sec_analysis.ipynb`

The SEC analysis notebook reproduces the Figure 4 panels (SEC traces, total
soluble-yield distribution, aggregation/pooling statistics) from raw HPLC
chromatograms. Unlike notebooks 1, 2 and 4, it is **not** fully self-contained,
because two of its dependencies are not redistributed in this
deposit:

1. **The SEC analysis engine** (`wetlab_utils` — `parse_chromatograms`,
   `process_sec_data`, `yields`, `calibrated_results`, `protparam`,
   `select_fractions`, `gen_ot2_script`, …) is third-party code by
   **Basile Wicky (IPD)**, distributed in the **SAPP_DMX** repository, not here.
2. **The raw HPLC traces and the column-calibration file** are large instrument
   data that live outside this record.

The notebook code is provided in full for transparency and to document exactly
how the published numbers were produced.

## What you need to supply

| Item | What it is | How to get it |
|------|------------|----------------|
| `SAPP_DMX` | SEC engine + `SEC_pool_and_norm_v3.py` | `git clone https://github.com/bwicky/SAPP_DMX.git` |
| `pycorn` | HPLC/ÄKTA trace parser | `pip install pycorn` |
| Calibration `.json` | column calibration (`Vo`, `Vc`, `slope`, `intercept`, `log10mw`, `Kav`) | your SEC run's calibration file (e.g. `231123_S75_5-150_HPLC.json`) |
| HPLC trace folders | one folder per injection + a `fractions.csv` | your instrument export (e.g. `20240517_dsPep/`) |
| `sec_input.csv` | well → design map (`Destination Well`, `ORF`, `eblock`, …) | produced by `2_cloning_qc.ipynb`; for the 60-variant figure, use your real run's file |

## Configure and run

Set the paths via environment variables (read by the CONFIG cell at the top of
the notebook), then launch Jupyter from the `code/` directory:

```bash
export SAPP_DMX_DIR=/path/to/SAPP_DMX
export SEC_CALIBRATION=/path/to/231123_S75_5-150_HPLC.json
export SEC_TRACES_GLOB='/path/to/20240517_dsPep/*'
export SEC_INPUT=/path/to/your/sec_input.csv    # optional; defaults to code/outputs/sec_input.csv
jupyter notebook 3_sec_analysis.ipynb
```

Figures and tables are written to `code/outputs/` (and `code/outputs/SEC_outputs/`).
The scalar results table it saves (`YYYY-MM-DD_expdata_df.csv`) corresponds,
after removing the peptide/DNA-sequence columns, to
`data/Figure4_source_data/Figure4_library_60variants_SEC_yield_REDACTED.csv`.


