Figure 5 - Source Data 1  (disulphide staple QC, Ellman's assay)
  ellmans_raw/   raw plate-reader workbook, cysteine standards, standard & unknown outputs,
                 plate layouts, analysis notebook (5_ellmans_analysis.ipynb)
  Figure5_sec_ellman_merged_REDACTED.csv  - merged SEC + Ellman table (peptide_seq column removed)
  panel-generation scripts
No IP sequences present.

UPDATE:
  fig5_panelB_v2_generation.py  - reformatted Panel B (two-tier axis, cleaner lines).
  figure_supplement1_standard_curve/ - the Ellman's L-cysteine standard curve, which moves to
     "Figure 5-figure supplement 1". Its underlying data are standard_output.csv / standards.csv
     in ellmans_raw/, and the code is in fig5_panelAB_generation.py (make_panel_a).
