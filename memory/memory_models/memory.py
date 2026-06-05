from pydantic import BaseModel, Field
from datetime import datetime, UTC


class Memory(BaseModel):

    id: str

    memory_type: str
    content: str

    confidence: float = 1.0

    source: str
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    embedding: list[float] | None = None