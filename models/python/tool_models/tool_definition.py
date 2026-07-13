from pydantic import BaseModel
from typing import Callable


class ToolDefinition:

    def __init__(self, function: Callable, request_model: type[BaseModel], description: str):
        self.func = function
        self.request_model = request_model
        self.desc = description


    def model_to_openai_schema(self, model: type[BaseModel]):
        schema = model.model_json_schema()

        return {
            "type": "function",
            "function": {
                "name": model.__name__,
                "description": "",
                "parameters": schema,
            }
        }

    def build_openai_tool(self, func, request_model, desc=""):
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": desc,
                "parameters": request_model.model_json_schema(),
            }
        },