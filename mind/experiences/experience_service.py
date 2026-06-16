from memory.memory_models.basic_memory.memory_type import MemoryType


class ExperienceService:

    def __init__(self, memory_service):
        self.memory = memory_service


    async def all(self):
        return await self.memory.search(
            query="",
            memory_types=[
                MemoryType.LIFE_EVENT
            ],
            limit=1000
        )
    

    async def add(self, summary: str, importance: float=0.7):
        return await self.memory.store(
            content=summary,
            memory_type=MemoryType.LIFE_EVENT,
            importance=importance,
        )