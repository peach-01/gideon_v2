import json
import re
from datetime import datetime

from models.python.memory.enums.memory_type import MemoryType
from models.python.memory.provenance import Provenance
from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage


# ------------- HELPER --------------
def parse_json_response(text):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    return json.loads(text.strip())


class MemoryExtractor:

    def __init__(self, advisor_service, memory_service, graph_memory):
        self.advisor = advisor_service
        self.memory = memory_service
        self.graph_memory = graph_memory


    async def extract(self, user_msg: str, gideon_response: str, message_id, episode_id):
        prompt = f"""
            Extract durable memories only from this interaction.
            Only return information likely to remain true or useful in the future.

            Extract (as a memory_type translated to singular tense):
            - facts
            - preferences
            - goals
            - projects
            - people
            - relationships
            - locations
            - workflows
            - life events
            - skills
            - decisions
            
            Return ONLY JSON.

            Example:
                Input:
                    "My wife Sarah loves hiking."

                Output:
                {
                    "memories": [
                        "content": "User is married to Sarah",
                        "memory_type": "relationship",
                        "importance": 0.9
                    ],

                    "edges": [
                        {
                            "source_entity": "user",
                            "relation": "married_to",
                            "target_entity": "Sarah",
                            "confidence": 1.0
                        },
                        {
                            "source_entity": "Sarah",
                            "relation": "likes",
                            "target_entity": "hiking",
                            "confidence": 0.95
                        }
                    ]
                }

            USER:
            {user_msg}

            GIDEON:
            {gideon_response}         
        """

        try:
            messages = [
                ConversationMessage(
                    role="user",
                    content=[
                        ContentBlock(
                            type="text",
                            content=prompt,
                        ),
                    ]
                )
            ],

            print(f"[DEBUG][MEMORY][{datetime.now():%X}] Prompt sent to API: {messages}")

            response = await self.advisor.ask(
                system_prompt="""
                    You are a memory extraction engine.
                    Only extract durable memories.
                    
                    Return JSON only.
                """,
                messages=messages,
                task="extraction"
            )

            print(f"[DEBUG][GIDEON][MEMORY][{datetime.now():%X}] {response}")

            results = (
                response.structured_date if response.structured_data
                else parse_json_response(response.content)
            )

            for m in results.get("memories", []):
                await self.memory.store(
                    content=m["content"],
                    memory_type=m.get("memory_type", MemoryType.FACT),
                    source="conversation",
                    importance=m.get("importance", 0.5),

                    provenance = Provenance(
                        message_id=message_id,
                        episode_id=episode_id,
                        source_type="conversation"
                    )
                )

            for e in results.get("edges", []):
                await self.graph_memory.add_edge(
                    source_entity=e["source_entity"],
                    relation=e["relation"],
                    target_entity=e["target_entity"],
                    confidence=e.get("confidence", 1.0),
                    origin_episode_id=episode_id,
                )

        except Exception as e:
            print(f"[MEMORY_EXTRACTOR] FAILED: {e}")