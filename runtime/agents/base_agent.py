from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, advisor_service):
        self.advisor = advisor_service

    @abstractmethod
    async def run(self, task):
        pass