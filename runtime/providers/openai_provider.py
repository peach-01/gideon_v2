from openai import AsyncOpenAI
from genetics.base_configs.config import settings
from memory.long_term_memory.episodic_memory.conversations.conversation_models.advisor_response import AdvisorResponse

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIProvider:

    async def generate(self, model, messages, system_prompt=""):
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
        )

        message = response.choices[0].message

        return AdvisorResponse(
            content=message.content or "",
            provider="openai",
            model=model,
        )