from pydantic import BaseModel
from datetime import datetime


class Reminder(BaseModel):
    
    id: str
    
    title: str
    message: str

    due_at: datetime
    completed: bool = False