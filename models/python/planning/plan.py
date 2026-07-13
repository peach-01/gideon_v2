from pydantic import BaseModel


class PlanStep(BaseModel):

    id: str
    agent: str
    task: str
    dependencies: list[str] = []


class Plan(BaseModel):

    goal: str
    steps: list[PlanStep]