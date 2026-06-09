import json


class CriticAgent:

    def __init__(self, advisor_service):
        self.advisor = advisor_service


    async def review(self, user_request, answer):
        prompt = f"""
            User Request:
            {user_request}

            Response:
            {answer}

            Evaluate:
            {{
                "approved": true,
                "issues": [],
                "score": 0.0,
            }}
            """
        
        result = await self.advisor.ask(prompt=prompt, task="critic")

        return json.loads(result)