from pydantic import BaseModel, Field
from datetime import datetime


class Entity(BaseModel):

    id: str

    name: str
    entity_type: str

    aliases: list[str] = Field(default_factory=list)

    description: str | None = None

    created_at: datetime
    updated_at: datetime