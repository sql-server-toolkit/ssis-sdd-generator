from pathlib import Path

import argparse
import sys

from loguru import logger

from app import config
from app.parsers.dtsx_parser import DtsxParser
from app.sdd.json_writer import JsonWriter
from app.sdd.markdown_writer import MarkdownWriter
from app.sdd.paths import build_run_output_folder
from app.sdd.project_builder import ProjectBuilder

SUPPORTED_EXTENSIONS = {".dtsx", ".conmgr", ".ispac"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate SDD Markdown files from SSIS project artifacts."
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--ssis-folder",
        type=Path,
        help=(
            "Folder where the SSIS project is located. Accepts absolute or relative paths. "
            "If omitted, --project-folder, INPUT_FOLDER, or ./input is used."
        ),
    )
    input_group.add_argument(
        "--project-folder",
        type=Path,
        help=(
            "Deprecated alias for --ssis-folder. Folder containing SSIS files. "
            "Defaults to INPUT_FOLDER or ./input."
        ),
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
    args = parser.parse_args()
    args.project_folder = args.ssis_folder or args.project_folder or config.INPUT_FOLDER
    return args


def configure_logging(log_level: str) -> None:
    logger.remove()
    logger.add(sys.stderr, level=log_level.upper(), format="{level}: {message}")


def validate_project_folder(project_folder: Path) -> list[Path]:
    project_folder = project_folder.expanduser().resolve()

    if not project_folder.exists():
        raise FileNotFoundError(f"SSIS folder does not exist: {project_folder}")

    if not project_folder.is_dir():
        raise NotADirectoryError(f"SSIS path is not a folder: {project_folder}")

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
            "SSIS folder does not contain supported files "
            "(.dtsx, .conmgr, .ispac)."
            f"{extension_message}"
        )

    return supported_files


def run(project_folder: Path, output_folder: Path) -> int:
    project_folder = project_folder.expanduser().resolve()
    output_folder = output_folder.expanduser().resolve()
    supported_files = validate_project_folder(project_folder)
    dtsx_files = sorted(
        file_path for file_path in supported_files if file_path.suffix.lower() == ".dtsx"
    )
    pending_files = sorted(set(supported_files) - set(dtsx_files))

    parser = DtsxParser()
    run_output_folder = build_run_output_folder(output_folder, project_folder)
    markdown_writer = MarkdownWriter(run_output_folder)
    json_writer = JsonWriter(run_output_folder)
    logger.info("Writing generated files to: {}", run_output_folder)

    generated_files = []
    generated_package_json_files = []
    failed_files = []
    parsed_packages = []

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
            parsed_packages.append(package_data)
            package_json_file = json_writer.write_package_json(package_data)
            generated_package_json_files.append(package_json_file)
            output_file = markdown_writer.write_package_spec(package_data)
            generated_files.append(output_file)
            logger.info("Generated package JSON: {}", package_json_file)
            logger.info("Generated spec: {}", output_file)
        except Exception as exc:
            failed_files.append(dtsx_file)
            logger.error("Failed to process {}: {}", dtsx_file, exc)

    index_file = markdown_writer.write_project_index(generated_files)
    if index_file:
        logger.info("Generated project index: {}", index_file)

    project_data = ProjectBuilder().build_project_data(
        ssis_folder=project_folder,
        output_folder=run_output_folder,
        supported_files=supported_files,
        package_data=parsed_packages,
        generated_markdown_files=generated_files,
        generated_package_json_files=generated_package_json_files,
        skipped_files=pending_files,
        failed_files=failed_files,
    )
    project_json_file = json_writer.write_project_json(project_data)
    logger.info("Generated project JSON: {}", project_json_file)

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
