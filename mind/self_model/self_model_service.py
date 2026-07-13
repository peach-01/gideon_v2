from models.python.awareness.self_model import SelfModel
from models.python.memory.enums.memory_type import MemoryType


class SelfModelService:

    def __init__(self, memory_service, identity_service):
        self.memory = memory_service
        self.identity = identity_service


    async def boot(self):
        self._snapshot = await self.snapshot()
        print("[SELF-MODEL] Ready.")


    async def snapshot(self):
        beliefs = await self.memory.search("", [MemoryType.BELIEF], 50)
        values = await self.memory.search("", [MemoryType.VALUE], 50)
        experiences = await self.memory.search("", [MemoryType.LIFE_EVENT], 50)
        preferences = await self.memory.search("", [MemoryType.PREFERENCE], 50)

        return SelfModel(
            identity=self.identity.snapshot(),
            beliefs=beliefs,
            values=values,
            experiences=experiences,
            preferences=preferences,
        )