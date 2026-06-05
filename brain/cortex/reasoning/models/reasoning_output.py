from pydantic import BaseModel


class ToolRequest(BaseModel):
    tool: str
    args: dict


class ReasoningOutput(BaseModel):
    intent: str
    plan: list[str]
    required_tools: list[ToolRequest]