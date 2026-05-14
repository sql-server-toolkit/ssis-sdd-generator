from dataclasses import asdict, dataclass, field
from typing import Any

from app.models.ssis_connection import SSISConnection
from app.models.ssis_package import SSISPackage


@dataclass
class SSISProject:
    name: str
    root_path: str
    packages: list[SSISPackage] = field(default_factory=list)
    shared_connections: list[SSISConnection] = field(default_factory=list)
    parameters: list[dict[str, Any]] = field(default_factory=list)
    manifest: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
