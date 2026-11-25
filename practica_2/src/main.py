"""CLI-инструмент визуализации графа зависимостей NuGet."""
import argparse
from pathlib import Path
from .config import load_config, ConfigError
from .npm_client import NuGetClient
from .test_repository import load_test_repository
from .graph_builder import GraphBuilder, build_graph_from_adjacency, print_ascii_tree
from .reverse_dependencies import find_reverse_dependencies
from .generate_diagrams import save_diagrams


def main():
    parser = argparse.ArgumentParser(description="Визуализация графа зависимостей NuGet")
    parser.add_argument("--config", default="config.ini", help="Путь к INI-конфигурации")
    args = parser.parse_args()
    try:
        config = load_config(args.config)
        print("--- Конфигурация ---")
        for key, value in config.items():
            print(f"{key} = {value}")

        root = config["package_name"]
        if config["test_mode"]:
            adjacency = load_test_repository(config["test_repository"])
            graph = build_graph_from_adjacency(
                adjacency, root, config["max_depth"], config["filter_substring"]
            )
        else:
            client = NuGetClient(config["repo_url"])
            cache = {}
            def provider(package):
                if package not in cache:
                    cache[package] = client.get_dependencies(package)
                return cache[package]
            graph = GraphBuilder(provider, config["max_depth"], config["filter_substring"]).build(root)
            print("\n--- Прямые зависимости ---")
            for dependency in provider(root):
                print(f"- {dependency['name']} ({dependency.get('version') or 'версия не указана'})")

        if not graph:
            print("Граф пуст: проверьте имя пакета, фильтр и источник данных.")
            return

        print("\n--- Граф зависимостей ---")
        for package, dependencies in graph.items():
            print(f"{package} -> {', '.join(dependencies) if dependencies else '(нет зависимостей)'}")

        if config["ascii_tree"]:
            print("\n--- ASCII-дерево ---")
            print(print_ascii_tree(graph, root))

        if config["reverse_dependencies"]:
            print(f"\n--- Обратные зависимости для {root} ---")
            reverse = find_reverse_dependencies(graph, root)
            print("\n".join(reverse) if reverse else "Обратные зависимости не найдены.")

        mermaid_path, svg_path = save_diagrams(graph, root.replace("/", "_"), config["output_dir"])
        print(f"\nMermaid сохранён: {mermaid_path}")
        print(f"SVG сохранён: {svg_path}")
        print("Откройте SVG-файл в браузере для просмотра изображения.")
    except (ConfigError, FileNotFoundError, ValueError, OSError, Exception) as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
