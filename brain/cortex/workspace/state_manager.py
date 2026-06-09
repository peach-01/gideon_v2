from pydantic import BaseModel, Field


class SessionState(BaseModel):

    active_goal: str | None = None

    active_project: str | None = None

    current_task: str | None = None

    conversation_mode: str = "chat"

    tool_chain: list[str] = Field(default_factory=list)