from datetime import datetime


class Fact:

    statement: str

    confidence: float
    evidence: list[str] = []

    contradictions: list[str] = []
    source: str

    stability: float = 1.0

    created_at: datetime
    last_reviewed: datetime