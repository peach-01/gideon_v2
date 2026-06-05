import json

from memory.models.memory_type import MemoryType
from brain.cortex.orchestrator import parse_json_response

class MemoryExtractor:

    def __init__(self, llm, memory_service):
        self.llm = llm
        self.memory = memory_service


    async def extract(self, user_msg: str, gideon_response: str):
        prompt = f"""
            Extract durable memories.

            Rules:
            - Store long-term useful facts only
            - Store user preferences
            - Store goals
            - Store projects
            - Store important decisions
            - Ignore temporary requests
            - Ignore greetings
            - Ignore conversational fluff
            - Ignore small talk

            Return ONLY JSON:
            [
                {{
                    "content": "...",
                    "memory_type": "fact",
                    "importance": 0.8
                }}
            ]

            USER:
            {user_msg}

            GIDEON:
            {gideon_response}         
        """

        try:
            results = await self.llm.generate(
                system_prompt="""
                    You are a memory extraction engine.
                    Only extract durable memories.
                    Return JSON only.
                """,
                user_prompt=prompt,
            )

            memories = parse_json_response(results)

            for m in memories:
                await self.memory.store(
                    content=m["content"],
                    memory_type=m.get("memory_type", MemoryType.FACT),
                    source="conversation",
                    importance=m.get("importance", 0.5),
                )

        except Exception as e:
            print(f"[MEMORY_EXTRACTOR] FAILED: {e}")