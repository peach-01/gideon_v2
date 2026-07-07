import json
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage


class StateExtractor:

    def __init__(self, advisor_service):
        self.advisor = advisor_service

    async def extract(self, state, user_msg, gideon_msg):
        prompt = f"""
            Update working memory.

            Current State:
            {state}

            Conversation:

            USER:
            {user_msg}

            GIDEON:
            {gideon_msg}

            Return JSON only:

            {{
                "active_goal": "...",
                "active_project": "...",
                "current_task": "...",
                "conversation_mode": "chat"
            }}
            """
        
        print(f"[DEBUG][STATE] Prompt sent to API: {prompt}")

        result = await self.advisor.ask(
            task="extraction", 
            messages=[
                ConversationMessage(
                    role="user",
                    content=[
                        ContentBlock(
                            type="text", 
                            content=prompt,
                        ),
                    ],
                )
            ]
        )

        print(f"[GIDEON][STATE] {result}")

        if result.structured_data:
            return result.structured_data
        
        return json.loads(result.content)