from pydantic import BaseModel


class ToolResult(BaseModel):

    success: bool
    tool: str
    action: str

    data: dict | None = None
    error: str | None = None

    duration_ms: int