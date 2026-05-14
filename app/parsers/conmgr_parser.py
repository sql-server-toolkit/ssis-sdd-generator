from pathlib import Path

from lxml import etree

from app.extractors.connections_extractor import ConnectionsExtractor
from app.models import SSISConnection
from app.parsers.xml_utils import attribute_value, element_label, named_properties, property_text


class ConnectionManagerParser:

    def parse(self, file_path: Path) -> dict:
        parser = etree.XMLParser(remove_blank_text=True, recover=False)
        tree = etree.parse(str(file_path), parser)
        root = tree.getroot()
        extractor = ConnectionsExtractor()
        properties = named_properties(root)
        connection_string = property_text(root, "ConnectionString")
        parsed_connection = extractor._parse_connection_string(connection_string)

        connection = SSISConnection(
            name=element_label(root, file_path.stem),
            connection_type=extractor._normalize_connection_type(
                attribute_value(root, "CreationName")
                or attribute_value(root, "ConnectionManagerType")
                or property_text(root, "CreationName")
            ),
            connection_string=extractor._mask_connection_string(connection_string),
            provider=property_text(root, "Provider") or parsed_connection.get("provider"),
            server=(
                property_text(root, "ServerName")
                or parsed_connection.get("server")
                or parsed_connection.get("data source")
            ),
            database=(
                property_text(root, "InitialCatalog")
                or parsed_connection.get("initial catalog")
                or parsed_connection.get("database")
            ),
            file_path=property_text(root, "FileName") or parsed_connection.get("filename"),
            properties={
                **properties,
                "parsed_connection_keys": sorted(parsed_connection.keys()),
            },
        )

        return connection.to_dict()
