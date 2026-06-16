from openai import AsyncOpenAI
from genetics.base_configs.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class EmbeddingService:

    async def embed(self, text: str):
        response = await client.embeddings.create(model="text-embedding-3-small", input=text)

        return response.data[0].embedding