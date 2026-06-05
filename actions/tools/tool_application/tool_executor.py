import json

from nervous_system.signal_bus.routing.tool_router import ToolRouter
from actions.tools.serializer import serialize


class ToolExecutor:

    def __init__(self):
        self.tool_router = ToolRouter()

    
    async def execute(self, tool_calls):
        results = []

        for call in tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")

            result = await self.tool_router.execute_tool(name=name, args=args)
            result = serialize(result)
            
            results.append({
                "tool_call_id": call.id,
                "role": "tool",
                "name": name,
                "content": json.dumps(result, default=str),
            })

        return results