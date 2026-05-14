from datetime import datetime
from pathlib import Path
from typing import Any

from app.sdd.paths import discover_ssis_project_name


class ProjectBuilder:

    def build_project_data(
        self,
        ssis_folder: Path,
        output_folder: Path,
        supported_files: list[Path],
        package_data: list[dict[str, Any]],
        generated_markdown_files: list[Path],
        generated_package_json_files: list[Path],
        skipped_files: list[Path],
        failed_files: list[Path],
    ) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "project": {
                "name": discover_ssis_project_name(ssis_folder),
                "ssis_folder": str(ssis_folder),
                "output_folder": str(output_folder),
            },
            "summary": {
                "supported_file_count": len(supported_files),
                "package_count": len(package_data),
                "generated_markdown_count": len(generated_markdown_files),
                "generated_package_json_count": len(generated_package_json_files),
                "skipped_file_count": len(skipped_files),
                "failed_file_count": len(failed_files),
            },
            "artifacts": {
                "supported_files": [str(file_path) for file_path in supported_files],
                "generated_markdown_files": [str(file_path) for file_path in generated_markdown_files],
                "generated_package_json_files": [
                    str(file_path) for file_path in generated_package_json_files
                ],
                "skipped_files": [str(file_path) for file_path in skipped_files],
                "failed_files": [str(file_path) for file_path in failed_files],
            },
            "packages": package_data,
        }
