#!/usr/bin/env python3
"""Verify or download the frozen UniProt proteomes used by the workshop.

Run without arguments for the configured snapshot. To freeze a newer current
UniProt release, run with ``--update-release YYYY_NN``. Existing raw files are
never overwritten.
"""

import argparse
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_VERSION = "2.0.0"
UNIPROT_API = "https://rest.uniprot.org"
USER_AGENT = f"fungal-adhesin-workshop/{SCRIPT_VERSION}"
REPOSITORY = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPOSITORY / "config" / "proteomes.json"
RAW_ROOT = REPOSITORY / "input" / "raw" / "proteomes"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def urls_for(accession: str) -> tuple[str, str]:
    metadata_url = f"{UNIPROT_API}/proteomes/{accession}"
    query = urllib.parse.urlencode(
        {"format": "fasta", "query": f"(proteome:{accession})"}
    )
    fasta_url = f"{UNIPROT_API}/uniprotkb/stream?{query}"
    return metadata_url, fasta_url


def download(url: str) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
        headers = {name.lower(): value for name, value in response.headers.items()}
    if not data:
        raise RuntimeError(f"empty download: {url}")
    return data, headers


def count_fasta_records(data: bytes) -> int:
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as error:
        raise RuntimeError("downloaded FASTA is not ASCII text") from error
    count = sum(line.startswith(">") for line in text.splitlines())
    if count == 0:
        raise RuntimeError("downloaded FASTA contains no records")
    return count


def validate_metadata(metadata: dict, proteome: dict) -> None:
    expected = {
        "proteome accession": (metadata.get("id"), proteome["proteome_accession"]),
        "proteome type": (metadata.get("proteomeType"), "Reference proteome"),
        "taxon ID": (
            metadata.get("taxonomy", {}).get("taxonId"),
            proteome["expected_taxon_id"],
        ),
        "genome assembly": (
            metadata.get("genomeAssembly", {}).get("assemblyId"),
            proteome["expected_assembly_accession"],
        ),
    }
    for label, (observed, wanted) in expected.items():
        if observed != wanted:
            raise RuntimeError(f"{label} is {observed!r}; expected {wanted!r}")
    if proteome["strain"].casefold() not in metadata.get("strain", "").casefold():
        raise RuntimeError(f"metadata does not identify strain {proteome['strain']}")


def download_proteome(proteome: dict, requested_release: str) -> dict:
    accession = proteome["proteome_accession"]
    metadata_url, fasta_url = urls_for(accession)
    metadata_data, metadata_headers = download(metadata_url)
    fasta_data, fasta_headers = download(fasta_url)
    metadata = json.loads(metadata_data)

    releases = {
        metadata_headers.get("x-uniprot-release"),
        fasta_headers.get("x-uniprot-release"),
    }
    if releases != {requested_release}:
        raise RuntimeError(
            f"{accession}: UniProt returned release(s) {sorted(str(x) for x in releases)}; "
            f"requested {requested_release}"
        )
    validate_metadata(metadata, proteome)
    record_count = count_fasta_records(fasta_data)
    if record_count != metadata.get("proteinCount"):
        raise RuntimeError(
            f"{accession}: FASTA has {record_count} records; "
            f"metadata reports {metadata.get('proteinCount')}"
        )

    return {
        "metadata_data": metadata_data,
        "fasta_data": fasta_data,
        "metadata_url": metadata_url,
        "fasta_url": fasta_url,
        "release_date": fasta_headers.get("x-uniprot-release-date"),
        "record_count": record_count,
        "fasta_sha256": sha256(fasta_data),
        "metadata_sha256": sha256(metadata_data),
        "metadata": metadata,
    }


def snapshot_paths(proteome: dict, release: str) -> tuple[Path, Path, Path]:
    directory = RAW_ROOT / proteome["slug"]
    prefix = f"{proteome['proteome_accession']}-uniprot-{release}"
    return (
        directory / f"{prefix}.fasta",
        directory / f"{prefix}.proteome.json",
        directory / f"{prefix}.download-info.json",
    )


