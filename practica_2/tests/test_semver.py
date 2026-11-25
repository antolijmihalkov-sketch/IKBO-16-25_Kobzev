import unittest
from src.semver import clean_version, version_key


class SemverTests(unittest.TestCase):
    def test_plain_version(self):
        self.assertEqual(clean_version("1.2.3"), "1.2.3")

    def test_open_range(self):
        self.assertEqual(clean_version("(, 2.0.0]"), "2.0.0")

    def test_numeric_order(self):
        self.assertGreater(version_key("1.10.0"), version_key("1.2.0"))


if __name__ == "__main__":
    unittest.main()
