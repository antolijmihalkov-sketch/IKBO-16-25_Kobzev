import tempfile
import unittest
from pathlib import Path
from src.svg_renderer import render_svg


class SvgTests(unittest.TestCase):
    def test_svg_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graph.svg"
            render_svg({"A": ["B"], "B": []}, path)
            self.assertTrue(path.exists())
            self.assertIn("<svg", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
