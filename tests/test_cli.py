import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase


FIXTURES = Path(__file__).parent / "fixtures"


class CliTests(TestCase):

    def test_cli_generates_markdown_for_dtsx_folder(self):
        with TemporaryDirectory() as input_dir, TemporaryDirectory() as output_dir:
            input_path = Path(input_dir)
            output_path = Path(output_dir)
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
            self.assertTrue((output_path / "SamplePackage.md").exists())

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
            self.assertIn("does not contain supported SSIS files", result.stderr)
