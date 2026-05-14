from lxml import etree

from app.models import SSISTask
from app.parsers.xml_utils import attribute_value, element_label, named_properties


class ControlFlowExtractor:

    def extract(self, root: etree._Element) -> list[SSISTask]:
        tasks = []

        for element in root.xpath(".//*[local-name()='Executable']"):
            task_type = (
                attribute_value(element, "ExecutableType")
                or attribute_value(element, "CreationName")
                or "Unknown"
            )
            parent = attribute_value(element, "Parent") or self._parent_name(element)
            tasks.append(
                SSISTask(
                    name=element_label(element, "Unnamed task"),
                    task_type=task_type,
                    task_id=attribute_value(element, "refId") or attribute_value(element, "ID"),
                    description=attribute_value(element, "Description"),
                    parent=parent,
                    precedence_constraints=self._precedence_constraints(element),
                    properties={
                        **named_properties(element),
                        "category": self._task_category(task_type),
                        "is_unknown": self._task_category(task_type) == "Unknown",
                        "child_tasks": self._child_task_names(element),
                    },
                )
            )

        return tasks

    def _precedence_constraints(self, element: etree._Element) -> list[dict]:
        constraints = []

        for constraint in element.xpath(".//*[local-name()='PrecedenceConstraint']"):
            constraints.append(
                {
                    "name": element_label(constraint, "Unnamed constraint"),
                    "from": attribute_value(constraint, "From"),
                    "to": attribute_value(constraint, "To"),
                    "value": attribute_value(constraint, "Value"),
                    "expression": attribute_value(constraint, "Expression"),
                }
            )

        return constraints

    def _parent_name(self, element: etree._Element) -> str | None:
        parent = element.getparent()
        while parent is not None:
            if etree.QName(parent).localname == "Executable":
                return element_label(parent, "Unnamed parent")
            parent = parent.getparent()

        return None

    def _child_task_names(self, element: etree._Element) -> list[str]:
        children = element.xpath(
            "./*[local-name()='Executable'] | ./*[local-name()='Executables']/*[local-name()='Executable']"
        )
        return [element_label(child, "Unnamed task") for child in children]

    def _task_category(self, task_type: str) -> str:
        value = task_type.lower()
        if "sqltask" in value or "execute sql" in value:
            return "Execute SQL Task"
        if "pipeline" in value or "data flow" in value:
            return "Data Flow Task"
        if "scripttask" in value or "script task" in value:
            return "Script Task"
        if "filesystemtask" in value or "file system" in value:
            return "File System Task"
        if "ftp" in value or "sftp" in value:
            return "FTP/SFTP Task"
        if "sequence" in value:
            return "Sequence Container"
        if "foreach" in value:
            return "Foreach Loop"

        return "Unknown"
