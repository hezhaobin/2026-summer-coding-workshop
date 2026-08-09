# Curated positive adhesin ID validation

Source label table: `input/raw/labels/20260729-curated-positive-adhesin-set-KN.csv`

Frozen reference proteomes:

- *Saccharomyces cerevisiae S288C*: `UP000002311`, UniProt release `2026_02`
- *Candida albicans SC5314*: `UP000000559`, UniProt release `2026_02`

## Summary

- Curated rows: 30
- Exact unique accession matches: 30
- Unmatched IDs: 0
- Ambiguous IDs: 0
- Duplicate IDs in the curated table: 0
- Curated-name mismatches: 0

Matches by reference proteome:

- *Saccharomyces cerevisiae S288C*: 8
- *Candida albicans SC5314*: 22

## Interpretation

Every curated ID is present once in one reference proteome, and every curated `Name` agrees with the matched UniProt entry name. No obsolete or unresolved IDs are indicated by this frozen snapshot.

The accession match determines resolution. The curated `Name` field is used only as an independent consistency check.

Detailed table: `input/interim/curated-positive-adhesins/curated-positive-id-mapping.tsv`
