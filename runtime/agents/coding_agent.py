from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage


class CodingAgent:

    def __init__(self, advisor_service):
        self.advisor = advisor_service


    async def run(self, task):
        prompt = f"""
            Coding Task:
            {task}

            Return Implementation.
            """
        
        response = await self.advisor.ask(
            task="coding",
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