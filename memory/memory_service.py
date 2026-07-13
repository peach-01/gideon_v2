import uuid
from datetime import datetime, UTC
from math import log

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import MemoryRecord

from memory.long_term_memory.semantic_memory.embeddings.embedding_service import EmbeddingService
from memory.storage.vector_memory.vector_memory_service import VectorMemoryService
from models.python.memory.enums.memory_type import MemoryType
from memory.long_term_memory.semantic_memory.relations.canonicalizer import MemoryCanonicalizer
from memory.storage.lineage.lineage_service import LineageService
from models.python.memory.provenance import Provenance
from models.python.memory.tier_mapper import get_tier
from models.python.memory.memory_statistics import MemoryStatistics, SemanticSummary


# Typical values: 0.70 = loose; 0.75 = balanced; 0.80 = strict; 0.85 = very strict
SIMILARITY_THRESHOLD = 0.78


def rank(memory):
    recency = (datetime.now(UTC) - memory.created_at).days
    recency_score = 1 / (1 + recency)

    return (
        memory.importance * 0.30 +
        memory.confidence * 0.40 +
        recency_score * 0.10 +
        log(memory.access_count + 1) * 0.20
    )


class MemoryService:

    def __init__(self, advisor_service):
        self.advisor = advisor_service

        self.embedder = EmbeddingService()
        self.vector_service = VectorMemoryService()
        self.canonicalizer = MemoryCanonicalizer(advisor_service=self.advisor)
        self.lineage = LineageService()


    async def boot(self):
        print("[MEMORY] Ready.")

    
    def reinforce(self, confidence: float):
        return confidence + (1.0 - confidence) * 0.15


    async def store(self, content: str, provenance: Provenance | None = None, memory_type: str=MemoryType.FACT, source: str="user", importance: float=0.5, meta_data: dict | None = None):
        db = SessionLocal()

        try:
            # memory deduplication
            canonical_content = await self.canonicalizer.canonicalize(
                content=content, 
                memory_type=str(memory_type)
            )

            existing = db.query(MemoryRecord).filter(MemoryRecord.canonical_content == canonical_content).first()
            if existing:
                existing.confidence = self.reinforce(existing.confidence)

                existing.last_accessed = datetime.now(UTC)
                existing.access_count += 1
                
                db.commit()

                return existing.id

            memory_id = str(uuid.uuid4())

            embedding = await self.embedder.embed(canonical_content)

            if provenance and provenance.origin_memory_id:
                await self.lineage.add_link(
                    child_memory_id=memory_id,
                    parent_memory_id=provenance.origin_memory_id,
                    relationship_type="derived_from"
                )

            memory_tier = get_tier(memory_type=memory_type)

            record = MemoryRecord(
                id=memory_id,
                vector_id=memory_id,

                memory_type=memory_type,
                memory_tier=memory_tier,

                content=content,
                canonical_content=canonical_content,

                confidence=1.0,
                importance=importance,
                stability=1.0,
                
                source=source,
                
                access_count=0,
                last_accessed=datetime.now(UTC),

                origin_message_id=provenance.message_id if provenance else None,
                origin_episode_id=provenance.episode_id if provenance else None,
                origin_memory_id=provenance.origin_memory_id if provenance else None,
                root_memory_id=provenance.root_memory_id if provenance else None,

                meta_data=meta_data or {},
                
                created_at=datetime.now(UTC),
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



    # --------- SEARCH ----------

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

    
    async def keyword_search(self, db, query: str, memory_types: list | None, limit: int):
        q = db.query(MemoryRecord).filter(MemoryRecord.content.ilike(f"%{query}%"))
        
        if memory_types:
            q = q.filter(MemoryRecord.memory_type.in_(memory_types))

        return q.limit(limit).all()
    

    async def search_by_tier(self, query: str, tier: str, limit: int=20):
        results = await self.search(query=query, limit=limit*2)

        return [
            m for m in results
            if m.memory_tier == tier
        ][:limit]
    
 

    # ------- BOOT / CACHE --------
 
    async def statistics(self) -> MemoryStatistics:
        db = SessionLocal()

        try:
            memories = db.query(MemoryRecord).all()

            if not memories:
                return MemoryStatistics(total_memories=0)

            by_type = {}
            by_tier = {}

            confidence = 0
            importance = 0

            newest = None

            for memory in memories:

                by_type[memory.memory_type] = by_type.get(memory.memory_type, 0) + 1
                by_tier[memory.memory_tier] = by_tier.get(memory.memory_tier, 0) + 1

                confidence += memory.confidence
                importance += memory.importance

                if newest is None or memory.created_at > newest:
                    newest = memory.created_at

            return MemoryStatistics(
                total_memories=len(memories),
                by_type=by_type,
                by_tier=by_tier,
                average_confidence=confidence / len(memories),
                average_importance=importance / len(memories),
                most_recent=newest,
            )

        finally:
            db.close()


    async def semantic_summary(self) -> SemanticSummary:
        db = SessionLocal()

        try:

            summary = SemanticSummary()
            memories = db.query(MemoryRecord).order_by(MemoryRecord.importance.desc()).all()

            buckets = {
                "person": summary.people,
                "project": summary.projects,
                "goal": summary.goals,
                "preference": summary.preferences,
                "skill": summary.skills,
                "decision": summary.decisions,
                "task": summary.tasks,
                "system": summary.systems,
            }

            for memory in memories:
                bucket = buckets.get(memory.memory_type)
                if bucket is None:
                    continue

                if len(bucket) < 15:
                    bucket.append(memory.content)

            return summary

        finally:
            db.close()