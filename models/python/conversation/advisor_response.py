from dataclasses import dataclass, field
from typing import Any


@dataclass
class AdvisorResponse:

    content: str = ""

    tool_calls: list = field(default_factory=list)
    thoughts: list[str] = field(default_factory=list)

    structured_data: dict[str, Any] = field(default_factory=dict)
    artifacts: list[dict] = field(default_factory=list)
    meta_data: dict[str, Any] = field(default_factory=dict)

    finish_reason: str = "completed"

    provider: str | None = None
    model: str | None = None