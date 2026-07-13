from pydantic import BaseModel, Field

from models.python.memory.basic_memory import Memory

class SelfModel(BaseModel):

    identity: dict

    beliefs: list[Memory] = Field(default_factory=list)
    values: list[Memory] = Field(default_factory=list)
    preferences: list[Memory] = Field(default_factory=list)
    
    experiences: list[Memory] = Field(default_factory=list)
