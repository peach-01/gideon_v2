import uuid

from datetime import datetime, UTC

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import MemoryEdge
from memory.long_term_memory.semantic_memory.relations.entity_service import EntityService


class GraphMemoryService:

    def __init__(self):
        self.entities = EntityService()

    async def add_edge(self, source_entity: str, relation: str, target_entity: str, confidence: float=1.0, origin_episode_id: str | None = None):
        db = SessionLocal()

        try:
            source = await self.entities.get_or_create(source_entity, "concept")
            target = await self.entities.get_or_create(target_entity, "concept")

            edge = MemoryEdge(
                id=str(uuid.uuid4()),
                source_entity_id=source.id,
                relation=relation,
                target_entity_id=target.id,
                confidence=confidence,
                origin_episode_id=origin_episode_id,
                created_at=datetime.now(UTC),
            )

            db.add(edge)
            db.commit()

            return edge

        finally:
            db.close()

    
    async def get_edges(self, entity_id: str):
        db = SessionLocal()

        try:
            return db.query(MemoryEdge).filter((MemoryEdge.source_identity_id == entity_id) | (MemoryEdge.target_entity_id == entity_id)).all()
        
        finally:
            db.close()


    async def find_relation(self, source_entity_id, relation):
        db = SessionLocal()

        try:
            return db.query(MemoryEdge).filter(
                MemoryEdge.source_entity_id == source_entity_id, 
                MemoryEdge.relation == relation,
            ).first()

        finally:
            db.close()