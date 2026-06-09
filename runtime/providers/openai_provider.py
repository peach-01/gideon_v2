from openai import AsyncOpenAI

from genetics.base_configs.config import settings
from mind.self_model.identity_service import IdentityService

client = AsyncOpenAI(api_key=settings.OPEN_API_KEY)


class OpenAIProvider:

    MODEL_MAP = {
        "reasoning": "o3",
        "planning": "o3",
        "coding": "gpt-4.1",
        "memory": "gpt-4o-mini",
        "summarization": "gpt-4o-mini",
        "critic": "o3",
        "tool_use": "gpt-4.1",
    }

    def __init__(self):
        self.identity = IdentityService()

    async def generate(self, task, prompt, system_prompt=""):
        model = self.MODEL_MAP.get(task, "gpt-4.1")
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
                    "content": prompt,
                },
            ],
        )

        return response.choices[0].message.content