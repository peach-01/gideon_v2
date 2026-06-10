from pydantic import BaseModel, Field
from datetime import datetime, UTC


class Experience(BaseModel):

    title: str
    summary: str
    outcome: str

    lessons: list[str] = Field(default_factory=list)

    confidence: float

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))