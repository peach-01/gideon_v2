class MemoryAgent:

    def __init__(self, advisor_service, memory_service):
        self.advisor = advisor_service
        self.memory_service = memory_service


    async def recall(self, query):
        return await self.memory_service.search(query)


    async def store(self, content, memory_type, importance):        
        return await self.memory_service.store(content, memory_type, importance=importance)