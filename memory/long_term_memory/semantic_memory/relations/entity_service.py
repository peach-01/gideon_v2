import uuid

from infrastructure.databases.postgres_models import EntityRecord


class EntityService:

    async def get_or_create(self, db, name: str, entity_type: str):
        try:
            entity = db.query(EntityRecord).filter(EntityRecord.name == name).first()
            if entity:
                return entity
            
            entity = EntityRecord(
                id=str(uuid.uuid4()),
                name=name,
                entity_type=entity_type,
            )

            db.add(entity)
            db.commit()

            return entity
        
        finally:
            db.close()