# Wet-lab protocols

Step-by-step bench protocols for the disulphide-stapled-peptide pipeline, provided
so the methods can be reproduced end to end.

| File | Covers | Related code / data |
|------|--------|---------------------|
| `cloning_ds-stapled_peptides.pdf` | IVA cloning of designs into the expression construct | `code/1_primer_design.ipynb`, `code/2_cloning_qc.ipynb`, `construct/` |
| `expression_and_purification.pdf` | Periplasmic secretion, DOC lysis, IMAC, SEC | `code/3_sec_analysis.ipynb` |
| `ellmans_free-thiol_assay.pdf` | Ellman's assay for free-cysteine / disulphide-staple QC | `code/4_ellmans_analysis.ipynb` |

The **Figure 3B densitometry method** (image analysis) is documented in
`data/Figure3_SourceData/densitometry_method.pdf`, next to its script.

## Notes
- The cloning protocol links to the expression-construct map on Benchling
  (`YFB001_PeriplasmicPeptideExpression`). The same sequence is included in this
  deposit as `construct/YFB001_pET24b_His6-SUMO-linker-ccdB.fasta`, so the protocol
  is fully usable even if the external link is unavailable.
- The Ellman's protocol refers to an analysis notebook by its original internal
  path (`.../Ellman/Ellmans_analysis.ipynb`); in this deposit that analysis is
  `code/4_ellmans_analysis.ipynb`.
- The expression/purification protocol links to an IPD internal wiki page for
  SEC/HPLC that is not publicly accessible; the SEC analysis is fully documented in
  `code/3_sec_analysis.ipynb` and `code/REPRODUCE_figure4_SEC.md`.
- No peptide sequences or target identities appear in these protocols; binding
  targets are anonymised (Target 1–Target 9) throughout the deposit.

Licence: CC BY 4.0 (see `../LICENSE-DATA-CC-BY-4.0.txt`).
