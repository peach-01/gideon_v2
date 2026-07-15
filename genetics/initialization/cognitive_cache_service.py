from datetime import datetime, UTC
from models.python.awareness.cognitive_cache import SessionCache, MessageCache, CognitiveCache


class CognitiveCacheService:
 
    def __init__(self, memory_service, self_model_service, graph_service, formatter):
        self.memory = memory_service
        self.self_model = self_model_service
        self.graph_memory = graph_service
        self.self_model_formatter = formatter

        self.cache = CognitiveCache()


    async def boot(self):

        # Only build once
        if self.cache.boot.last_refresh is not None:
            return self.cache.boot
        
        self_snap = await self.self_model.snapshot()

        self.cache.boot.self_model_snapshot = self_snap
        self.cache.boot.rendered_identity = self.self_model_formatter.format(self_snap)

        self.cache.boot.graph_summary = await self.graph_memory.get_summary()
        self.cache.boot.memory_statistics = await self.memory.statistics()
        self.cache.boot.semantic_summary = await self.memory.semantic_summary()

        self.cache.boot.last_refresh = datetime.now(UTC)

        return self.cache.boot

    
    async def refresh_boot(self):
        self.cache.boot.last_refresh = None
        return await self.boot()


    async def refresh_semantic(self):
        self.cache.boot.semantic_summary = await self.memory.semantic_summary()
    

    async def refresh_identity(self):
        self_snap = await self.self_model.snapshot()
        
        self.cache.boot.self_model_snapshot = self_snap
        self.cache.boot.rendered_identity = self.self_model_formatter.format(self_snap)
    


    def ensure_session(self, session_id: str) -> SessionCache:
        return self.cache.sessions.setdefault(session_id, SessionCache())
    

    def clear_message(self):
        self.cache.message = MessageCache()