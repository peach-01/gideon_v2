from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    async def generate(self, task: str, prompt: str, system_prompt: str=""):
        pass