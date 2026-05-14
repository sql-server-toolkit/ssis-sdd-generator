from pathlib import Path
import re

from app.sdd.spec_builder import SpecBuilder


class MarkdownWriter:

    def __init__(self, output_folder: Path):
        self.output_folder = output_folder
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def write_package_spec(self, package_data: dict) -> Path:
        builder = SpecBuilder()

        markdown_content = builder.build_package_spec(package_data)

        output_file = self.output_folder / f"{self._safe_filename(package_data['package_name'])}.md"

        output_file.write_text(markdown_content, encoding="utf-8")

        return output_file

    def write_project_index(self, generated_files: list[Path]) -> Path | None:
        if len(generated_files) < 2:
            return None

        rows = ["# SSIS SDD Index", "", "| Package Spec |", "| --- |"]
        for file_path in sorted(generated_files):
            rows.append(f"| [{file_path.stem}]({file_path.name}) |")

        output_file = self.output_folder / "index.md"
        output_file.write_text("\n".join(rows) + "\n", encoding="utf-8")

        return output_file

    def _safe_filename(self, value: str) -> str:
        filename = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
        return filename or "package"
