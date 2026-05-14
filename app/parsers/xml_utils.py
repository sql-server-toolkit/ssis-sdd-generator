from lxml import etree


def attribute_value(element: etree._Element, attribute_name: str) -> str | None:
    for attribute, value in element.attrib.items():
        if etree.QName(attribute).localname == attribute_name:
            return value

    return None


def property_text(element: etree._Element, property_name: str) -> str | None:
    matches = element.xpath(
        ".//*[local-name()='Property' and @*[local-name()='Name']=$property_name]",
        property_name=property_name,
    )

    if not matches:
        return attribute_value(element, property_name)

    text = matches[0].text
    return text.strip() if text else None


def named_properties(element: etree._Element) -> dict[str, str]:
    properties = {}

    for property_element in element.xpath(".//*[local-name()='Property']"):
        name = attribute_value(property_element, "Name")
        if name and property_element.text:
            properties[name] = property_element.text.strip()

    return properties


def element_label(element: etree._Element, fallback: str = "Unnamed") -> str:
    return (
        attribute_value(element, "ObjectName")
        or attribute_value(element, "Name")
        or property_text(element, "ObjectName")
        or fallback
    )
