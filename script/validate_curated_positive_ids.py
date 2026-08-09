#!/usr/bin/env python3
"""Check curated positive IDs against the two frozen reference proteomes."""

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURATED_FILE = ROOT / "input/raw/labels/20260729-curated-positive-adhesin-set-KN.csv"
PROTEOMES = {
    "S. cerevisiae": ROOT / "input/raw/proteomes/saccharomyces_cerevisiae_s288c"
    / "UP000002311-uniprot-2026_02.fasta",
    "C. albicans": ROOT / "input/raw/proteomes/candida_albicans_sc5314"
    / "UP000000559-uniprot-2026_02.fasta",
}
OUTPUT_FILE = ROOT / "input/interim/curated-positive-adhesins"
OUTPUT_FILE = OUTPUT_FILE / "curated-positive-id-matches.tsv"


def read_uniprot_ids(fasta_file):
    ids = set()
    with fasta_file.open() as handle:
        for line in handle:
            if line.startswith(">"):
                ids.add(line.split("|")[1])
    return ids


proteome_ids = {
    species: read_uniprot_ids(path) for species, path in PROTEOMES.items()
}

with CURATED_FILE.open(newline="", encoding="utf-8-sig") as handle:
    curated_rows = list(csv.DictReader(handle))

id_counts = Counter(row["ID"] for row in curated_rows)
results = []
for row in curated_rows:
    found_in = [species for species, ids in proteome_ids.items() if row["ID"] in ids]
    if len(found_in) == 1:
        status = "matched"
    elif len(found_in) == 0:
        status = "unmatched"
    else:
        status = "ambiguous"
    results.append(
        {
            "curated_id": row["ID"],
            "species": found_in[0] if len(found_in) == 1 else "",
            "match_status": status,
            "duplicate_in_curated_set": "yes" if id_counts[row["ID"]] > 1 else "no",
        }
    )

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT_FILE.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=results[0], delimiter="\t")
    writer.writeheader()
    writer.writerows(results)

status_counts = Counter(row["match_status"] for row in results)
species_counts = Counter(row["species"] for row in results if row["species"])
print(f"Checked {len(results)} curated IDs")
for species in PROTEOMES:
    print(f"{species}: {species_counts[species]} matched")
print(f"Unmatched: {status_counts['unmatched']}")
print(f"Ambiguous: {status_counts['ambiguous']}")
print(f"Duplicated curated IDs: {sum(count > 1 for count in id_counts.values())}")
