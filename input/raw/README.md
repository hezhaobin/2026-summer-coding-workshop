# Raw data

Immutable source data. Never edit these files in place.

Expected organization:

- `proteomes/<species>/`: frozen reference-proteome FASTA files.
- `labels/`: original curated positive and negative label files.
- `predictors/<species>/`: original FungalRV, SignalP, PredGPI, TANGO, XSTREAM, or NetGPI outputs.

For every file, record its source, strain, acquisition date, version or database release, relevant parameters, and checksum in a source-information record. Parsing and cleanup must write to `../interim/` or `../processed/`.

## Proteome acquisition

The configured UniProt reference proteomes are downloaded with:

```bash
python3 script/download_proteomes.py
```

The script normally verifies the configured release and checksums without network
access. If a configured file is absent, it downloads from UniProt only when the
server reports the configured release and the content matches the recorded
checksum. It validates accession, strain, taxonomy, assembly, and record count
before retaining a release-stamped FASTA, the unmodified UniProt metadata, and a
download-information sidecar. Existing raw files are never overwritten.

UniProt does not provide small per-proteome files in its previous-release
archives; archived knowledgebase releases are distributed as very large bundles.
The frozen local files and their configured checksums are therefore the stable
workshop snapshot. The source URLs are official but serve UniProt's current
release.

To deliberately freeze a newer release for a future workshop, first confirm that
it is the current UniProt release, then run:

```bash
python3 script/download_proteomes.py --update-release YYYY_NN
```

This downloads and validates all three proteomes, creates new release-stamped raw
files without removing the previous snapshot, and updates `config/proteomes.json`
with the new release, counts, and checksums. Review and commit that configuration
change together with the chosen distribution of the new raw files.

Downloaded proteomes are modest but are still large generated inputs. No Git LFS
or other large-file policy has been selected yet, so decide whether to track these
files directly, use Git LFS, or distribute them separately before committing them.

## Legacy FungalRV data

`labels/fungalrv_2011/` contains the publication's positive and negative FASTA
sets. Their labels are retained as legacy source labels, not biological ground
truth. Source-provided KN feature tables are kept separately under
`predictors/fungalrv_2011/kn_2025/`; they are used only for a brief import check
because features will be recalculated consistently from the raw sequences.
