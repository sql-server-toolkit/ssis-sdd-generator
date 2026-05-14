from lxml import etree

from app.parsers.xml_utils import attribute_value, element_label, named_properties


class DataFlowExtractor:

    def extract(self, root: etree._Element) -> list[dict]:
        data_flows = []

        for executable in root.xpath(
            ".//*[local-name()='Executable' and contains(@*[local-name()='ExecutableType'], 'Pipeline')]"
        ):
            data_flows.append(
                {
                    "name": element_label(executable, "Unnamed data flow"),
                    "components": self._components(executable),
                    "properties": named_properties(executable),
                }
            )

        return data_flows

    def _components(self, executable: etree._Element) -> list[dict]:
        components = []

        for component in executable.xpath(".//*[local-name()='component']"):
            components.append(
                {
                    "name": element_label(component, "Unnamed component"),
                    "component_class_id": attribute_value(component, "componentClassID"),
                    "description": attribute_value(component, "description"),
                    "component_type": self._component_type(component),
                    "connection_references": self._connection_references(component),
                    "column_mappings": self._column_mappings(component),
                    "properties": named_properties(component),
                }
            )

        return components

    def _component_type(self, component: etree._Element) -> str:
        raw_value = (
            attribute_value(component, "componentClassID")
            or attribute_value(component, "description")
            or element_label(component, "")
        ).lower()

        markers = {
            "lookup": "Lookup",
            "derived": "Derived Column",
            "conditional": "Conditional Split",
            "aggregate": "Aggregate",
            "sort": "Sort",
            "merge": "Merge",
            "union": "Union All",
            "source": "Source",
            "destination": "Destination",
            "script": "Script Component",
        }
        for marker, label in markers.items():
            if marker in raw_value:
                return label

        return "Unknown"

    def _connection_references(self, component: etree._Element) -> list[str]:
        references = []
        for connection in component.xpath(".//*[local-name()='connection']"):
            connection_id = (
                attribute_value(connection, "connectionManagerID")
                or attribute_value(connection, "connectionManagerRefId")
                or attribute_value(connection, "name")
            )
            if connection_id:
                references.append(connection_id)

        return sorted(set(references))

    def _column_mappings(self, component: etree._Element) -> list[dict]:
        mappings = []
        for column in component.xpath(".//*[local-name()='inputColumn' or local-name()='outputColumn']"):
            mappings.append(
                {
                    "name": element_label(column, "Unnamed column"),
                    "lineage_id": attribute_value(column, "lineageId"),
                    "external_metadata_column_id": attribute_value(
                        column,
                        "externalMetadataColumnId",
                    ),
                    "data_type": attribute_value(column, "dataType"),
                }
            )

        return mappings
