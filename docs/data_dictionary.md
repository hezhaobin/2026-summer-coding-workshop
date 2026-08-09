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

## Curated positive adhesin ID mapping

Canonical file:
`input/interim/curated-positive-adhesins/curated-positive-id-mapping.tsv`

| Column | Meaning |
| --- | --- |
| `source_file` | Raw curated label-table filename. |
| `source_row` | One-based spreadsheet row, including the header as row 1. |
| `curated_id` | UniProt accession supplied in the curated table. |
| `curated_name` | UniProt entry name supplied in the curated table. |
| `curated_id_occurrences` | Number of appearances of this ID in the curated table. |
| `match_status` | `exact-unique`, `unmatched`, or `ambiguous` accession match across the two reference proteomes. |
| `name_check` | Whether the curated name exactly matches the resolved UniProt entry name. |
| `matched_species` | Reference strain containing the resolved accession. |
| `reference_proteome_id` | UniProt reference-proteome accession. |
| `uniprot_accession` | Primary accession retained from the frozen FASTA header. |
| `uniprot_entry_name` | Entry name retained from the frozen FASTA header. |
| `gene_name` | Gene name retained from the frozen FASTA header, when present. |
| `protein_description` | Protein description retained from the frozen FASTA header. |
| `reference_fasta` | Frozen FASTA filename used for validation. |

Accession matching determines whether an ID is resolved. The curated name is an
independent consistency check and is not used as a replacement identifier.
