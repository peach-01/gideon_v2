from runtime.providers.openai_provider import OpenAIProvider
from runtime.providers.claude_provider import ClaudeProvider
from runtime.providers.gemini_provider import GeminiProvider
from runtime.providers.local_provider import LocalProvider

from nervous_system.signal_bus.routing.advisor_router import AdvisorRouter


class AdvisorService:

    def __init__(self):
        self.router = AdvisorRouter()
        self.providers = {
            "gpt": OpenAIProvider(),
            "claude": ClaudeProvider(),
            "gemini": GeminiProvider(),
            "local": LocalProvider(),
        }

    async def ask(self, task: str, prompt: str, system_prompt: str="", advisor: str | None = None):
        advisor_name = advisor or self.router.choose(task)

        provider = self.providers[advisor_name]

        return await provider.generate(task=task, prompt=prompt, system_prompt=system_prompt)