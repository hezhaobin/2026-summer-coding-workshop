import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "script" / "download_proteomes.py"
SPEC = importlib.util.spec_from_file_location("download_proteomes", SCRIPT_PATH)
download_proteomes = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(download_proteomes)


class DownloadProteomesTests(unittest.TestCase):
    def test_count_fasta_records(self):
        fasta = b">sp|P00001|ONE\nMSTT\n>tr|A0A000|TWO\nAAA\n"
        self.assertEqual(download_proteomes.count_fasta_records(fasta), 2)

    def test_count_fasta_records_rejects_non_fasta_text(self):
        with self.assertRaisesRegex(RuntimeError, "contains no records"):
            download_proteomes.count_fasta_records(b"not a FASTA file\n")

    def test_validate_metadata_checks_scientific_identity(self):
        proteome = {
            "proteome_accession": "UP000000001",
            "expected_taxon_id": 123,
            "expected_assembly_accession": "GCA_000000001.1",
            "strain": "Example strain",
        }
        metadata = {
            "id": "UP000000001",
            "proteomeType": "Reference proteome",
            "taxonomy": {"taxonId": 123},
            "genomeAssembly": {"assemblyId": "GCA_000000001.1"},
            "strain": "Example strain / collection name",
        }
        download_proteomes.validate_metadata(metadata, proteome)

        metadata["taxonomy"]["taxonId"] = 999
        with self.assertRaisesRegex(RuntimeError, "taxon ID"):
            download_proteomes.validate_metadata(metadata, proteome)


if __name__ == "__main__":
    unittest.main()
