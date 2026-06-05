import json


class StateExtractor:

    def __init__(self, llm):
        self.llm = llm

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
        
        result = await self.llm.generate(user_prompt=prompt)

        return json.loads(result)