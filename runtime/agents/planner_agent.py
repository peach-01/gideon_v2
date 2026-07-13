import json
from datetime import datetime

from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage


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
        
        print(f"[DEBUG][PLANNER][{datetime.now():%X}] Prompt sent to API: {messages}")
        
        response = await self.advisor.ask(
            task="planning",
            messages=messages,
        )

        print(f"[DEBUG][GIDEON][PLANNER][{datetime.now():%X}] {response}")
        
        return json.loads(response.content)