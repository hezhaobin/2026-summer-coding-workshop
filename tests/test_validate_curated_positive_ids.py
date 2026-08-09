import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "script" / "validate_curated_positive_ids.py"
SPEC = importlib.util.spec_from_file_location("validate_curated_positive_ids", SCRIPT)
validation = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validation)


class ValidateCuratedPositiveIdsTests(unittest.TestCase):
    def test_parse_uniprot_header(self):
        record = validation.parse_uniprot_header(
            "sp|P32768|FLO1_YEAST Flocculation protein FLO1 "
            "OS=Saccharomyces cerevisiae GN=FLO1 PE=1 SV=3"
        )
        self.assertEqual(record["uniprot_accession"], "P32768")
        self.assertEqual(record["uniprot_entry_name"], "FLO1_YEAST")
        self.assertEqual(record["gene_name"], "FLO1")
        self.assertEqual(record["protein_description"], "Flocculation protein FLO1")

    def test_validate_ids_uses_accession_and_checks_name(self):
        proteome_records = [
            {
                "uniprot_accession": "P32768",
                "uniprot_entry_name": "FLO1_YEAST",
                "gene_name": "FLO1",
                "protein_description": "Flocculation protein FLO1",
                "matched_species": "Saccharomyces cerevisiae S288C",
                "reference_proteome_id": "UP000002311",
                "reference_fasta": "reference.fasta",
            }
        ]
        curated_rows = [
            {"ID": "P32768", "Name": "WRONG_NAME", "source_row": 2},
            {"ID": "NOT_FOUND", "Name": "UNKNOWN", "source_row": 3},
        ]
        results = validation.validate_ids(curated_rows, proteome_records)
        self.assertEqual(results[0]["match_status"], "exact-unique")
        self.assertEqual(results[0]["name_check"], "mismatch")
        self.assertEqual(results[1]["match_status"], "unmatched")


if __name__ == "__main__":
    unittest.main()
