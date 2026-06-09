class CodingAgent:

    def __init__(self, advisor_service):
        self.advisor = advisor_service


    async def run(self, task):
        prompt = f"""
            Coding Task:
            {task}

            Return Implementation.
            """
        
        return await self.advisor.ask(prompt=prompt, task="coding")