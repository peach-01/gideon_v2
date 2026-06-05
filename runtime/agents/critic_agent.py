import json


class CriticAgent:

    def __init__(self, llm):
        self.llm = llm


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
        
        result = await self.llm.generate(prompt, task="critic")

        return json.loads(result)