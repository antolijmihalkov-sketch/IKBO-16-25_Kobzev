"""Минимальная обработка версий и диапазонов NuGet без сторонних библиотек."""
import re


def clean_version(value):
    """Извлекает нижнюю границу версии из типичных NuGet-диапазонов."""
    if not value:
        return None
    value = value.strip()
    if value.startswith("[") or value.startswith("("):
        match = re.search(r"[\[(]\s*([^,\])]+)", value)
        if match and match.group(1).strip():
            return match.group(1).strip()
        match = re.search(r",\s*([^\])]+)[\])]", value)
        if match and match.group(1).strip():
            return match.group(1).strip()
        return None
    return value


def version_key(version):
    """Ключ для сравнения обычных числовых версий."""
    parts = re.findall(r"\d+|[A-Za-z]+", version or "")
    return tuple((0, int(p)) if p.isdigit() else (1, p.lower()) for p in parts)


def choose_version(versions):
    """Выбирает последнюю стабильную версию из списка NuGet."""
    stable = [v for v in versions if "-" not in v]
    candidates = stable or list(versions)
    return max(candidates, key=version_key) if candidates else None
