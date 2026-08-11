# Data dictionary

This dictionary will expand as processed feature tables are assembled. Raw source
column names remain unchanged in their original files.

## FungalRV 2011 sequence header-information extract

Canonical file: `input/interim/fungalrv_2011/sequence-header-info-extract.tsv`

| Column | Meaning |
| --- | --- |
| `stable_id` | Project-controlled ID assigned in fixed FASTA record order. |
| `legacy_source` | Source dataset; currently `fungalrv_2011`. |
| `legacy_label` | Publication label, `positive` or `negative`; this is not treated as biological ground truth. |
| `source_file` | Canonical raw FASTA filename. |
| `source_record_number` | One-based record order within the source FASTA. |
| `original_header` | Complete unmodified source FASTA header. |
| `source_id` | Conservatively parsed primary identifier from the source header. |
| `protein_length` | Number of amino-acid residues in the imported sequence. |

The paired normalized FASTA is
`input/interim/fungalrv_2011/normalized-sequences.fasta`. Its headers carry
`stable_id`, `legacy_source`, `legacy_label`, and `source_id`.

## Brief KN source-file comparison

Canonical file: `input/interim/fungalrv_2011/kn-source-file-matches.tsv`

| Column | Meaning |
| --- | --- |
| `legacy_label` | Positive or negative FungalRV source set. |
| `stable_id` | Matching sequence ID; blank for an unmatched KN row. |
| `source_id` | Primary identifier parsed from the FASTA header. |
| `kn_file` | Raw source-provided KN feature filename. |
| `kn_row_number` | One-based data-row number in the KN file. |
| `kn_id` | Identifier as supplied in the KN table. |
| `match_status` | `direct_id_match`, `ambiguous_id_match`, `fasta_unmatched`, or `kn_unmatched`. |

This comparison is an import check only. KN feature values are not authoritative;
features will be recalculated consistently from sequence.

## Curated positive adhesin ID matches

Canonical file:
`input/interim/curated-positive-adhesins/curated-positive-id-matches.tsv`

| Column | Meaning |
| --- | --- |
| `curated_id` | UniProt accession supplied in the curated table. |
| `species` | Reference proteome containing the ID; blank if unresolved. |
| `match_status` | `matched`, `unmatched`, or `ambiguous` across the two proteomes. |
| `duplicate_in_curated_set` | Whether the ID appears more than once in the curated table. |

## Morning known-adhesin IDs

Canonical file: `input/processed/morning-known-adhesins.tsv`

This student-safe table is generated only after every KN curated positive ID
matches exactly one of the frozen *S. cerevisiae* or *C. albicans* proteomes and
no curated ID is duplicated. Precomputed KN feature values are intentionally
excluded.

| Column | Meaning |
| --- | --- |
| `protein_id` | Validated UniProt accession in a frozen workshop proteome. |
| `protein_name` | Protein name retained from the KN curated positive table. |
| `species` | Full species name for the matched frozen proteome. |

## Sequence-derived teaching features

| Feature | Definition and behavior |
| --- | --- |
| `protein_length` | Number of amino-acid residues in the sequence. |
| `st_frequency` | `(count(S) + count(T)) / protein_length`; an empty sequence is missing (`None`), and every non-S/T residue remains in the denominator. |
| `sliding_st_frequencies` | Ordered list of S/T fractions for every overlapping window, moving one residue at a time. List item `i` describes the window beginning at zero-based position `i`. An empty sequence returns `[]`; a sequence no longer than the window returns one whole-sequence value. |
| `max_st_frequency_window` | Maximum value in `sliding_st_frequencies`; missing (`None`) for an empty sequence. The teaching window is controlled by `WINDOW_SIZE` and defaults to 50 residues. |
