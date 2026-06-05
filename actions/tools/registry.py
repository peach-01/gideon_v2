from actions.tools.tool_models.tool_definition import ToolDefinition


class ToolRegistry:

    def __init__(self, tool_definition: ToolDefinition):
        self.tools = {}
        self.definition = tool_definition

    def register(self, func, request_model, desc=""):
        self.tools[func.__name__] = {
            "function": func,
            "model": request_model,
            "description": desc,
        }

    def get(self, name):
        return self.tools[name]

    def schemas(self):
        return [
            self.definition.build_openai_tool(
                func=item["function"],
                request_model=item["model"],
                desc=item["description"]
            )
            for item in self.tools.values()
        ]