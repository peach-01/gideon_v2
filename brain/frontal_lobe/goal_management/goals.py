from brain.frontal_lobe.goal_management.goal_service import GoalService


class GoalTool:

    name = "goals"

    def __init__(self, memory_service):
        self.memory = memory_service
        self.service = GoalService(memory_service=self.memory)

    async def create_goal(self, title, description="", priority=0.8):
        return await self.service.create_goal(title=title, description=description, priority=priority)

    async def list_goals(self):
        return await self.service.list_goals()

    async def complete_goal(self, goal_id):
        return await self.service.complete_goal(goal_id=goal_id)