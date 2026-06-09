import uuid

from qdrant_client.models import PointStruct

from infrastructure.databases.qdrant import client


class VectorMemoryService:

    COLLECTION = "gideon_memory"

    async def store(self, memory_id: str, embedding: list[float], memory_type: str, source: str):
        client.upsert(
            collection_name=self.COLLECTION,
            points=[
                PointStruct(
                    id=memory_id,
                    vector=embedding,
                    payload={
                        "memory_id": memory_id,
                        "memory_type": memory_type,
                        "source": source,
                    }
                ),
            ]
        )

    async def search(self, embedding: list[float], limit: int=10):
        results = client.query_points(
            collection_name=self.COLLECTION,
            query=embedding,
            limit=limit,
        ).points

        return results