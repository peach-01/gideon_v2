from memory.memory_models.basic_memory.memory_type import MemoryType


class BeliefService:

    def __init__(self, memory_service):
        self.memory = memory_service


    async def all(self):
        return await self.memory.search(
            query="",
            memory_types=[
                MemoryType.BELIEF
            ],
            limit=1000
        )
    

    async def add(self, statement: str, confidence: float=0.5):
        return await self.memory.store(
            content=statement,
            memory_type=MemoryType.BELIEF,
            importance=confidence,
        )