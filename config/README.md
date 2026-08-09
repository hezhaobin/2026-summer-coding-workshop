# Configuration

Version-controlled scientific and pipeline settings.

Planned files include species/strain metadata, exact UniProt proteome accessions, approved FungalRV and SignalP pass definitions, PredGPI encoding, sliding-window length, random seeds, and TANGO/XSTREAM parameters when resolved.

Do not invent missing scientific thresholds. Record the source and rationale for each parameter.

`proteomes.json` records the three approved UniProt reference-proteome accessions,
workshop strain names, and expected taxonomy and genome-assembly identifiers used
to guard the download stage against an accidental upstream mismatch. It also pins
the workshop release, protein counts, and SHA-256 checksums. Updating the release
is an explicit operation performed by `script/download_proteomes.py`.
