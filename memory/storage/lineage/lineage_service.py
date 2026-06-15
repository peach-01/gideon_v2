import uuid

from datetime import datetime, UTC

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import MemoryLineageRecord


class LineageService:

    async def add_link(self, child_memory_id: str, parent_memory_id: str, relationship_type: str):
        db = SessionLocal()

        try:
            existing = db.query(MemoryLineageRecord).filter(
                MemoryLineageRecord.child_memory_id == child_memory_id,
                MemoryLineageRecord.parent_memory_id == parent_memory_id,
                MemoryLineageRecord.relationship_type == relationship_type,
            ).first()

            if existing:
                return existing
            

            link = MemoryLineageRecord(
                id=str(uuid.uuid4()),
                child_memory_id=child_memory_id,
                parent_memory_id=parent_memory_id,
                relationship_type=relationship_type,
                created_at=datetime.now(UTC),
            )

            db.add(link)
            db.commit()

            return link
        
        except Exception:
            db.rollback()
            raise

        finally:
            db.close()