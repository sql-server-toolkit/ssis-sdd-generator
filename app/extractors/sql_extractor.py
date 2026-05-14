from lxml import etree

from app.parsers.xml_utils import attribute_value, element_label


class SqlExtractor:
    SQL_PROPERTY_NAMES = {
        "SqlCommand",
        "SqlStatement",
        "SqlStatementSource",
        "CommandText",
        "OpenRowset",
    }

    def extract(self, root: etree._Element) -> list[dict]:
        commands = []

        for element in root.xpath(".//*[local-name()='Property']"):
            property_name = attribute_value(element, "Name")
            if property_name not in self.SQL_PROPERTY_NAMES:
                continue

            sql_text = element.text.strip() if element.text else ""
            if not sql_text:
                continue

            owner = element.getparent()
            source = element_label(owner, "Unknown source") if owner is not None else "Unknown source"
            commands.append(
                {
                    "source": source,
                    "property": property_name,
                    "sql": sql_text,
                    "is_dynamic": self._is_dynamic(property_name, sql_text),
                    "statement_type": self._statement_type(sql_text),
                    "referenced_variables": self._referenced_variables(sql_text),
                    "referenced_objects": self._referenced_objects(sql_text),
                }
            )

        return commands

    def _is_dynamic(self, property_name: str, sql_text: str) -> bool:
        return (
            property_name in {"OpenRowset"}
            or "@[" in sql_text
            or "::" in sql_text
            or "?" in sql_text
        )

    def _statement_type(self, sql_text: str) -> str:
        first_token = sql_text.strip().split(maxsplit=1)[0].upper()
        if first_token in {"SELECT", "INSERT", "UPDATE", "DELETE", "MERGE", "EXEC", "EXECUTE"}:
            return "DML"
        if first_token in {"CREATE", "ALTER", "DROP", "TRUNCATE"}:
            return "DDL"

        return "Unknown"

    def _referenced_variables(self, sql_text: str) -> list[str]:
        references = []
        start = 0
        while True:
            start = sql_text.find("@[", start)
            if start == -1:
                break
            end = sql_text.find("]", start)
            if end == -1:
                break
            references.append(sql_text[start + 2:end])
            start = end + 1

        return references

    def _referenced_objects(self, sql_text: str) -> list[str]:
        tokens = sql_text.replace("\n", " ").split()
        object_keywords = {"FROM", "JOIN", "INTO", "UPDATE", "TABLE", "EXEC", "EXECUTE"}
        objects = []

        for index, token in enumerate(tokens[:-1]):
            if token.upper().rstrip(",") in object_keywords:
                objects.append(tokens[index + 1].strip("[];,()"))

        return sorted(set(objects))
