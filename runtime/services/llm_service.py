from openai import AsyncOpenAI

from genetics.base_configs.config import settings
from mind.self_model.identity_service import IdentityService
from nervous_system.signal_bus.routing.model_router import ModelRouter

client = AsyncOpenAI(api_key=settings.OPEN_API_KEY)


class LLMService:

    def __init__(self):
        self.identity = IdentityService()
        self.model_router = ModelRouter()

    async def generate(self, user_prompt: str, system_prompt: str | None = None, task: str="reasoning"):
        model = self.model_router.choose(task)
        base_identity = self.identity.system_prompt()

        if system_prompt:
            system_prompt = base_identity + "\n\n" + system_prompt
        else:
            system_prompt = base_identity

        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content
    
    async def chat(self, messages, tools=None, model="gpt-4.1"):
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto" if tools else None,
        )

        return response.choices[0].message