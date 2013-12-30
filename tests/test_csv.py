from pathlib import Path
import unittest

from csv_profiler_lab.core import profile
from csv_profiler_lab.fixture_check import check


class CsvTests(unittest.TestCase):
    def test_quoted_fields_blanks_and_numeric_classification(self):
        result = profile('name,amount\n"A, B",0.10\nC,\nD,n/a\n')
        self.assertEqual(result["row_count"], 3)
        self.assertEqual(result["columns"][1], {"name": "amount", "nonempty": 2, "empty": 1, "numeric": 1, "distinct": 2, "max_length": 4})

    def test_duplicate_headers_and_bad_width_fail(self):
        for text in ("", "a, a\n", ",b\n", "a,b\n1,2,3\n", 'a,b\n"unfinished'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                profile(text)

    def test_custom_delimiter_and_empty_body(self):
        result = profile("a;b\n", delimiter=";")
        self.assertEqual(result["row_count"], 0)
        self.assertEqual(result["columns"][0]["max_length"], 0)
        with self.assertRaises(ValueError):
            profile("a,b", delimiter="xx")

    def test_all_generated_fixtures(self):
        self.assertGreaterEqual(check(Path(__file__).resolve().parents[1] / "fixtures" / "cases.jsonl", profile), 350)


if __name__ == "__main__":
    unittest.main()
