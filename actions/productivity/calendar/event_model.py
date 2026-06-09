from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):

    id: str

    title: str

    start: datetime
    end: datetime