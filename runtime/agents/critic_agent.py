import json
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage


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
        
        response = await self.advisor.ask(
            task="critic",
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

        return json.loads(response.content)