#!/usr/bin/env python3
"""Validate curated positive adhesin IDs against the frozen reference proteomes."""

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
CURATED_FILE = (
    REPOSITORY / "input" / "raw" / "labels"
    / "20260729-curated-positive-adhesin-set-KN.csv"
)
PROTEOMES = {
    "Saccharomyces cerevisiae S288C": {
        "proteome_id": "UP000002311",
        "path": REPOSITORY / "input" / "raw" / "proteomes"
        / "saccharomyces_cerevisiae_s288c"
        / "UP000002311-uniprot-2026_02.fasta",
    },
    "Candida albicans SC5314": {
        "proteome_id": "UP000000559",
        "path": REPOSITORY / "input" / "raw" / "proteomes"
        / "candida_albicans_sc5314"
        / "UP000000559-uniprot-2026_02.fasta",
    },
}
MAPPING_FILE = (
    REPOSITORY / "input" / "interim" / "curated-positive-adhesins"
    / "curated-positive-id-mapping.tsv"
)
REPORT_FILE = (
    REPOSITORY / "output" / "curated-positive-adhesins"
    / "id-validation-report.md"
)


def parse_uniprot_header(header: str) -> dict:
    """Extract identifiers from a standard UniProt FASTA header."""
    first_field, _, description_and_fields = header.partition(" ")
    parts = first_field.split("|")
    if len(parts) != 3 or parts[0] not in {"sp", "tr"}:
        raise ValueError(f"Unexpected UniProt FASTA header: {header}")

    gene_match = re.search(r"(?:^| )GN=([^ ]+)", description_and_fields)
    description = description_and_fields.split(" OS=", 1)[0]
    return {
        "uniprot_accession": parts[1],
        "uniprot_entry_name": parts[2],
        "gene_name": gene_match.group(1) if gene_match else "",
        "protein_description": description,
        "original_fasta_header": header,
    }


def read_proteome(species: str, proteome_id: str, path: Path) -> list[dict]:
    records = []
    with path.open(encoding="ascii") as handle:
        for line in handle:
            if line.startswith(">"):
                record = parse_uniprot_header(line[1:].rstrip())
                record["matched_species"] = species
                record["reference_proteome_id"] = proteome_id
                record["reference_fasta"] = path.name
                records.append(record)
    return records


def read_curated_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not {"ID", "Name"}.issubset(reader.fieldnames):
            raise ValueError(f"{path}: required columns are ID and Name")
        rows = list(reader)

    for row_number, row in enumerate(rows, 2):
        row["ID"] = row["ID"].strip()
        row["Name"] = row["Name"].strip()
        row["source_row"] = row_number
        if not row["ID"]:
            raise ValueError(f"{path}: blank ID at row {row_number}")
    return rows


def validate_ids(curated_rows: list[dict], proteome_records: list[dict]) -> list[dict]:
    by_accession = defaultdict(list)
    for record in proteome_records:
        by_accession[record["uniprot_accession"]].append(record)

    curated_id_counts = Counter(row["ID"] for row in curated_rows)
    results = []
    for row in curated_rows:
        matches = by_accession[row["ID"]]
        if len(matches) == 1:
            match = matches[0]
            match_status = "exact-unique"
            name_status = (
                "exact" if row["Name"] == match["uniprot_entry_name"] else "mismatch"
            )
        elif not matches:
            match = {}
            match_status = "unmatched"
            name_status = "not-checked"
        else:
            match = {}
            match_status = "ambiguous"
            name_status = "not-checked"

        results.append(
            {
                "source_file": CURATED_FILE.name,
                "source_row": row["source_row"],
                "curated_id": row["ID"],
                "curated_name": row["Name"],
                "curated_id_occurrences": curated_id_counts[row["ID"]],
                "match_status": match_status,
                "name_check": name_status,
                "matched_species": match.get("matched_species", ""),
                "reference_proteome_id": match.get("reference_proteome_id", ""),
                "uniprot_accession": match.get("uniprot_accession", ""),
                "uniprot_entry_name": match.get("uniprot_entry_name", ""),
                "gene_name": match.get("gene_name", ""),
                "protein_description": match.get("protein_description", ""),
                "reference_fasta": match.get("reference_fasta", ""),
            }
        )
    return results


def write_mapping(results: list[dict]) -> None:
    MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with MAPPING_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(results)


def write_report(results: list[dict]) -> None:
    match_counts = Counter(row["match_status"] for row in results)
    species_counts = Counter(
        row["matched_species"] for row in results if row["matched_species"]
    )
    duplicate_ids = sorted(
        {row["curated_id"] for row in results if row["curated_id_occurrences"] > 1}
    )
    name_mismatches = [row for row in results if row["name_check"] == "mismatch"]
    unresolved = [row for row in results if row["match_status"] != "exact-unique"]

    lines = [
        "# Curated positive adhesin ID validation",
        "",
        f"Source label table: `{CURATED_FILE.relative_to(REPOSITORY)}`",
        "",
        "Frozen reference proteomes:",
        "",
    ]
    for species, details in PROTEOMES.items():
        lines.append(
            f"- *{species}*: `{details['proteome_id']}`, UniProt release `2026_02`"
        )
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Curated rows: {len(results)}",
            f"- Exact unique accession matches: {match_counts['exact-unique']}",
            f"- Unmatched IDs: {match_counts['unmatched']}",
            f"- Ambiguous IDs: {match_counts['ambiguous']}",
            f"- Duplicate IDs in the curated table: {len(duplicate_ids)}",
            f"- Curated-name mismatches: {len(name_mismatches)}",
            "",
            "Matches by reference proteome:",
            "",
        ]
    )
    for species in PROTEOMES:
        lines.append(f"- *{species}*: {species_counts[species]}")

    lines.extend(["", "## Interpretation", ""])
    if not unresolved and not duplicate_ids and not name_mismatches:
        lines.append(
            "Every curated ID is present once in one reference proteome, and every "
            "curated `Name` agrees with the matched UniProt entry name. No obsolete "
            "or unresolved IDs are indicated by this frozen snapshot."
        )
    else:
        lines.append(
            "Rows requiring review are retained in the ID-mapping table with their "
            "match and name-check status."
        )

    lines.extend(
        [
            "",
            "The accession match determines resolution. The curated `Name` field is "
            "used only as an independent consistency check.",
            "",
            f"Detailed table: `{MAPPING_FILE.relative_to(REPOSITORY)}`",
            "",
        ]
    )
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    curated_rows = read_curated_rows(CURATED_FILE)
    proteome_records = []
    for species, details in PROTEOMES.items():
        proteome_records.extend(
            read_proteome(species, details["proteome_id"], details["path"])
        )
    results = validate_ids(curated_rows, proteome_records)
    write_mapping(results)
    write_report(results)

    counts = Counter(row["match_status"] for row in results)
    print(
        f"Validated {len(results)} curated IDs: "
        f"{counts['exact-unique']} exact unique, "
        f"{counts['unmatched']} unmatched, {counts['ambiguous']} ambiguous"
    )


if __name__ == "__main__":
    main()
