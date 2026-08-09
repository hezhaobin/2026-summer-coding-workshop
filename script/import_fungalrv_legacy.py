#!/usr/bin/env python3
"""Import the FungalRV 2011 legacy sequence sets and compare KN identifiers."""

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
LABEL_DIR = REPOSITORY / "input" / "raw" / "labels" / "fungalrv_2011"
KN_DIR = REPOSITORY / "input" / "raw" / "predictors" / "fungalrv_2011" / "kn_2025"
INTERIM_DIR = REPOSITORY / "input" / "interim" / "fungalrv_2011"
REPORT_DIR = REPOSITORY / "output" / "fungalrv_2011"

SEQUENCE_FILES = {
    "positive": LABEL_DIR / "FungalRV-positive-dataset-101seq.fasta",
    "negative": LABEL_DIR / "FungalRV-negative-dataset-2644seq.fasta",
}
EXPECTED_COUNTS = {"positive": 101, "negative": 2644}
STANDARD_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def read_fasta(path: Path) -> list[tuple[str, str]]:
    records = []
    header = None
    sequence_lines = []
    for line_number, raw_line in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                records.append((header, "".join(sequence_lines)))
            header = line[1:]
            sequence_lines = []
        elif header is None:
            raise ValueError(f"{path}: sequence before first header at line {line_number}")
        else:
            sequence_lines.append(line)
    if header is not None:
        records.append((header, "".join(sequence_lines)))

    for header, sequence in records:
        if not sequence:
            raise ValueError(f"{path}: empty sequence for {header}")
        unexpected = set(sequence) - STANDARD_AMINO_ACIDS
        if unexpected:
            raise ValueError(f"{path}: unexpected residues {sorted(unexpected)}")
    return records


def identifiers_from_header(header: str) -> tuple[str, set[str]]:
    """Return a primary legacy ID and conservative exact-match alternatives."""
    parts = [part.strip() for part in header.split("|")]
    if header.startswith("gi|") and len(parts) >= 4:
        primary = parts[1]
    elif header.startswith(("sp|", "tr|")) and len(parts) >= 2:
        primary = parts[1]
    else:
        primary = parts[0].split()[0]

    identifiers = {primary}
    for part in parts:
        token = part.split()[0] if part else ""
        if re.fullmatch(r"[A-Za-z0-9_.-]+", token) and token.lower() not in {
            "gi",
            "gb",
            "ref",
            "sp",
            "tr",
            "emb",
            "dbj",
            "pir",
            "gnl",
        }:
            identifiers.add(token)
            identifiers.add(re.sub(r"\.\d+$", "", token))
    return primary, identifiers


def load_sequences() -> list[dict]:
    records = []
    for label in ("positive", "negative"):
        fasta_records = read_fasta(SEQUENCE_FILES[label])
        if len(fasta_records) != EXPECTED_COUNTS[label]:
            raise ValueError(
                f"{SEQUENCE_FILES[label]}: found {len(fasta_records)} records; "
                f"expected {EXPECTED_COUNTS[label]}"
            )
        for number, (header, sequence) in enumerate(fasta_records, 1):
            source_id, candidate_ids = identifiers_from_header(header)
            records.append(
                {
                    "stable_id": f"fungalrv2011_{label[:3]}_{number:04d}",
                    "legacy_source": "fungalrv_2011",
                    "legacy_label": label,
                    "source_file": SEQUENCE_FILES[label].name,
                    "source_record_number": number,
                    "original_header": header,
                    "source_id": source_id,
                    "protein_length": len(sequence),
                    "sequence": sequence,
                    "candidate_ids": candidate_ids,
                }
            )
    return records


def load_kn_rows() -> list[dict]:
    rows = []
    for path in sorted(KN_DIR.glob("*.csv")):
        label = "positive" if path.name.startswith("positive-") else "negative"
        with path.open(newline="", encoding="utf-8-sig") as handle:
            table = list(csv.DictReader(handle))
        if not table:
            continue
        id_column = "Protein ID" if "Protein ID" in table[0] else "ID"
        if id_column not in table[0]:
            raise ValueError(f"{path}: no Protein ID or ID column")
        for number, row in enumerate(table, 1):
            rows.append(
                {
                    "legacy_label": label,
                    "kn_file": path.name,
                    "kn_row_number": number,
                    "kn_id": row[id_column].strip(),
                }
            )
    return rows


def write_normalized_fasta(records: list[dict]) -> None:
    path = INTERIM_DIR / "normalized-sequences.fasta"
    with path.open("w", encoding="ascii") as handle:
        for record in records:
            handle.write(
                f">{record['stable_id']} legacy_source={record['legacy_source']} "
                f"legacy_label={record['legacy_label']} source_id={record['source_id']}\n"
            )
            sequence = record["sequence"]
            for start in range(0, len(sequence), 70):
                handle.write(sequence[start : start + 70] + "\n")


