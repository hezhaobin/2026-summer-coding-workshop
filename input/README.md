# Input data

This directory contains the canonical data inputs and reusable derived tables. Do not duplicate these files in notebooks, analysis folders, or outputs.

- `raw/`: immutable files obtained from databases, collaborators, or prediction tools.
- `interim/`: regenerable normalization, identifier-mapping, eligibility, and parser intermediates.
- `processed/`: validated tables intended for repeated analysis or workshop use.

Every table should have a documented schema and source details. Preserve original protein identifiers and use explicit mapping tables for normalized identifiers.

Organization follows data lifecycle first and source within each data type:

- raw source sequences and source labels: `raw/labels/<dataset>/`;
- untouched source or tool predictor outputs: `raw/predictors/<dataset>/`;
- normalized sequences, parsed outputs, and mappings: `interim/<dataset>/`;
- validated reusable feature tables: `processed/`.

Analytical roles such as training, legacy comparison, or test data belong in
documented fields rather than directory names because those roles may change.
