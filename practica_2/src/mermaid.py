"""Генерация диаграммы Mermaid."""
import re


def _safe_id(name):
    return "N_" + re.sub(r"[^A-Za-z0-9_]", "_", name)


def generate_mermaid(graph, root=None):
    lines = ["flowchart TD"]
    nodes = set(graph)
    for children in graph.values():
        nodes.update(children)
    for node in sorted(nodes):
        safe = _safe_id(node)
        label = node.replace('"', "'")
        lines.append(f'    {safe}["{label}"]')
    for parent, children in graph.items():
        for child in children:
            lines.append(f"    {_safe_id(parent)} --> {_safe_id(child)}")
    return "\n".join(lines) + "\n"
