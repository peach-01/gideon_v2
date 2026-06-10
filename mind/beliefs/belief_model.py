from pydantic import BaseModel, Field
from datetime import datetime, UTC


class Belief(BaseModel):
    
    statement: str

    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    evidence: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)

    domain: str
    source: str

    stability: float = Field(default=1.0, ge=0.0, le=1.0)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_reviewed: datetime = Field(default_factory=lambda: datetime.now(UTC))