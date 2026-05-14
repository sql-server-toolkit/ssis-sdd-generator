from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from app.parsers.dtsx_parser import DtsxParser
from app.sdd.markdown_writer import MarkdownWriter
from app.sdd.spec_builder import SpecBuilder


FIXTURES = Path(__file__).parent / "fixtures"


class SddTests(TestCase):

    def test_spec_builder_renders_extracted_sections(self):
        package = DtsxParser().parse(FIXTURES / "sample.dtsx")
        markdown = SpecBuilder().build_package_spec(package)

        self.assertIn("# SDD: SamplePackage", markdown)
        self.assertIn("## 1. Specification Metadata", markdown)
        self.assertIn("## 3. Execution Contract", markdown)
        self.assertIn("### 4.1 Connections", markdown)
        self.assertIn("Password=***", markdown)
        self.assertIn("## 8. SQL Specification", markdown)
        self.assertIn("Implementation Backlog", markdown)

    def test_markdown_writer_uses_safe_filename_and_index(self):
        with TemporaryDirectory() as temp_dir:
            writer = MarkdownWriter(Path(temp_dir))
            first = writer.write_package_spec({"package_name": "Package One", "file_path": "one.dtsx"})
            second = writer.write_package_spec({"package_name": "Package/Two", "file_path": "two.dtsx"})
            index = writer.write_project_index([first, second])

            self.assertEqual(first.name, "Package_One.md")
            self.assertEqual(second.name, "Package_Two.md")
            self.assertIsNotNone(index)
            self.assertTrue(index.exists())
