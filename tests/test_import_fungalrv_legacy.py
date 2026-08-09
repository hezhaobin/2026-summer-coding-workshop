import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "script" / "import_fungalrv_legacy.py"
SPEC = importlib.util.spec_from_file_location("import_fungalrv_legacy", SCRIPT)
legacy = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(legacy)


class ImportFungalRVLegacyTests(unittest.TestCase):
    def test_read_fasta(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tiny.fasta"
            path.write_text(">one\nMST\n>two description\nAAAA\n", encoding="ascii")
            self.assertEqual(
                legacy.read_fasta(path),
                [("one", "MST"), ("two description", "AAAA")],
            )

    def test_identifiers_from_gi_header(self):
        header = "gi|46439831|gb|EAK99144.1| agglutinin-like protein"
        primary, identifiers = legacy.identifiers_from_header(header)
        self.assertEqual(primary, "46439831")
        self.assertIn("EAK99144.1", identifiers)
        self.assertIn("EAK99144", identifiers)

    def test_identifiers_from_uniprot_header(self):
        primary, identifiers = legacy.identifiers_from_header(
            "tr|Q6FNG2|Q6FNG2_CANGA Similarity"
        )
        self.assertEqual(primary, "Q6FNG2")
        self.assertIn("Q6FNG2", identifiers)


if __name__ == "__main__":
    unittest.main()
