from dataclasses import asdict, dataclass, field
from typing import Any

from app.models.ssis_connection import SSISConnection
from app.models.ssis_task import SSISTask


@dataclass
class SSISPackage:
    name: str
    file_path: str
    package_id: str | None = None
    version: str | None = None
    creator: str | None = None
    creation_date: str | None = None
    connections: list[SSISConnection] = field(default_factory=list)
    variables: list[dict[str, Any]] = field(default_factory=list)
    parameters: list[dict[str, Any]] = field(default_factory=list)
    tasks: list[SSISTask] = field(default_factory=list)
    data_flows: list[dict[str, Any]] = field(default_factory=list)
    sql_commands: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["package_name"] = self.name
        return data
