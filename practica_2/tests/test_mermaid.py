import unittest
from src.mermaid import generate_mermaid


class MermaidTests(unittest.TestCase):
    def test_edges(self):
        result = generate_mermaid({"A": ["B"], "B": []})
        self.assertIn("flowchart TD", result)
        self.assertIn("N_A --> N_B", result)


if __name__ == "__main__":
    unittest.main()
