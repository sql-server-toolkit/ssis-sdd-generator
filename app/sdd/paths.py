import re
from datetime import datetime
from pathlib import Path


def safe_path_name(value: str, fallback: str = "ssis_project") -> str:
    path_name = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    return path_name or fallback


def build_run_output_folder(output_folder: Path, ssis_folder: Path) -> Path:
    project_name = safe_path_name(discover_ssis_project_name(ssis_folder))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return output_folder / f"{project_name}_{timestamp}"


def discover_ssis_project_name(ssis_folder: Path) -> str:
    for extension in ("*.dtproj", "*.sln", "*.ispac"):
        candidates = sorted(ssis_folder.glob(extension))
        if candidates:
            return candidates[0].stem

    for extension in ("*.dtproj", "*.sln", "*.ispac"):
        candidates = sorted(ssis_folder.rglob(extension))
        if candidates:
            return candidates[0].stem

    return ssis_folder.name
