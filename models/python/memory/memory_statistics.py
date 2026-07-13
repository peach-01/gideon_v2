from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MemoryStatistics:
    total_memories: int

    by_type: dict[str, int] = field(default_factory=dict)
    by_tier: dict[str, int] = field(default_factory=dict)

    average_confidence: float = 0.0
    average_importance: float = 0.0

    most_recent: datetime | None = None


@dataclass
class SemanticSummary:
    people: list[str] = field(default_factory=list)

    projects: list[str] = field(default_factory=list)

    goals: list[str] = field(default_factory=list)

    preferences: list[str] = field(default_factory=list)

    skills: list[str] = field(default_factory=list)

    decisions: list[str] = field(default_factory=list)

    tasks: list[str] = field(default_factory=list)

    systems: list[str] = field(default_factory=list)