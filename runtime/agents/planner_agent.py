import json


class PlannerAgent:

    def __init__(self, llm):
        self.llm = llm


    async def run(self, context, user_request):
        prompt = f"""
            User Request:
            {user_request}

            Context:
            {context}

            Available Tools:
            ...

            Return JSON:
            {{
                "goal": "...",
                "steps": [
                    {{
                        "agent": "research",
                        "task": "..."
                    }}
                ]
            }}
            """
        
        result = await self.llm.generate(prompt, task="planning")
        
        return json.loads(result)