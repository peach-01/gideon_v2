from pydantic import BaseModel
from datetime import datetime


class Goal(BaseModel):

    id: str

    title: str
    description: str | None = None

    status: str = "active"
    priority: float = 0.5

    created_at: datetime
    updated_at: datetime

    completed_at: datetime