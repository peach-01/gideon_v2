import asyncio
from sentence_transformers import SentenceTransformer

class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


    async def boot(self):
        print("[EMBEDDING] Ready.")


    async def embed(self, text: str):
        loop = asyncio.get_running_loop()

        embedding = await loop.run_in_executor(None, lambda: self.model.encode(text, normalize_embeddings=True).tolist())

        return embedding