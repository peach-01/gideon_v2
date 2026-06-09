import uuid

from datetime import datetime, UTC

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import MemoryEdge


class GraphMemoryService:

    async def add_edge(self, source_entity: str, relation: str, target_entity: str, confidence: float=1.0):
        db = SessionLocal()

        try:
            edge = MemoryEdge(
                id=str(uuid.uuid4()),
                source_entity=source_entity,
                relation=relation,
                target_entity=target_entity,
                confidence=confidence,
                created_at=datetime.now(UTC),
            )

            db.add(edge)
            db.commit()

            return edge

        finally:
            db.close()

    
    async def get_edges(self, entity: str):
        db = SessionLocal()

        try:
            return db.query(MemoryEdge).filter((MemoryEdge.source_identity == entity) | (MemoryEdge.target_entity == entity)).all()
        
        finally:
            db.close()


    async def find_relation(self, source_entity, relation):
        db = SessionLocal()

        try:
            return db.query(MemoryEdge).filter(
                MemoryEdge.source_identity == source_entity, 
                MemoryEdge.relation == relation,
            ).first()

        finally:
            db.close()