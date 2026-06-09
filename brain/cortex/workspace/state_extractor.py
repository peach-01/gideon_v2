import json


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
        
        result = await self.advisor.ask(task="extraction", prompt=prompt)

        return json.loads(result)