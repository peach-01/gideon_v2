from pydantic import BaseModel, Field
from datetime import datetime, UTC

from memory.memory_models.provenance import Provenance


class Memory(BaseModel):

    id: str

    memory_type: str
    content: str

    confidence: float = 1.0
    importance: float = 0.5
    stability: float = 1.0

    source: str
    
    provenance: Provenance | None = None

    embedding: list[float] | None = None

    valid_from: datetime | None = None
    valid_until: datetime | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None