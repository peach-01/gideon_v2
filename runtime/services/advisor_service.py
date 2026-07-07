import asyncio
import time

from runtime.providers.openai_provider import OpenAIProvider
from runtime.providers.claude_provider import ClaudeProvider
from runtime.providers.gemini_provider import GeminiProvider
from runtime.providers.local_provider import LocalProvider
from runtime.providers.message_adapter import MessageAdapter

from mind.self_model.self_model_service import SelfModelService
from mind.self_model.self_model_formatter import SelfModelFormatter
from mind.identity.identity_service import IdentityService

from runtime.services.provider_model_service.intelligent_router import IntelligentRouter

from memory.memory_service import MemoryService
from memory.long_term_memory.episodic_memory.conversations.conversation_models.advisor_response import AdvisorResponse
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage


class AdvisorService:

    _semaphore = asyncio.Semaphore(1)
    _last_request_time = 0.0
    _min_interval = 3.0     # seconds


    def __init__(self):
        self.router = IntelligentRouter()
        self.identity = IdentityService()
        self.formatter = SelfModelFormatter()

        self.memory = MemoryService(self)
        self.self_model = SelfModelService(memory_service=self.memory, identity_service=self.identity)

        self.providers = {
            "gpt": OpenAIProvider(),
            "claude": ClaudeProvider(),
            "gemini": GeminiProvider(),
            "local": LocalProvider(),
        }


    async def _build_system_prompt(self, system_prompt: str) -> str:
        snapshot = await self.self_model.snapshot()
        identity = self.formatter.format(snapshot=snapshot)

        if system_prompt:
            return identity + "\n\n" + system_prompt
        return identity
    

    def _adapt_messages(self, provider_name: str, messages: list[ConversationMessage]):
        if provider_name == "gpt":
            return MessageAdapter.to_openai(messages=messages)
        
        elif provider_name == "gemini":
            return {
                "contents": MessageAdapter.to_gemini(messages=messages)
            }
        
        elif provider_name == "local":
            return MessageAdapter.to_ollama(messages=messages)
        
        else:
            return messages


    async def ask(self, task: str, messages: list[ConversationMessage], system_prompt: str="", advisor: str | None = None) -> AdvisorResponse:

        print(f"\n[ADVISOR-SERVICE][DEBUG] Messages Received: {messages}")

        route = self.router.route(task=task)

        model = route["model"]

        provider_name = route["provider"]
        provider = self.providers[provider_name]

        system_prompt = await self._build_system_prompt(system_prompt=system_prompt)
        adapted_messages = self._adapt_messages(provider_name=provider_name, messages=messages)

        start = time.monotonic()

        try:
            print(f"\n[ADVISOR-SERVICE][DEBUG] Adapted Messages: {adapted_messages}")

            response = await provider.generate(
                model=model,
                messages=adapted_messages,
                system_prompt=system_prompt
            )

            success = True

        except Exception as e:
            print(f"\n[ADVISOR-SERVICE][ERROR] {type(e).__name__}: {e}")
            raise
        
            #response = None
            #success = False

        latency = time.monotonic() - start

        self.router.learn(
            task=task,
            model=model,
            success=success,
            latency=latency,
            score=0.9  # placeholder, can refine later
        )

        return response
