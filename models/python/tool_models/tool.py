from abc import ABC, abstractmethod


class Tool(ABC):

    name: str
    description: str
    schema: dict

    @abstractmethod
    async def execute(self, action: str, params: dict):
        pass