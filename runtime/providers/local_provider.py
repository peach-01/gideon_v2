from ollama import AsyncClient
from models.python.conversation.advisor_response import AdvisorResponse

client = AsyncClient()


class LocalProvider:

    async def boot(self):
        print("[OLLAMA] Ready.")


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