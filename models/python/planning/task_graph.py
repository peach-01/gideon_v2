from pydantic import BaseModel


class TaskNode(BaseModel):
    id: str
    agent: str
    task: str
    dependencies: list[str] = []


class TaskGraph(BaseModel):
    goal: str
    nodes: list[TaskNode]