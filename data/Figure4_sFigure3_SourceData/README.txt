Figure 4 - Source Data 1  (library-scale purification & yield, N=60)
  Figure4_library_60variants_SEC_yield_REDACTED.csv  - all 60 tested variants (no subset),
     SEC metrics, yields, MW, retention, aggregation state. Peptide/DNA sequence columns
     (Peptide, eblock, ORF, tagged_peptide, exp_prod) REMOVED for IP; de-identified IDs retained.
  regenerate_sec_figures.py - figure code (originally reads the .h5; use the redacted CSV).
NOTE: the source .h5 is excluded because it contained sequences.

ANONYMISATION & PRIVACY
  - Binding-target names are anonymised throughout as "Target 1"-"Target 9"; design
    identifiers in the Name column are de-identified (e.g. TargetN_NN).
  - Some columns are sequence-DERIVED aggregate biophysical descriptors, retained
    because they characterise the library and underlie the yield/concentration
    calculations: Peptide_length, tagged_peptide_length, nAA, protomer_MW, MW,
    aliphatic_idx, e280, e205, OD280, OD205, nC (Cys count), charge@7.4, pI.
  - These descriptors do NOT reveal target identity, and the underlying peptide/DNA
    sequences cannot be reconstructed from them. Cross-referencing a row to a specific
    design would require already possessing the withheld sequences.
