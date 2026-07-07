from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage


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
        
        response = await self.advisor.ask(
            task="research",
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
        )        

        return response.content