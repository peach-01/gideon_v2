from openai import AsyncOpenAI

from genetics.base_configs.config import settings

from runtime.providers.message_adapter import MessageAdapter

from mind.self_model.self_model_service import SelfModelService
from mind.self_model.self_model_formatter import SelfModelFormatter
from mind.identity.identity_service import IdentityService

from memory.long_term_memory.episodic_memory.conversations.conversation_models.advisor_response import AdvisorResponse
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIProvider:

    MODEL_MAP = {
        "reasoning":        "o3",
        "planning":         "o3",
        "coding":           "gpt-4.1",
        "memory":           "gpt-4o-mini",
        "summarization":    "gpt-4o-mini",
        "critic":           "o3",
        "tool_use":         "gpt-4.1",
    }


    def __init__(self, memory_service):
        self.memory = memory_service
        self.identity = IdentityService()

        self.self_model = SelfModelService(
            memory_service=self.memory, 
            identity_service=self.identity
        )
        self.formatter = SelfModelFormatter()


    async def generate(self, task, messages, system_prompt=""):
        model = self.MODEL_MAP.get(task, "gpt-4.1")

        self_snap = await self.self_model.snapshot()

        base_identity = self.formatter.format(snapshot=self_snap)

        if system_prompt:
            system_prompt = base_identity + "\n\n" + system_prompt
        else:
            system_prompt = base_identity

        provider_messages = [
            ConversationMessage(
                role="system",
                content=[
                    ContentBlock(
                        type="text",
                        content=system_prompt
                    )
                ]
            )
        ]

        provider_messages.extend(MessageAdapter.to_openai(messages=messages))

        response = await client.chat.completions.create(
            model=model,
            messages=provider_messages
        )

        message = response.choices[0].message

        return AdvisorResponse(
            content=message.content or "",
            provider="openai",
            model=model,
        )