def verify_cached_snapshot(proteome: dict, release: str) -> bool:
    fasta_path, metadata_path, download_info_path = snapshot_paths(proteome, release)
    existing = [path.exists() for path in (fasta_path, metadata_path, download_info_path)]
    if not any(existing):
        return False
    if not all(existing):
        raise RuntimeError(f"incomplete cached snapshot for {proteome['proteome_accession']}")

    fasta_data = fasta_path.read_bytes()
    metadata_data = metadata_path.read_bytes()
    if sha256(fasta_data) != proteome["fasta_sha256"]:
        raise RuntimeError(f"checksum mismatch: {fasta_path}")
    if sha256(metadata_data) != proteome["metadata_sha256"]:
        raise RuntimeError(f"checksum mismatch: {metadata_path}")
    if count_fasta_records(fasta_data) != proteome["protein_count"]:
        raise RuntimeError(f"record-count mismatch: {fasta_path}")

    print(
        f"CACHED {proteome['proteome_accession']} release {release} "
        f"({proteome['protein_count']} records)"
    )
    return True


def write_new_file(path: Path, data: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"refusing to overwrite raw file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.part")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def download_info(proteome: dict, release: str, result: dict) -> bytes:
    record = {
        "schema_version": 1,
        "script": "script/download_proteomes.py",
        "script_version": SCRIPT_VERSION,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "UniProt REST API",
        "proteome_accession": proteome["proteome_accession"],
        "workshop_organism": proteome["workshop_organism"],
        "strain": proteome["strain"],
        "uniprot_scientific_name": result["metadata"]["taxonomy"]["scientificName"],
        "uniprot_taxon_id": result["metadata"]["taxonomy"]["taxonId"],
        "genome_assembly_accession": result["metadata"]["genomeAssembly"]["assemblyId"],
        "uniprot_release": release,
        "uniprot_release_date": result["release_date"],
        "metadata_url": result["metadata_url"],
        "fasta_url": result["fasta_url"],
        "protein_count": result["record_count"],
        "fasta_sha256": result["fasta_sha256"],
        "metadata_sha256": result["metadata_sha256"],
    }
    return (json.dumps(record, indent=2) + "\n").encode("utf-8")


def freeze_download(proteome: dict, release: str, result: dict) -> None:
    fasta_path, metadata_path, download_info_path = snapshot_paths(proteome, release)
    write_new_file(fasta_path, result["fasta_data"])
    write_new_file(metadata_path, result["metadata_data"])
    write_new_file(download_info_path, download_info(proteome, release, result))


def use_configured_snapshot(config: dict) -> None:
    release = config["frozen_release"]
    for proteome in config["proteomes"]:
        if verify_cached_snapshot(proteome, release):
            continue
        result = download_proteome(proteome, release)
        if result["fasta_sha256"] != proteome["fasta_sha256"]:
            raise RuntimeError(f"unexpected FASTA checksum for {proteome['proteome_accession']}")
        if result["metadata_sha256"] != proteome["metadata_sha256"]:
            raise RuntimeError(
                f"unexpected metadata checksum for {proteome['proteome_accession']}"
            )
        freeze_download(proteome, release, result)
        print(f"DOWNLOADED {proteome['proteome_accession']} release {release}")


def update_release(config: dict, release: str) -> None:
    if release == config["frozen_release"]:
        raise RuntimeError(f"release {release} is already configured")

    results = []
    for proteome in config["proteomes"]:
        paths = snapshot_paths(proteome, release)
        if any(path.exists() for path in paths):
            raise RuntimeError(f"release {release} already has raw files for {proteome['slug']}")
        results.append(download_proteome(proteome, release))

    for proteome, result in zip(config["proteomes"], results):
        freeze_download(proteome, release, result)
        proteome["protein_count"] = result["record_count"]
        proteome["fasta_sha256"] = result["fasta_sha256"]
        proteome["metadata_sha256"] = result["metadata_sha256"]

    config["frozen_release"] = release
    config["uniprot_release_date"] = results[0]["release_date"]
    temporary = CONFIG_PATH.with_name(f".{CONFIG_PATH.name}.part")
    temporary.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, CONFIG_PATH)
    print(f"UPDATED configured workshop snapshot to UniProt {release}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update-release",
        metavar="YYYY_NN",
        help="explicitly freeze the named current UniProt release",
    )
    args = parser.parse_args()
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if args.update_release:
        update_release(config, args.update_release)
    else:
        use_configured_snapshot(config)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
