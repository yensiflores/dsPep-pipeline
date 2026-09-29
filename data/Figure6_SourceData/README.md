# Figure 6 — Source Data: Surface plasmon resonance (SPR)

Single-cycle-kinetics SPR sensorgrams for the representative designs shown in
Figure 6 (exported from Biacore Insight). One file per panel; tab-delimited .txt.

## Files
| File | Design | Format |
|------|--------|--------|
| T5-D1-sumo.txt   | Target 5, design 1 | recombinant His6–SUMO-tagged construct |
| T5-D1.txt        | Target 5, design 1 | peptide-only form |
| T5-D1-linear.txt | Target 5, design 1 | unconstrained linear peptide (negative control) |
| T3-D1-sumo.txt   | Target 3, design 1 | recombinant His6–SUMO-tagged construct |
| T3-D1.txt        | Target 3, design 1 | peptide-only form |
| T3-D2-sumo.txt   | Target 3, design 2 | recombinant His6–SUMO-tagged construct (matched non-binder) |
| T3-D2.txt        | Target 3, design 2 | peptide-only form (matched non-binder) |

## Column format (each file)
Tab-separated, four columns:
1. Measured_X — time (s)
2. Measured_Y — measured response (RU)
3. Fitted_X — time (s) for the fitted trace
4. Fitted_Y — global 1:1 fit response (RU)

The header row records run / channel / flow-cell / cycle and the injected
analyte concentration series (single-cycle kinetics).

## Anonymisation
Binding targets are de-identified as Target 3 / Target 5, and design identifiers
are anonymised (T{target}-D{design}). No target names or peptide sequences appear
in the file names or contents.

## Method
Single-cycle-kinetics SPR with a 1:1 binding fit; each file's header lists that
run's analyte concentration series. Instrument, buffer, capture and fitting
details are given in the Methods of the associated manuscript (in preparation).
