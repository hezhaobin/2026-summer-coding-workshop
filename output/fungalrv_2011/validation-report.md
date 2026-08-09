# FungalRV 2011 legacy import validation

## Sequence import

- Positive FASTA records: 101
- Negative FASTA records: 2644
- Empty sequences: 0
- Unexpected amino-acid characters: 0

## Brief KN identifier comparison

- `20251017-KN-negative-dataset-FRV-SignalP-PredGPI.csv`: 651 rows
- `20251017-KN-negative-dataset-other-features.csv`: 635 rows
- `positive-df-one.csv`: 22 rows
- `positive-df-three.csv`: 55 rows
- `positive-df-two.csv`: 25 rows
- Duplicate KN ID rows within the same file beyond the first: 6
- KN IDs present in more than one source file: 635
- FASTA records with at least one direct identifier match: 71
- FASTA records without a direct identifier match: 2674
- KN rows with a direct identifier match: 75
- KN rows without a direct identifier match: 1313
- Positive FASTA records matched directly: 67 of 101
- Negative FASTA records matched directly: 4 of 2644

This is intentionally a shallow identifier comparison. The KN files contain updated,
subsetted, and duplicate identifiers, so these source-provided features are not treated
as authoritative. Predictor and sequence-derived features will be recalculated from the
normalized FASTA sequences for consistent downstream analysis.
