from lxml import etree

from app.models import SSISConnection
from app.parsers.xml_utils import attribute_value, element_label, named_properties, property_text

SENSITIVE_KEYS = {
    "password",
    "pwd",
    "token",
    "access token",
    "secret",
    "client secret",
    "accountkey",
    "sharedaccesskey",
}


class ConnectionsExtractor:

    def extract(self, root: etree._Element) -> list[SSISConnection]:
        connections = []

        for element in root.xpath(".//*[local-name()='ConnectionManager']"):
            properties = named_properties(element)
            connection_string = (
                property_text(element, "ConnectionString")
                or properties.get("ConnectionString")
            )
            parsed_connection = self._parse_connection_string(connection_string)
            connection_type = self._normalize_connection_type(
                attribute_value(element, "CreationName")
                or attribute_value(element, "ConnectionManagerType")
                or property_text(element, "CreationName")
            )

            connections.append(
                SSISConnection(
                    name=element_label(element, "Unnamed connection"),
                    connection_type=connection_type,
                    connection_string=self._mask_connection_string(connection_string),
                    provider=property_text(element, "Provider") or parsed_connection.get("provider"),
                    server=(
                        property_text(element, "ServerName")
                        or parsed_connection.get("server")
                        or parsed_connection.get("data source")
                    ),
                    database=(
                        property_text(element, "InitialCatalog")
                        or parsed_connection.get("initial catalog")
                        or parsed_connection.get("database")
                    ),
                    file_path=property_text(element, "FileName") or parsed_connection.get("filename"),
                    properties={
                        **properties,
                        "detected_type": connection_type,
                        "parsed_connection_keys": sorted(parsed_connection.keys()),
                    },
                )
            )

        return connections

    def _normalize_connection_type(self, raw_type: str | None) -> str | None:
        if not raw_type:
            return None

        value = raw_type.lower()
        if "oledb" in value or "ole db" in value:
            return "OLE DB"
        if "ado.net" in value or "adonet" in value:
            return "ADO.NET"
        if "flatfile" in value or "flat file" in value:
            return "Flat File"
        if "excel" in value:
            return "Excel"
        if "odbc" in value:
            return "ODBC"

        return raw_type

    def _parse_connection_string(self, connection_string: str | None) -> dict[str, str]:
        if not connection_string:
            return {}

        parsed = {}
        for part in connection_string.split(";"):
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            key = key.strip().lower()
            value = value.strip()
            if key:
                parsed[key] = value

        return parsed

    def _mask_connection_string(self, connection_string: str | None) -> str | None:
        if not connection_string:
            return None

        masked_parts = []
        for part in connection_string.split(";"):
            if "=" not in part:
                masked_parts.append(part)
                continue

            key, value = part.split("=", 1)
            if key.strip().lower() in SENSITIVE_KEYS:
                value = "***"
            masked_parts.append(f"{key}={value}")

        return ";".join(masked_parts)
