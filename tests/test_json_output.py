import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from app.parsers.dtsx_parser import DtsxParser
from app.sdd.json_writer import JsonWriter
from app.sdd.project_builder import ProjectBuilder


FIXTURES = Path(__file__).parent / "fixtures"


class JsonOutputTests(TestCase):

    def test_json_writer_writes_package_and_project_json(self):
        package = DtsxParser().parse(FIXTURES / "sample.dtsx")

        with TemporaryDirectory() as temp_dir:
            output_folder = Path(temp_dir)
            writer = JsonWriter(output_folder)
            package_json = writer.write_package_json(package)
            project = ProjectBuilder().build_project_data(
                ssis_folder=FIXTURES,
                output_folder=output_folder,
                supported_files=[FIXTURES / "sample.dtsx"],
                package_data=[package],
                generated_markdown_files=[output_folder / "SamplePackage.md"],
                generated_package_json_files=[package_json],
                skipped_files=[],
                failed_files=[],
            )
            project_json = writer.write_project_json(project)

            package_payload = json.loads(package_json.read_text(encoding="utf-8"))
            project_payload = json.loads(project_json.read_text(encoding="utf-8"))

        self.assertEqual(package_payload["package_name"], "SamplePackage")
        serialized_package = json.dumps(package_payload)
        self.assertNotIn("Password=secret", serialized_package)
        self.assertNotIn("secret", serialized_package)
        self.assertEqual(project_payload["schema_version"], "1.0")
        self.assertEqual(project_payload["summary"]["package_count"], 1)
        self.assertEqual(project_payload["packages"][0]["package_name"], "SamplePackage")
