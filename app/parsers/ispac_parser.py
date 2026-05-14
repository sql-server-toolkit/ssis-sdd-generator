from pathlib import Path
from zipfile import BadZipFile, ZipFile


class IspacParser:

    def inspect(self, file_path: Path) -> dict:
        try:
            with ZipFile(file_path) as archive:
                entries = archive.namelist()
        except BadZipFile as exc:
            raise ValueError(f"Invalid .ispac file: {file_path}") from exc

        return {
            "file_path": str(file_path),
            "packages": sorted(entry for entry in entries if entry.lower().endswith(".dtsx")),
            "connections": sorted(
                entry for entry in entries if entry.lower().endswith(".conmgr")
            ),
            "project_parameters": sorted(
                entry for entry in entries if "params" in entry.lower()
            ),
            "manifest_files": sorted(
                entry
                for entry in entries
                if "manifest" in entry.lower() or entry.lower().endswith(".manifest")
            ),
            "entries": entries,
        }
