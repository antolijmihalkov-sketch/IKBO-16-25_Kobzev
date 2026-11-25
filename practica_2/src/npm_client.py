"""Клиент NuGet V3 Flat Container. Имя файла оставлено по шаблону проекта."""
import json
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from .semver import choose_version, clean_version


class NuGetClient:
    def __init__(self, repo_url="https://api.nuget.org/v3-flatcontainer", timeout=15):
        self.repo_url = repo_url.rstrip("/")
        self.timeout = timeout

    def _get(self, url):
        request = urllib.request.Request(url, headers={"User-Agent": "DependencyGraphStudentProject/1.0"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return response.read()

    def get_versions(self, package):
        url = f"{self.repo_url}/{package.lower()}/index.json"
        data = json.loads(self._get(url).decode("utf-8"))
        return data.get("versions", [])

    def get_latest_version(self, package):
        return choose_version(self.get_versions(package))

    def get_dependencies(self, package, version=None):
        """Возвращает прямые зависимости пакета из его .nuspec."""
        version = version or self.get_latest_version(package)
        if not version:
            return []
        url = f"{self.repo_url}/{package.lower()}/{version.lower()}/{package.lower()}.nuspec"
        root = ET.fromstring(self._get(url))
        dependencies = []
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1] == "dependency":
                dep_id = element.attrib.get("id")
                dep_version = clean_version(element.attrib.get("version", ""))
                if dep_id:
                    dependencies.append({"name": dep_id, "version": dep_version})
        # Один и тот же пакет может встречаться в нескольких target framework groups.
        unique = {}
        for item in dependencies:
            unique.setdefault(item["name"].lower(), item)
        return list(unique.values())
