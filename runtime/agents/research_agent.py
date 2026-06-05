class ResearchAgent:

    def __init__(self, llm, web_search):
        self.llm = llm
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
        
        return await self.llm.generate(prompt, task="reasoning")