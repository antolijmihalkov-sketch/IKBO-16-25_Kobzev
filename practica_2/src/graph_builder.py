"""Построение графа зависимостей рекурсивным DFS."""
class GraphBuilder:
    def __init__(self, dependency_provider, max_depth=3, filter_substring=""):
        self.dependency_provider = dependency_provider
        self.max_depth = max_depth
        self.filter_substring = filter_substring.lower()
        self.graph = {}
        self.expanded_depth = {}
        self.active = set()

    def build(self, root):
        self.graph = {}
        self.expanded_depth = {}
        self.active = set()
        self._dfs(root, 0)
        return self.graph

    def _dfs(self, node, depth):
        if depth > self.max_depth or self._filtered(node):
            return
        self.graph.setdefault(node, [])
        # Повторно раскрываем узел, если нашли более короткий путь к нему.
        previous_depth = self.expanded_depth.get(node)
        if previous_depth is not None and previous_depth <= depth:
            return
        self.expanded_depth[node] = depth
        if depth == self.max_depth:
            return
        self.active.add(node)
        children = self.dependency_provider(node)
        names = [item["name"] if isinstance(item, dict) else str(item) for item in children]
        for child in names:
            if self._filtered(child):
                continue
            if child not in self.graph[node]:
                self.graph[node].append(child)
            self.graph.setdefault(child, [])
            # Ребро цикла сохраняем, но не уходим по нему рекурсивно.
            if child not in self.active:
                self._dfs(child, depth + 1)
        self.active.discard(node)

    def _filtered(self, package):
        return bool(self.filter_substring and self.filter_substring in package.lower())

def build_graph_from_adjacency(adjacency, root, max_depth=3, filter_substring=""):
    """DFS для заранее загруженного тестового графа."""
    builder = GraphBuilder(lambda node: adjacency.get(node, []), max_depth, filter_substring)
    return builder.build(root)


def print_ascii_tree(graph, root):
    """Печать дерева с защитой от циклов и повторных узлов."""
    lines = [str(root)]
    def visit(node, prefix, path):
        children = graph.get(node, [])
        for index, child in enumerate(children):
            last = index == len(children) - 1
            connector = "└── " if last else "├── "
            lines.append(prefix + connector + child)
            if child in path:
                lines.append(prefix + ("    " if last else "│   ") + "↳ цикл")
            else:
                visit(child, prefix + ("    " if last else "│   "), path | {child})
    visit(root, "", {root})
    return "\n".join(lines)
