"""Простая SVG-визуализация графа средствами стандартной библиотеки."""
import html
import math


def render_svg(graph, output_path):
    nodes = sorted(set(graph) | {child for values in graph.values() for child in values})
    if not nodes:
        nodes = ["(пустой граф)"]
    width = 900
    row_height = 90
    height = max(150, 80 + len(nodes) * row_height)
    positions = {node: (width // 2, 50 + i * row_height) for i, node in enumerate(nodes)}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<defs><marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#475569"/></marker></defs>',
             '<rect width="100%" height="100%" fill="#ffffff"/>']
    for parent, children in graph.items():
        x1, y1 = positions[parent]
        for child in children:
            x2, y2 = positions[child]
            parts.append(f'<path d="M {x1} {y1+18} C {x1+100} {y1+35}, {x2+100} {y2-35}, {x2} {y2-18}" fill="none" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>')
    for node, (x, y) in positions.items():
        label = html.escape(node)
        parts.append(f'<rect x="{x-130}" y="{y-20}" width="260" height="40" rx="8" fill="#e0f2fe" stroke="#0284c7"/>')
        parts.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-family="Arial" font-size="14" fill="#0f172a">{label}</text>')
    parts.append("</svg>")
    output_path = str(output_path)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(parts))
    return output_path
