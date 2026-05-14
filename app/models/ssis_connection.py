from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SSISConnection:
    name: str
    connection_type: str | None = None
    connection_string: str | None = None
    provider: str | None = None
    server: str | None = None
    database: str | None = None
    file_path: str | None = None
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
