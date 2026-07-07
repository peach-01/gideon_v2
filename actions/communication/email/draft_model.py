from pydantic import BaseModel


class Draft(BaseModel):

    recipient: str
    subject: str
    body: str