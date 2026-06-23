from runtime.providers.openai_provider import OpenAIProvider
from runtime.providers.claude_provider import ClaudeProvider
from runtime.providers.gemini_provider import GeminiProvider
from runtime.providers.local_provider import LocalProvider

from nervous_system.signal_bus.routing.advisor_router import AdvisorRouter

from memory.memory_service import MemoryService
from memory.long_term_memory.episodic_memory.conversations.conversation_models.advisor_response import AdvisorResponse
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock

class AdvisorService:

    def __init__(self):
        self.router = AdvisorRouter()
        self.memory = MemoryService(self)

        self.providers = {
            "gpt": OpenAIProvider(self.memory),
            "claude": ClaudeProvider(),
            "gemini": GeminiProvider(self.memory),
            "local": LocalProvider(),
        }

    async def ask(self, task: str, messages: list[ContentBlock] | list[dict], system_prompt: str="", advisor: str | None = None) -> AdvisorResponse:
        advisor_name = advisor or self.router.choose(task)

        provider = self.providers[advisor_name]

        return await provider.generate(task=task, messages=messages, system_prompt=system_prompt)