def write_header_info(records: list[dict]) -> None:
    fields = [
        "stable_id",
        "legacy_source",
        "legacy_label",
        "source_file",
        "source_record_number",
        "original_header",
        "source_id",
        "protein_length",
    ]
    with (INTERIM_DIR / "sequence-header-info-extract.tsv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for record in records:
            writer.writerow({field: record[field] for field in fields})


def match_kn_rows(records: list[dict], kn_rows: list[dict]) -> tuple[list[dict], dict]:
    candidate_map = defaultdict(list)
    for record in records:
        for identifier in record["candidate_ids"]:
            candidate_map[(record["legacy_label"], identifier)].append(record)

    match_rows = []
    matched_stable_ids = set()
    matched_kn_rows = 0
    for kn_row in kn_rows:
        matches = candidate_map.get((kn_row["legacy_label"], kn_row["kn_id"]), [])
        if matches:
            matched_kn_rows += 1
            status = "direct_id_match" if len(matches) == 1 else "ambiguous_id_match"
            for record in matches:
                matched_stable_ids.add(record["stable_id"])
                match_rows.append(
                    {
                        "legacy_label": record["legacy_label"],
                        "stable_id": record["stable_id"],
                        "source_id": record["source_id"],
                        **kn_row,
                        "match_status": status,
                    }
                )
        else:
            match_rows.append(
                {
                    "legacy_label": kn_row["legacy_label"],
                    "stable_id": "",
                    "source_id": "",
                    **kn_row,
                    "match_status": "kn_unmatched",
                }
            )

    for record in records:
        if record["stable_id"] not in matched_stable_ids:
            match_rows.append(
                {
                    "legacy_label": record["legacy_label"],
                    "stable_id": record["stable_id"],
                    "source_id": record["source_id"],
                    "kn_file": "",
                    "kn_row_number": "",
                    "kn_id": "",
                    "match_status": "fasta_unmatched",
                }
            )

    summary = {
        "matched_stable_ids": len(matched_stable_ids),
        "unmatched_fasta_records": len(records) - len(matched_stable_ids),
        "matched_kn_rows": matched_kn_rows,
        "unmatched_kn_rows": len(kn_rows) - matched_kn_rows,
        "matched_sequences_by_label": Counter(
            record["legacy_label"]
            for record in records
            if record["stable_id"] in matched_stable_ids
        ),
    }
    return match_rows, summary


def write_matches(match_rows: list[dict]) -> None:
    fields = [
        "legacy_label",
        "stable_id",
        "source_id",
        "kn_file",
        "kn_row_number",
        "kn_id",
        "match_status",
    ]
    with (INTERIM_DIR / "kn-source-file-matches.tsv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(match_rows)


def write_report(records: list[dict], kn_rows: list[dict], summary: dict) -> None:
    label_counts = Counter(record["legacy_label"] for record in records)
    kn_file_counts = Counter(row["kn_file"] for row in kn_rows)
    duplicate_kn_rows = sum(
        count - 1
        for count in Counter(
            (row["legacy_label"], row["kn_file"], row["kn_id"]) for row in kn_rows
        ).values()
        if count > 1
    )
    files_by_kn_id = defaultdict(set)
    for row in kn_rows:
        files_by_kn_id[(row["legacy_label"], row["kn_id"])].add(row["kn_file"])
    ids_in_multiple_files = sum(len(files) > 1 for files in files_by_kn_id.values())
    lines = [
        "# FungalRV 2011 legacy import validation",
        "",
        "## Sequence import",
        "",
        f"- Positive FASTA records: {label_counts['positive']}",
        f"- Negative FASTA records: {label_counts['negative']}",
        "- Empty sequences: 0",
        "- Unexpected amino-acid characters: 0",
        "",
        "## Brief KN identifier comparison",
        "",
    ]
    for filename, count in sorted(kn_file_counts.items()):
        lines.append(f"- `{filename}`: {count} rows")
    lines.extend(
        [
            f"- Duplicate KN ID rows within the same file beyond the first: {duplicate_kn_rows}",
            f"- KN IDs present in more than one source file: {ids_in_multiple_files}",
            f"- FASTA records with at least one direct identifier match: {summary['matched_stable_ids']}",
            f"- FASTA records without a direct identifier match: {summary['unmatched_fasta_records']}",
            f"- KN rows with a direct identifier match: {summary['matched_kn_rows']}",
            f"- KN rows without a direct identifier match: {summary['unmatched_kn_rows']}",
            f"- Positive FASTA records matched directly: {summary['matched_sequences_by_label']['positive']} of {label_counts['positive']}",
            f"- Negative FASTA records matched directly: {summary['matched_sequences_by_label']['negative']} of {label_counts['negative']}",
            "",
            "This is intentionally a shallow identifier comparison. The KN files contain updated,",
            "subsetted, and duplicate identifiers, so these source-provided features are not treated",
            "as authoritative. Predictor and sequence-derived features will be recalculated from the",
            "normalized FASTA sequences for consistent downstream analysis.",
            "",
        ]
    )
    (REPORT_DIR / "validation-report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    records = load_sequences()
    kn_rows = load_kn_rows()
    write_normalized_fasta(records)
    write_header_info(records)
    match_rows, summary = match_kn_rows(records, kn_rows)
    write_matches(match_rows)
    write_report(records, kn_rows, summary)
    print(f"Imported {len(records)} legacy sequences")
    print(f"Direct KN identifier matches for {summary['matched_stable_ids']} sequences")


if __name__ == "__main__":
    main()
