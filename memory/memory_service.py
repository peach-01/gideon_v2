import uuid
from datetime import datetime, UTC

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import MemoryRecord

from memory.semantic_memory.embeddings.embedding_service import EmbeddingService
from memory.vector_memory.vector_memory_service import VectorMemoryService
from memory.models.memory_type import MemoryType


# Typical values: 0.70 = loose; 0.75 = balanced; 0.80 = strict; 0.85 = very strict
SIMILARITY_THRESHOLD = 0.78

def rank(memory):
    recency = (datetime.now(UTC) - memory.created_at).days
    recency_score = 1 / (1 + recency)

    return (
        memory.importance * 0.4 +
        memory.confidence * 0.3 +
        recency_score * 0.2 +
        (min(memory.access_count, 100) / 100) * 0.1
    )

class MemoryService:

    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_service = VectorMemoryService()


    async def store(self, content: str, memory_type: str=MemoryType.FACT, source: str="user", importance: float=0.5):
        db = SessionLocal()

        try:
            # memory deduplication
            existing = db.query(MemoryRecord).filter(MemoryRecord.content == content).first()
            if existing:
                return existing.id

            memory_id = str(uuid.uuid4())

            embedding = await self.embedder.embed(content)

            record = MemoryRecord(
                id=memory_id,
                vector_id=memory_id,
                memory_type=memory_type,
                content=content,
                confidence=1.0,
                importance=importance,
                source=source,
                created_at=datetime.now(UTC),
                last_accessed=datetime.now(UTC),
                access_count=0,
            )

            db.add(record)
            db.commit()

            await self.vector_service.store(
                memory_id=memory_id, 
                embedding=embedding,
                memory_type=memory_type,
                source=source,
            )

            return memory_id
        
        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


    async def search(self, query: str, memory_types: list=None, limit: int=10):
        db = SessionLocal()

        try:
            embedding = await self.embedder.embed(query)

            # --------- VECTOR SEARCH ---------
            vector_results = await self.vector_service.search(embedding=embedding, limit=limit*2)

            vector_results = [
                r for r in vector_results
                if r.score > SIMILARITY_THRESHOLD
            ]

            vector_ids = [r.payload["memory_id"] for r in vector_results]

            vector_memories = []

            if vector_ids:
                vector_memories = db.query(MemoryRecord).filter(MemoryRecord.id.in_(vector_ids)).all()
            

            # ---------- KEYWORD SEARCH ----------
            keyword_results = await self.keyword_search(db=db, query=query, memory_types=memory_types, limit=limit*2)


            # ----------- MERGE + DEDUPE ----------
            memory_map = {}

            for memory in vector_memories:
                memory_map[memory.id] = memory

            for memory in keyword_results:
                memory_map[memory.id] = memory

            memories = list(memory_map.values())


            # ----------- FILTER TYPES -----------
            if memory_types:
                memories = [
                    m for m in memories
                    if m.memory_type in memory_types
                ]

            # --------- UPDATE ACCESS STATS --------
            for memory in memory_map.values():
                memory.last_accessed = datetime.now(UTC)
                memory.access_count += 1

            db.commit()

            # ------------- RANK --------------
            memories.sort(
                key=rank,
                reverse=True,
            )

            return memories[:limit]
        
        finally:
            db.close()

    
    def keyword_search(self, db, query: str, memory_types: list | None, limit: int):
        q = db.query(MemoryRecord).filter(MemoryRecord.content.ilike(f"%{query}%"))
        
        if memory_types:
            q = q.filter(MemoryRecord.memory_type.in_(memory_types))

        return q.limit(limit).all()