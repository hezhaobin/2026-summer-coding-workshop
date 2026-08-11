import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "script" / "sequence_features.py"
SPEC = importlib.util.spec_from_file_location("sequence_features", SCRIPT)
FEATURES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FEATURES)


class SequenceFeatureTests(unittest.TestCase):
    def test_count_occurrences(self):
        self.assertEqual(FEATURES.count_occurrences("BANANA", "A"), 3)
        self.assertEqual(FEATURES.count_occurrences("MASTT", "S"), 1)
        self.assertEqual(FEATURES.count_occurrences("", "S"), 0)

    def test_count_occurrences_rejects_more_than_one_character(self):
        with self.assertRaisesRegex(ValueError, "exactly one character"):
            FEATURES.count_occurrences("MASTT", "ST")

    def test_st_frequency(self):
        self.assertEqual(FEATURES.st_frequency("MASTT"), 3 / 5)
        self.assertEqual(FEATURES.st_frequency("AAAA"), 0)
        self.assertIsNone(FEATURES.st_frequency(""))

    def test_sliding_st_frequencies_returns_ordered_list(self):
        self.assertEqual(
            FEATURES.sliding_st_frequencies("MASTTA", 4),
            [2 / 4, 3 / 4, 3 / 4],
        )

    def test_sliding_st_frequencies_handles_short_and_empty_sequences(self):
        self.assertEqual(FEATURES.sliding_st_frequencies("ST", 50), [1])
        self.assertEqual(FEATURES.sliding_st_frequencies("", 50), [])

    def test_sliding_st_frequencies_rejects_invalid_window(self):
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            FEATURES.sliding_st_frequencies("MASTT", 0)

    def test_max_st_frequency_window(self):
        self.assertEqual(FEATURES.max_st_frequency_window("MASTTA", 4), 3 / 4)
        self.assertIsNone(FEATURES.max_st_frequency_window("", 50))


if __name__ == "__main__":
    unittest.main()
