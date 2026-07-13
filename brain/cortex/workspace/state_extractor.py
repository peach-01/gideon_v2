import json
from datetime import datetime
from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage


class StateExtractor:

    def __init__(self, advisor_service):
        self.advisor = advisor_service


    async def boot(self):
        print("[STATE-MANAGER] Ready.")


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
        
        messages = [
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
        
        print(f"[DEBUG][STATE][{datetime.now():%X}] Prompt sent to API: {messages}")

        result = await self.advisor.ask(
            task="extraction", 
            messages=messages
        )

        print(f"[DEBUG][GIDEON][STATE][{datetime.now():%X}] {result}")

        if result.structured_data:
            return result.structured_data
        
        return json.loads(result.content)