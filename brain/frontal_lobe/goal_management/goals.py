class GoalTool:

    name = "goals"

    def __init__(self, memory_service, goal_manager):
        self.memory = memory_service
        self.manager = goal_manager

    async def create_goal(self, title, description="", priority=0.8):
        return await self.manager.create_goal(title=title, description=description, priority=priority)

    async def list_goals(self):
        return await self.manager.get_active_goals()

    async def complete_goal(self, goal_id):
        return await self.manager.complete_goal(goal_id=goal_id)