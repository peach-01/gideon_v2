import json
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage


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
        
        response = await self.advisor.ask(
            task="planning",
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