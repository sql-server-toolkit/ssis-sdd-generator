from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from zipfile import ZipFile

from app.parsers.conmgr_parser import ConnectionManagerParser
from app.parsers.dtsx_parser import DtsxParser
from app.parsers.ispac_parser import IspacParser


FIXTURES = Path(__file__).parent / "fixtures"


class ParserTests(TestCase):

    def test_dtsx_parser_extracts_core_metadata(self):
        package = DtsxParser().parse(FIXTURES / "sample.dtsx")

        self.assertEqual(package["package_name"], "SamplePackage")
        self.assertEqual(package["creator"], "Codex")
        self.assertEqual(len(package["connections"]), 1)
        self.assertEqual(package["connections"][0]["database"], "Sales")
        self.assertIn("Password=***", package["connections"][0]["connection_string"])
        self.assertEqual(len(package["variables"]), 1)
        self.assertEqual(len(package["tasks"]), 2)
        self.assertEqual(len(package["data_flows"]), 1)
        self.assertEqual(len(package["sql_commands"]), 1)
        self.assertTrue(package["sql_commands"][0]["is_dynamic"])

    def test_conmgr_parser_masks_secret_values(self):
        connection = ConnectionManagerParser().parse(FIXTURES / "sample.conmgr")

        self.assertEqual(connection["name"], "SharedDb")
        self.assertEqual(connection["connection_type"], "ADO.NET")
        self.assertEqual(connection["server"], "server02")
        self.assertIn("Pwd=***", connection["connection_string"])

    def test_ispac_parser_inspects_archive_entries(self):
        with TemporaryDirectory() as temp_dir:
            ispac_path = Path(temp_dir) / "sample.ispac"
            with ZipFile(ispac_path, "w") as archive:
                archive.write(FIXTURES / "sample.dtsx", "Package.dtsx")
                archive.write(FIXTURES / "sample.conmgr", "Shared.conmgr")
                archive.writestr("Project.params", "<Project />")

            manifest = IspacParser().inspect(ispac_path)

        self.assertEqual(manifest["packages"], ["Package.dtsx"])
        self.assertEqual(manifest["connections"], ["Shared.conmgr"])
        self.assertEqual(manifest["project_parameters"], ["Project.params"])
