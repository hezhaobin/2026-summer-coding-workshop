# 2026 Summer Coding Workshop

Materials and reproducible data preparation for a one-day beginner Python workshop on fungal adhesin prediction.

The workshop follows this progression:

> protein sequence → measurable features → group differences → simple classifier → candidate interpretation

## Start here

- Read `AGENTS.md` before making project changes.
- Read `docs/workshop_plan.md` for the authoritative teaching plan.
- Record scientific definitions and column meanings in `docs/data_dictionary.md`.
- Run data preparation through scripts; do not edit raw or derived tables manually.

## Repository map

| Path | Purpose |
| --- | --- |
| `input/raw/` | Immutable proteomes, curated labels, and original predictor outputs |
| `input/interim/` | Regenerable normalization, mapping, and parser intermediates |
| `input/processed/` | Validated reusable tables consumed by notebooks and analyses |
| `script/` | Reproducible download, validation, feature, parsing, and assembly code |
| `notebooks/` | Student and instructor-solution Colab notebooks |
| `analysis/` | Instructor-only exploration and quality control |
| `output/` | Regenerable reports, figures, logs, and candidate lists |
| `config/` | Species metadata, thresholds, and tool parameters |
| `tests/` | Automated tests and small synthetic fixtures |
| `docs/` | Workshop plan, source documentation, data dictionary, and teaching notes |

## Data flow

`input/raw/` → scripts and configuration → `input/interim/` → validation → `input/processed/` → notebooks/analysis → `output/`

Raw data are never edited in place. Interim, processed, and output files must be reproducible from version-controlled scripts and documented configuration.

## Current status

The three reference-proteome accessions are confirmed and UniProt release
`2026_02` has been frozen with checksums and source metadata. The morning
instructor and student notebooks are implemented and verified. Screening
thresholds, negative-set source and curation rules, and optional TANGO/XSTREAM
settings still require confirmation. See `docs/workshop_plan.md` for the complete
decision list.

The `dev` branch is the complete development and instructor source. The
independent `main` branch is the student distribution and contains only its
README, the morning student notebook, and the three frozen proteome FASTAs.
