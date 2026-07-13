from dataclasses import dataclass

@dataclass
class GoalSummary:
    active: list[str]
    completed: int
    highest_priority: str | None
    total: int