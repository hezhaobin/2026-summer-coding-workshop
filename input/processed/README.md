# Processed data

Validated, reusable tables consumed by workshop notebooks and instructor analyses.

Expected products include:

- an instructor table with labels, source details, and all available features;
- a student table containing only the fields needed for each exercise;
- an unlabeled *Candida auris* candidate table;
- a data-quality summary with row counts, missingness, duplicates, and unresolved identifiers.

Every file must be reproducible from scripts and configuration. Do not place one-off figures or run logs here; those belong in `../../output/`.

Final parsed predictor fields and sequence-derived features belong here when they
are ready for reuse. Native tool outputs remain under `../raw/predictors/`, while
partially parsed or joined tables remain under `../interim/`.
