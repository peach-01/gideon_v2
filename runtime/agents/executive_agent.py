class ExecutiveAgent:

    def __init__(self, planner_agent, agent_registry, critic_agent):
        self.planner = planner_agent
        self.registry = agent_registry
        self.critic = critic_agent
        

    async def run(self, objective):
        plan = await self.planner.run(objective)

        results = {}

        for step in plan.steps:
            agent = self.registry.get(step.agent)

            results[step.id] = await agent.run(step.task)

            review = await self.critic.review(objective, results)

        return review