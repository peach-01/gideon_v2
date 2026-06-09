class AdvisorTool:

    name = "model"

    def __init__(self, advisor_service):
        self.advisor = advisor_service


    async def ask(self, task: str, prompt: str, system_prompt: str = "", advisor=None):
        return await self.advisor.ask(advisor=advisor, prompt=prompt, system_prompt=system_prompt, task=task)