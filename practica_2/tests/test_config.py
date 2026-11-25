import tempfile
import unittest
from pathlib import Path
from src.config import load_config, ConfigError


class ConfigTests(unittest.TestCase):
    def test_valid_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.ini"
            path.write_text("""[Settings]
package_name = A
repo_url = https://example.com
test_mode = true
max_depth = 2
ascii_tree = true
filter_substring =
""", encoding="utf-8")
            self.assertEqual(load_config(path)["package_name"], "A")

    def test_missing_config(self):
        with self.assertRaises(ConfigError):
            load_config("file_that_does_not_exist.ini")


if __name__ == "__main__":
    unittest.main()
