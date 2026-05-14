from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SSISTask:
    name: str
    task_type: str
    task_id: str | None = None
    description: str | None = None
    parent: str | None = None
    precedence_constraints: list[dict[str, Any]] = field(default_factory=list)
    properties: dict[str, Any] = field(default_factory=dict)
    children: list["SSISTask"] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
