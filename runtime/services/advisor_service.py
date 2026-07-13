import asyncio
import time

from runtime.providers.message_adapter import MessageAdapter

from models.python.conversation.advisor_response import AdvisorResponse
from models.python.conversation.converstation_message import ConversationMessage


class AdvisorService:

    _semaphore = asyncio.Semaphore(1)
    _last_request_time = 0.0
    _min_interval = 3.0     # seconds


    def __init__(self, intelligent_router, providers: dict):
        self.router = intelligent_router
        self.providers = providers


    async def boot(self):
        print("[ADVISOR] Ready.")
    

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


    async def ask(self, task: str, messages: list[ConversationMessage], system_prompt: str = "") -> AdvisorResponse:

        #print(f"\n[ADVISOR-SERVICE][DEBUG] Messages Received: {messages}")

        route = self.router.route(task=task)

        model = route["model"]

        provider_name = route["provider"]
        provider = self.providers[provider_name]

        adapted_messages = self._adapt_messages(provider_name=provider_name, messages=messages)

        start = time.monotonic()

        try:
            #print(f"\n[ADVISOR-SERVICE][DEBUG] Adapted Messages: {adapted_messages}")

            response = await provider.generate(
                model=model,
                messages=adapted_messages,
                system_prompt=system_prompt
            )

            success = True

        except Exception as e:
            #print(f"\n[ADVISOR-SERVICE][ERROR] {type(e).__name__}: {e}")
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
