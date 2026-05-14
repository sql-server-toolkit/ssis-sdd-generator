import json
from pathlib import Path
from typing import Any

from app.sdd.paths import safe_path_name


class JsonWriter:

    def __init__(self, output_folder: Path):
        self.output_folder = output_folder
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.packages_folder = self.output_folder / "packages"
        self.packages_folder.mkdir(parents=True, exist_ok=True)

    def write_package_json(self, package_data: dict[str, Any]) -> Path:
        output_file = self.packages_folder / f"{safe_path_name(package_data['package_name'], 'package')}.json"
        self._write_json(output_file, package_data)
        return output_file

    def write_project_json(self, project_data: dict[str, Any]) -> Path:
        output_file = self.output_folder / "project.json"
        self._write_json(output_file, project_data)
        return output_file

    def _write_json(self, output_file: Path, data: dict[str, Any]) -> None:
        output_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
