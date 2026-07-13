from datetime import datetime

from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage


class CodingAgent:

    def __init__(self, advisor_service):
        self.advisor = advisor_service


    async def run(self, task):
        prompt = f"""
            Coding Task:
            {task}

            Return Implementation.
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

        print(f"[DEBUG][CODING][{datetime.now():%X}] Prompt sent to API: {messages}")
        
        response = await self.advisor.ask(
            task="coding",
            messages=messages,
        )

        print(f"[DEBUG][GIDEON][CODING][{datetime.now():%X}] {response}")

        return response.content