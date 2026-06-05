from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, llm):
        self.llm = llm

    @abstractmethod
    async def run(self, task):
        pass