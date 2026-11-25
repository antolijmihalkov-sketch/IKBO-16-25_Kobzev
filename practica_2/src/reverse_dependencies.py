"""Поиск обратных зависимостей в построенном графе."""


def find_reverse_dependencies(graph, package):
    """Возвращает пакеты, у которых есть ребро к package."""
    result = []
    for parent, children in graph.items():
        if package in children:
            result.append(parent)
    return sorted(result)
