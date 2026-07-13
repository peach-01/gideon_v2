from pydantic import BaseModel
from datetime import datetime


class MemoryEvidence(BaseModel):

    id: str

    memory_id: str

    message_id: str | None = None
    episode_id: str | None = None

    confidence: float = 1.0

    created_at: datetime