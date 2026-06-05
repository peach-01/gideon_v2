class ToolDispatcher:

    def __init__(self, tool_service):
        self.tool_service = tool_service


    async def execute(self, tool_name, action, **kwargs):
        tool = self.tool_service.get_tool(tool_name)

        fn = getattr(tool, action)

        return await fn(**kwargs)