"""Загрузка и проверка настроек приложения."""
import configparser
from pathlib import Path


class ConfigError(ValueError):
    """Ошибка конфигурации."""


def load_config(path="config.ini"):
    path = Path(path)
    if not path.is_file():
        raise ConfigError(f"Файл конфигурации не найден: {path}")

    parser = configparser.ConfigParser()
    try:
        read = parser.read(path, encoding="utf-8")
        if not read or "Settings" not in parser:
            raise ConfigError("В конфигурации отсутствует секция [Settings].")
        section = parser["Settings"]
        config = {
            "package_name": section.get("package_name", "").strip(),
            "repo_url": section.get("repo_url", "").strip().rstrip("/"),
            "test_mode": section.getboolean("test_mode"),
            "test_repository": section.get("test_repository", "test_data/simple.json").strip(),
            "ascii_tree": section.getboolean("ascii_tree"),
            "max_depth": section.getint("max_depth"),
            "filter_substring": section.get("filter_substring", "").strip(),
            "reverse_dependencies": section.getboolean("reverse_dependencies", fallback=False),
            "output_dir": section.get("output_dir", "diagrams").strip(),
        }
    except (ValueError, configparser.Error) as exc:
        raise ConfigError(f"Ошибка в настройках: {exc}") from exc

    if not config["package_name"]:
        raise ConfigError("Параметр package_name не должен быть пустым.")
    if not config["test_mode"] and not config["repo_url"].startswith(("https://", "http://")):
        raise ConfigError("repo_url должен быть корректным HTTP(S)-адресом.")
    if config["max_depth"] < 0:
        raise ConfigError("max_depth не может быть отрицательным.")
    if not config["output_dir"]:
        raise ConfigError("output_dir не должен быть пустым.")
    return config
