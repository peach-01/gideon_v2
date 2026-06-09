from pydantic import BaseModel, Field
from datetime import datetime, UTC


class Message(BaseModel):
    
    id: str
    session_id: str

    role: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))