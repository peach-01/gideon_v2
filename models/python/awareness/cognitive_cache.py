from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class BootCache:
    boot_time: datetime = field(default_factory=lambda: datetime.now(UTC))

    self_model_snapshot = None
    rendered_identity: str | None = None

    graph_summary = None
    semantic_summary = None
    memory_statistics = None

    last_refresh: datetime | None = None


@dataclass
class SessionCache:
    conversation_summary: str | None = None

    working_context = None
    goals = None

    last_memories: list = field(default_factory=list)
    last_tool_outputs: list = field(default_factory=list)


@dataclass
class MessageCache:
    retrieval_results: list = field(default_factory=list)
    tool_results: list = field(default_factory=list)

    planner_output = None
    prompt = None


@dataclass
class CognitiveCache:
    boot: BootCache = field(default_factory=BootCache)

    sessions: dict[str, SessionCache] = field(default_factory=dict)

    message: MessageCache = field(default_factory=MessageCache)