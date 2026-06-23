from google import genai

from genetics.base_configs.config import settings

from runtime.providers.message_adapter import MessageAdapter

from mind.self_model.self_model_service import SelfModelService
from mind.self_model.self_model_formatter import SelfModelFormatter
from mind.identity.identity_service import IdentityService

from memory.long_term_memory.episodic_memory.conversations.conversation_models.advisor_response import AdvisorResponse

client = genai.Client(api_key=settings.GEMINI_API_KEY)


class GeminiProvider:

    MODEL_MAP = {
        "reasoning":        "gemini-2.5-flash",
        "planning":         "gemini-2.5-flash",
        "coding":           "gemini-2.5-flash",
        "memory":           "gemini-2.5-flash",
        "summarization":    "gemini-2.5-flash",
        "critic":           "gemini-2.5-flash",
        "tool_use":         "gemini-2.5-flash",
    }

    def __init__(self, memory_service):
        self.memory = memory_service
        self.identity = IdentityService()
        self.self_model = SelfModelService(
            memory_service=self.memory,
            identity_service=self.identity,
        )
        self.formatter = SelfModelFormatter()


    async def generate(self, task, messages, system_prompt=""):
        model = self.MODEL_MAP.get(task, "gemini-2.5-flash")

        self_snap = await self.self_model.snapshot()
        base_identity = self.formatter.format(snapshot=self_snap)

        if system_prompt:
            system_prompt = (base_identity + "\n\n" + system_prompt)
        else:
            system_prompt = base_identity

        contents = MessageAdapter.to_gemini(messages=messages)

        response = await client.aio.models.generate_content(
            model=model,
            contents=contents,
            config={
                "system_instruction": system_prompt,
            },
        )

        return AdvisorResponse(
            content=response.text or "",
            provider="gemini",
            model=model,
        )