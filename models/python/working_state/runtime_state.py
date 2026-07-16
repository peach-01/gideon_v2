from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class RuntimeState:

    status: str = "running"

    session_ids: list[str] = field(default_factory=list)

    pending_tasks: list = field(default_factory=list)
    pending_reflections: list = field(default_factory=list)

    conversation_summary: dict = field(default_factory=dict)

    model_state: dict = field(default_factory=dict)

    boot_cache: dict = field(default_factory=dict)

    saved_at: datetime = field(default_factory=lambda: datetime.now(UTC))