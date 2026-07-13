from actions.tools.tool_application.tool_service import ToolService


class ToolRouter:

    def __init__(self, memory_service):
        self.memory = memory_service

        self.tool_service = ToolService(self.memory)
        self.routes = self.tool_service.get_func_map()


    async def execute_tool(self, name: str, args: dict):
        tool_func = self.routes.get(name)

        if not tool_func:
            raise ValueError(f"Unknown tool: {name}")

        return await tool_func(**args)