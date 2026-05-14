from lxml import etree

from app.parsers.xml_utils import attribute_value, element_label, property_text


class VariablesExtractor:

    def extract(self, root: etree._Element) -> list[dict]:
        variables = []

        for element in root.xpath(".//*[local-name()='Variable']"):
            variables.append(
                {
                    "name": element_label(element, "Unnamed variable"),
                    "namespace": attribute_value(element, "Namespace"),
                    "data_type": (
                        attribute_value(element, "DataType")
                        or property_text(element, "DataType")
                    ),
                    "value": self._value(element),
                    "scope": attribute_value(element, "Scope"),
                    "expression": attribute_value(element, "Expression") or property_text(element, "Expression"),
                }
            )

        return variables

    def extract_parameters(self, root: etree._Element) -> list[dict]:
        parameters = []

        for element in root.xpath(".//*[local-name()='PackageParameter' or local-name()='ProjectParameter' or local-name()='Parameter']"):
            parameters.append(
                {
                    "name": element_label(element, "Unnamed parameter"),
                    "data_type": attribute_value(element, "DataType") or property_text(element, "DataType"),
                    "value": self._value(element),
                    "required": attribute_value(element, "Required") or property_text(element, "Required"),
                    "sensitive": attribute_value(element, "Sensitive") or property_text(element, "Sensitive"),
                }
            )

        return parameters

    def _value(self, element: etree._Element) -> str | None:
        value = property_text(element, "Value")
        if value:
            return value

        value_element = element.xpath(".//*[local-name()='VariableValue' or local-name()='ParameterValue']")
        if value_element and value_element[0].text:
            return value_element[0].text.strip()

        return None
