"""Генерация Mermaid и SVG для графа."""
from pathlib import Path
from .mermaid import generate_mermaid
from .svg_renderer import render_svg


def save_diagrams(graph, name, output_dir="diagrams"):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    mermaid_path = output / f"{name}.mmd"
    svg_path = output / f"{name}.svg"
    mermaid_path.write_text(generate_mermaid(graph), encoding="utf-8")
    render_svg(graph, svg_path)
    return mermaid_path, svg_path
