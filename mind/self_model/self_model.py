from pydantic import BaseModel

from memory.memory_models.basic_memory.memory import Memory

class SelfModel(BaseModel):

    identity: dict

    beliefs: list[Memory] = []
    values: list[Memory] = []
    preferences: list[Memory] = []
    
    experiences: list[Memory] = []
