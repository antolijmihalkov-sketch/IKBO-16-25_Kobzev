import unittest
from src.semver import clean_version, choose_version


class NuGetVersionTests(unittest.TestCase):
    def test_range(self):
        self.assertEqual(clean_version("[1.2.0, 2.0.0)"), "1.2.0")

    def test_latest_stable(self):
        self.assertEqual(choose_version(["1.0.0", "2.0.0-beta", "1.9.0"]), "1.9.0")


if __name__ == "__main__":
    unittest.main()
