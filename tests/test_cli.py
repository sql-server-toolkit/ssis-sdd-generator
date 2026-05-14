import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase


FIXTURES = Path(__file__).parent / "fixtures"


class CliTests(TestCase):

    def test_cli_generates_markdown_for_dtsx_folder(self):
        with TemporaryDirectory() as temp_dir, TemporaryDirectory() as output_dir:
            input_path = Path(temp_dir) / "My SSIS Project"
            output_path = Path(output_dir)
            input_path.mkdir()
            (input_path / "RealProject.dtproj").write_text("<Project />", encoding="utf-8")
            (input_path / "sample.dtsx").write_text(
                (FIXTURES / "sample.dtsx").read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "app.main",
                    "--ssis-folder",
                    str(input_path),
                    "--output-folder",
                    str(output_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            run_folders = list(output_path.iterdir())
            self.assertEqual(len(run_folders), 1)
            self.assertTrue(run_folders[0].name.startswith("RealProject_"))
            self.assertTrue((run_folders[0] / "SamplePackage.md").exists())
            self.assertTrue((run_folders[0] / "project.json").exists())
            self.assertTrue((run_folders[0] / "packages" / "SamplePackage.json").exists())

    def test_cli_keeps_project_folder_alias_for_compatibility(self):
        with TemporaryDirectory() as temp_dir, TemporaryDirectory() as output_dir:
            input_path = Path(temp_dir) / "Legacy Project"
            output_path = Path(output_dir)
            input_path.mkdir()
            (input_path / "sample.dtsx").write_text(
                (FIXTURES / "sample.dtsx").read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "app.main",
                    "--project-folder",
                    str(input_path),
                    "--output-folder",
                    str(output_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            run_folders = list(output_path.iterdir())
            self.assertEqual(len(run_folders), 1)
            self.assertTrue(run_folders[0].name.startswith("Legacy_Project_"))
            self.assertTrue((run_folders[0] / "SamplePackage.md").exists())
            self.assertTrue((run_folders[0] / "project.json").exists())

    def test_cli_reports_empty_input_folder(self):
        with TemporaryDirectory() as input_dir, TemporaryDirectory() as output_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "app.main",
                    "--project-folder",
                    input_dir,
                    "--output-folder",
                    output_dir,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("does not contain supported files", result.stderr)
