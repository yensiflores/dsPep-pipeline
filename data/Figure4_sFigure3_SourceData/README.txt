Figure 4 - Source Data 1 (library-scale purification & yield, N=60)
 Figure4_library_60variants_SEC_yield_REDACTED.csv - all 60 tested variants,
 SEC metrics, yields, MW, retention, aggregation state. Peptide/DNA sequence columns
 (Peptide, eblock, ORF, tagged_peptide, exp_prod) REMOVED for IP; de-identified IDs retained.
 regenerate_sec_figures.py - figure code for Figure 4 A-C and supplementary Figure 3
 (MW vs retention); runs directly against the anonymised traces file below
 (no external inputs).
 Figure4_SEC_traces_60variants_ANON.h5 - the same 60 library variants WITH the per-well
 SEC chromatogram traces needed for panel A (overlay + clustered ridge plot). Binding-target
 names anonymised (Target 1-9); every peptide/DNA sequence column (Peptide, eblock, ORF,
 tagged_peptide, exp_prod) removed. This is an anonymised, sequence-free derivative of the
 internal SEC dataframe; the original (which carried sequences) is not redistributed.

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
