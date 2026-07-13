import uuid

from datetime import datetime, UTC

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import MemoryEdge
from memory.long_term_memory.semantic_memory.relations.entity_service import EntityService
from infrastructure.databases.postgres_models import MemoryEdge
from infrastructure.databases.postgres_models import EntityRecord
from models.python.memory.graph_summary import GraphSummary


class GraphMemoryService:

    def __init__(self):
        self.entities = EntityService()


    async def boot(self):
        print("[GRAPH-MEMORY] Ready.")
    

    async def add_edge(self, source_entity: str, relation: str, target_entity: str, confidence: float=1.0, origin_episode_id: str | None = None):
        db = SessionLocal()

        try:
            source = await self.entities.get_or_create(db, source_entity, "concept")
            target = await self.entities.get_or_create(db, target_entity, "concept")

            edge = MemoryEdge(
                id=str(uuid.uuid4()),
                source_entity_id=source.id,
                relation=relation,
                target_entity_id=target.id,
                confidence=confidence,
                origin_episode_id=origin_episode_id,
                created_at=datetime.now(UTC),
            )

            existing = db.query(MemoryEdge).filter(
                MemoryEdge.source_entity_id == source.id,
                MemoryEdge.target_entity_id == target.id,
                MemoryEdge.relation == relation
            ).first()

            if existing:
                return existing

            db.add(edge)
            db.commit()

            return edge

        finally:
            db.close()

    
    async def get_summary(self) -> GraphSummary:
        db = SessionLocal()
        
        try:
            entity_count = db.query(EntityRecord).count()

            edges = db.query(MemoryEdge).all()
            edge_count = len(edges)

            relation_counts: dict[str, int] = {}

            for edge in edges:
                relation_counts[edge.relation] = relation_counts.get(edge.relation, 0) + 1

            top_relations = sorted(relation_counts.items(), key=lambda x: x[1], reverse=True)[:10]

            return GraphSummary(
                entity_count=entity_count,
                edge_count=edge_count,
                relation_counts=relation_counts,
                top_relations=top_relations,
            )
        
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