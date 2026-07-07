class ExecutionAgent:

    def __init__(self, tool_executor):
        self.tool_executor = tool_executor


    async def run(self, tool_calls):
        return await self.tool_executor.execute(tool_calls)