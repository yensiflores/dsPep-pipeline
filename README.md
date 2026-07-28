# A scalable recombinant pipeline for disulphide-stapled peptides — code and data

This repository accompanies the manuscript *"A scalable recombinant pipeline for
disulphide-stapled peptides validated across diverse target classes"*
(Flores Bueso, Gökçe, Jeung, Rettie, Baker, Tangney & Bhardwaj). It contains the
analysis code and the sequence-free source data needed to reproduce the methods
and figures.

## What this pipeline does
A 96-well-compatible recombinant workflow for disulphide-stapled cyclic peptides:
automated primer design (reverse-translation and codon optimisation, IVA primer
assembly), qPCR-monitored cloning, periplasmic secretion and sodium-deoxycholate
lysis, IMAC purification, size-exclusion chromatography (SEC) yield analysis, and
an Ellman's free-thiol read-out for disulphide-staple quality control.

## Contents
- `code/` — analysis notebooks and figure scripts
  - `1_primer_design.ipynb` — reverse-translation, DNA-Chisel constraint
    optimisation, and IVA primer-pair assembly (fixed 3' adapter tail +
    peptide-encoding extension + variable 5' homology block)
  - `2_cloning_qc.ipynb` — in-silico assembly/ORF check of the IVA product
  - `3_sec_analysis.ipynb` — SEC trace alignment, per-well mapping, yield
    integration, and average-linkage hierarchical clustering (Figure 4)
  - `4_ellmans_analysis.ipynb` — Ellman's assay standard curve and free-thiol
    quantification (Figure 5)
  - `REPRODUCE_figure4_SEC.md` — how to run notebook 3 for full reproduction
  - `figure_scripts/` — scripts that draw the figure panels (transparency only;
    see `figure_scripts/README.md` for which panels are final vs superseded)
- `construct/` — the expression construct designed for this work:
  `YFB001_pET24b_His6-SUMO-linker-ccdB.fasta` (His6–SUMO–linker–ccdB in a
  pET-24b(+) backbone; the ccdB cassette is replaced by the peptide-encoding
  sequence during IVA cloning)
- `data/` — sequence-free source data, organised by figure:
  `Figure2_SourceData/` (cloning gels, qPCR traces, transformation OD),
  `Figure3_SourceData/` (secretion densitometry),
  `Figure4_sFigure3_SourceData/` (SEC yield table, keyed by design ID/target),
  `Figure5_sFigure4_SourceData/` (Ellman's data + merged SEC/Ellman table),
  `sFigure1_lysis-SDS-PAGE/` (DOC vs sucrose lysis gels),
  `sFigure2_temperature_gels/` (secretion-signal temperature series). Several
  folders carry their own README.
- `protocols/` — step-by-step wet-lab protocols (IVA cloning, expression &
  purification, Ellman's free-thiol assay); see `protocols/README.md`. The Figure 3B
  densitometry method is in `data/Figure3_SourceData/densitometry_method.pdf`.
- `examples/example_peptides.fasta` — a small **synthetic** example input
- `requirements.txt` — Python dependencies (tested on Python 3.10)

## Running the pipeline
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd code && jupyter notebook
```
Run the notebooks in order; intermediate/derived files are written to
`code/outputs/` (created on first run).

- **Notebooks 1, 2 and 4 run end-to-end as shipped.** Notebook 1 reads the
  synthetic `examples/example_peptides.fasta` and writes `pcr_input.csv`;
  notebook 2 consumes that plus the `construct/` plasmid to simulate the
  assembly and translate the His6–SUMO–peptide ORF; notebook 4 reads the
  Ellman's data in `data/Figure5_sFigure4_SourceData/ellmans_raw/` and reproduces the
  standard curve and free-thiol table. The constant IVA adapter / primer-binding
  / T7 / RBS sequences these notebooks use are part of the **public construct
  backbone** in `construct/` — no peptide design sequences are involved.
- **Notebook 3 (SEC) is provided in full but needs external inputs** to
  reproduce Figure 4: the SEC engine in the SAPP_DMX repository
  (github.com/bwicky/SAPP_DMX), plus raw HPLC traces and a column-calibration
  file. See `code/REPRODUCE_figure4_SEC.md`.

## Important notes on scope
- **Designed peptide sequences are not included.** The peptide amino-acid
  sequences and the FASTA/eBlock inputs that encode them are intellectual
  property and have been withheld. The notebooks run on the synthetic example;
  users supply their own sequences. Derived source-data tables are keyed by
  de-identified design ID (sequence columns removed — see the per-figure READMEs).
- **The construct backbone sequence is shared** (see `construct/`); it contains
  no peptide designs.
- **Binding-target names are anonymised** (Target 1–Target 9) throughout the code
  and data.

## Licence
- Code (`code/`): MIT — see `LICENSE-MIT.txt`
- Data and construct (`data/`, `construct/`): CC BY 4.0 — see
  `LICENSE-DATA-CC-BY-4.0.txt`

## Acknowledgements
Notebook 3 (SEC analysis) is built on top of **SAPP_DMX** by **Basile Wicky**
(Institute for Protein Design) — https://github.com/bwicky/SAPP_DMX — which
provides the SEC chromatogram parsing, column calibration and fraction-pooling
routines (`wetlab_utils`, `SEC_pool_and_norm`). That code is not redistributed
here; please cite SAPP_DMX if you use notebook 3.

## AI assistance
The analysis/figure-generation code and the packaging of this deposit were
prepared with assistance from an AI tool (Claude, Anthropic); the raw experimental
data were generated by the authors in the laboratory. See `AI_ASSISTANCE.md` for a
full disclosure, including representative prompts, for reproducibility.

## Citation
If you use this pipeline, please cite the manuscript and this deposit
(DOI: [10.5281/zenodo.21441297](https://doi.org/10.5281/zenodo.21441297); see
`CITATION.cff`), and cite **SAPP_DMX** (above) if you use the SEC analysis.
