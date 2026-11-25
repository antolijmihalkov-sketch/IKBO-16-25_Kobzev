import unittest
from src.reverse_dependencies import find_reverse_dependencies


class ReverseTests(unittest.TestCase):
    def test_reverse(self):
        graph = {"A": ["C"], "B": ["C"], "C": []}
        self.assertEqual(find_reverse_dependencies(graph, "C"), ["A", "B"])


if __name__ == "__main__":
    unittest.main()
