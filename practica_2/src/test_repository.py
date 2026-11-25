"""Чтение тестового репозитория из JSON."""
import json
from pathlib import Path


def load_test_repository(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Тестовый репозиторий не найден: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Тестовый граф должен быть JSON-объектом.")
    graph = {}
    for parent, children in data.items():
        if not isinstance(parent, str) or not isinstance(children, list):
            raise ValueError("Ожидается формат: имя пакета: список зависимостей.")
        graph[parent] = [str(child) for child in children]
        for child in children:
            graph.setdefault(str(child), [])
    return graph
