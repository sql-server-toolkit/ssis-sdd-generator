from pathlib import Path

import argparse
import sys

from loguru import logger

from app import config
from app.parsers.dtsx_parser import DtsxParser
from app.sdd.markdown_writer import MarkdownWriter

SUPPORTED_EXTENSIONS = {".dtsx", ".conmgr", ".ispac"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate SDD Markdown files from SSIS project artifacts."
    )
    parser.add_argument(
        "--project-folder",
        type=Path,
        default=config.INPUT_FOLDER,
        help="Folder containing SSIS files. Defaults to INPUT_FOLDER or ./input.",
    )
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=config.OUTPUT_FOLDER,
        help="Folder where Markdown files will be generated. Defaults to OUTPUT_FOLDER or ./output.",
    )
    parser.add_argument(
        "--log-level",
        default=config.LOG_LEVEL,
        help="Logging level. Defaults to LOG_LEVEL or INFO.",
    )
    return parser.parse_args()


def configure_logging(log_level: str) -> None:
    logger.remove()
    logger.add(sys.stderr, level=log_level.upper(), format="{level}: {message}")


def validate_project_folder(project_folder: Path) -> list[Path]:
    if not project_folder.exists():
        raise FileNotFoundError(f"Input folder does not exist: {project_folder}")

    if not project_folder.is_dir():
        raise NotADirectoryError(f"Input path is not a folder: {project_folder}")

    supported_files = [
        file_path
        for file_path in project_folder.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not supported_files:
        found_extensions = sorted(
            {
                file_path.suffix.lower() or "<no extension>"
                for file_path in project_folder.rglob("*")
                if file_path.is_file() and file_path.name != ".gitkeep"
            }
        )
        extension_message = (
            f" Found extensions: {', '.join(found_extensions)}."
            if found_extensions
            else ""
        )
        raise ValueError(
            "Input folder does not contain supported SSIS files "
            "(.dtsx, .conmgr, .ispac)."
            f"{extension_message}"
        )

    return supported_files


def run(project_folder: Path, output_folder: Path) -> int:
    supported_files = validate_project_folder(project_folder)
    dtsx_files = sorted(
        file_path for file_path in supported_files if file_path.suffix.lower() == ".dtsx"
    )
    pending_files = sorted(set(supported_files) - set(dtsx_files))

    parser = DtsxParser()
    writer = MarkdownWriter(output_folder)

    generated_files = []
    failed_files = []

    for file_path in pending_files:
        logger.warning("Skipping non-DTSX artifact for Markdown generation: {}", file_path)

    if not dtsx_files:
        raise ValueError(
            "No .dtsx files were found. .conmgr and .ispac detection exists, "
            "but Markdown generation is currently based on DTSX packages."
        )

    for dtsx_file in dtsx_files:
        try:
            logger.info("Parsing package: {}", dtsx_file)
            package_data = parser.parse(dtsx_file)
            output_file = writer.write_package_spec(package_data)
            generated_files.append(output_file)
            logger.info("Generated spec: {}", output_file)
        except Exception as exc:
            failed_files.append(dtsx_file)
            logger.error("Failed to process {}: {}", dtsx_file, exc)

    index_file = writer.write_project_index(generated_files)
    if index_file:
        logger.info("Generated project index: {}", index_file)

    logger.info(
        "Execution summary: {} package(s) read, {} file(s) generated, "
        "{} warning(s), {} error(s).",
        len(dtsx_files),
        len(generated_files),
        len(pending_files),
        len(failed_files),
    )

    return 1 if failed_files else 0


def main() -> int:
    args = parse_args()
    configure_logging(args.log_level)

    try:
        return run(args.project_folder, args.output_folder)
    except Exception as exc:
        logger.error("{}", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
