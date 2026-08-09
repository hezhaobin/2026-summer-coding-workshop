# Scripts

Small, restartable programs for the reproducible data pipeline.

Planned responsibilities include proteome download, checksum and source-detail capture, FASTA inventory, identifier validation, sequence-feature calculation, predictor-output parsing, eligibility filtering, table assembly, and notebook-data export.

Prefer simple command-line interfaces, readable Python, explicit configuration, and clear failure messages. Reusable scientific logic belongs here rather than only in a notebook. Scripts must not modify `../input/raw/`.

`download_proteomes.py` is the controlled exception that creates new,
release-stamped files under `input/raw/proteomes/`. It validates existing cached
files and never edits or replaces a retained raw file. Normal runs use the frozen
configured snapshot; `--update-release YYYY_NN` is reserved for deliberately
freezing a newer current UniProt release for a future workshop.

`import_fungalrv_legacy.py` assigns stable IDs to the FungalRV 2011 positive and
negative FASTAs, writes a normalized FASTA and sequence header-information extract, and performs a
brief exact-identifier comparison with the source-provided KN feature tables.
