import json
from datetime import datetime

from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage


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
        
        messages=[
            ConversationMessage(
                role="user",
                content=[
                    ContentBlock(
                        type="text",
                        content=prompt,
                    )
                ]
            )
        ]
        
        print(f"[DEBUG][CRITIC][{datetime.now():%X}] Prompt sent to API: {messages}")
        
        response = await self.advisor.ask(
            task="critic",
            messages=messages,
        )

        print(f"[DEBUG][GIDEON][CRITIC][{datetime.now():%X}] {response}")

        return json.loads(response.content)