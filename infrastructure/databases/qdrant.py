from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from config import settings

client = QdrantClient(url=settings.QDRANT_URL)

collections = [c.name for c in client.get_collections().collections]

if "gideon_memory" not in collections:
    client.create_collection(
        collection_name="gideon_memory",
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE,
        ),
    )