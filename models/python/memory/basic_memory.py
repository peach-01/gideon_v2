from pydantic import BaseModel, Field
from datetime import datetime, UTC

from models.python.memory.provenance import Provenance


class Memory(BaseModel):

    id: str

    vector_id: str | None = None

    memory_type: str
    memory_tier: str

    content: str
    canonical_content: str

    confidence: float = 1.0
    importance: float = 0.5
    stability: float = 1.0

    source: str

    access_count: int = 0
    last_accessed: datetime | None = None

    meta_data: dict = Field(default_factory=dict)
    
    provenance: Provenance | None = None

    embedding: list[float] | None = None

    valid_from: datetime | None = None
    valid_until: datetime | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None