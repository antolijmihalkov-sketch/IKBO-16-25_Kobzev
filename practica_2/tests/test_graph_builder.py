import unittest
from src.graph_builder import build_graph_from_adjacency, print_ascii_tree


class GraphTests(unittest.TestCase):
    def test_simple_graph(self):
        graph = {"A": ["B"], "B": ["C"], "C": []}
        self.assertEqual(build_graph_from_adjacency(graph, "A", 2), graph)

    def test_depth(self):
        graph = {"A": ["B"], "B": ["C"], "C": ["D"], "D": []}
        result = build_graph_from_adjacency(graph, "A", 1)
        self.assertEqual(result["A"], ["B"])
        self.assertEqual(result["B"], [])
        self.assertNotIn("C", result)

    def test_cycle_terminates(self):
        graph = {"A": ["B"], "B": ["A"]}
        result = build_graph_from_adjacency(graph, "A", 5)
        self.assertIn("A", result["B"])
        self.assertIn("цикл", print_ascii_tree(result, "A"))


if __name__ == "__main__":
    unittest.main()
