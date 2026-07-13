from datetime import datetime

from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage


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
        
        print(f"[DEBUG][RESEARCH][{datetime.now():%X}] Prompt sent to API: {messages}")
        
        response = await self.advisor.ask(
            task="research",
            messages=messages,
        )

        print(f"[DEBUG][GIDEON][RESEARCH][{datetime.now():%X}] {response}")

        return response.content