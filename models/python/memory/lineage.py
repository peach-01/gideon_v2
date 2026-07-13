from datetime import datetime, UTC
from pydantic import BaseModel, Field


class MemoryLineage(BaseModel):

    id: str

    child_memory_id: str
    parent_memory_id: str

    relationship_type: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))