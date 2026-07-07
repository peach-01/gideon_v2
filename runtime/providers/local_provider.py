from ollama import AsyncClient
from memory.long_term_memory.episodic_memory.conversations.conversation_models.advisor_response import AdvisorResponse

client = AsyncClient()


class LocalProvider:

    async def generate(self, model, messages, system_prompt=""):    
        response = await client.chat(
            model=model,
            messages=messages,
        )

        return AdvisorResponse(
            content=response["message"]["content"] or "",
            provider="local",
            model=model,
        )