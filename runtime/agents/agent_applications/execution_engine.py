from actions.tools.serializer import serialize


class ExecutionEngine:

    def __init__(self, registry):
        self.registry = registry


    async def run(self, plan):
        for step in plan.steps:
            tool = self.registry.get(step.tool)

            result = await tool.execute(action=step.action, params=step.args)

            result = serialize(result)