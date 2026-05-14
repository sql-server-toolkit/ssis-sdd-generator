from pathlib import Path
from lxml import etree

from app.extractors.connections_extractor import ConnectionsExtractor
from app.extractors.control_flow_extractor import ControlFlowExtractor
from app.extractors.data_flow_extractor import DataFlowExtractor
from app.extractors.sql_extractor import SqlExtractor
from app.extractors.variables_extractor import VariablesExtractor
from app.models import SSISPackage
from app.parsers.xml_utils import property_text


class DtsxParser:

    def parse(self, file_path: Path) -> dict:
        parser = etree.XMLParser(remove_blank_text=True, recover=False)
        tree = etree.parse(str(file_path), parser)
        root = tree.getroot()
        connections = ConnectionsExtractor().extract(root)
        variables_extractor = VariablesExtractor()
        variables = variables_extractor.extract(root)
        parameters = variables_extractor.extract_parameters(root)
        tasks = ControlFlowExtractor().extract(root)
        data_flows = DataFlowExtractor().extract(root)
        sql_commands = SqlExtractor().extract(root)

        package = SSISPackage(
            name=property_text(root, "ObjectName") or file_path.stem,
            file_path=str(file_path),
            package_id=property_text(root, "PackageID"),
            version=(
                property_text(root, "VersionGUID")
                or property_text(root, "PackageFormatVersion")
            ),
            creator=property_text(root, "CreatorName"),
            creation_date=property_text(root, "CreationDate"),
            connections=connections,
            variables=variables,
            parameters=parameters,
            tasks=tasks,
            data_flows=data_flows,
            sql_commands=sql_commands,
            properties={
                "root_tag": root.tag,
                "namespaces": {key or "default": value for key, value in root.nsmap.items()},
            },
        )

        return package.to_dict()
