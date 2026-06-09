import json


class PlannerAgent:

    def __init__(self, advisor_service):
        self.advisor = advisor_service


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
        
        result = await self.advisor.ask(prompt=prompt, task="planning")
        
        return json.loads(result)