class ResearchAgent:

    def __init__(self, advisor_service, web_search):
        self.advisor = advisor_service
        self.web_search = web_search


    async def run(self, task):
        results = await self.web_search.search(task)

        prompt = f"""
            Research Task:
            {task}

            Sources:
            {results}

            Produce:
            {{
                "summary": "...",
                "sources": []
            }}
            """
        
        return await self.advisor.ask(prompt=prompt, task="reasoning")