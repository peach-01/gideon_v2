from pydantic import BaseModel
from datetime import datetime


class Entity(BaseModel):

    id: str

    name: str
    entity_type: str

    aliases: list[str] = []

    descriptions: str | None = None

    created_at: datetime
    updated_at: datetime