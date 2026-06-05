class CodingAgent:

    def __init__(self, llm):
        self.llm = llm


    async def run(self, task):
        prompt = f"""
            Coding Task:
            {task}

            Return Implementation.
            """
        
        return await self.llm.generate(prompt, task="coding")