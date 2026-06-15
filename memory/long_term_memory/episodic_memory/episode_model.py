from pydantic import BaseModel
from datetime import datetime


class Episode(BaseModel):

    id: str

    summary: str

    session_id: str

    start_time: datetime
    end_time: datetime

    emotional_weight: float = 0.5
    importance: float

    embedding_id: str | None = None

    parent_episode_id: str | None = None

    created_at: datetime