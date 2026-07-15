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


class CognitionExtractor:

    def __init__(self, advisor_service, memory_service, graph_memory, entity_service, state_manager, goal_manager):
        self.advisor = advisor_service
        self.memory = memory_service
        self.graph_memory = graph_memory
        self.entity_service = entity_service
        self.state_manager = state_manager
        self.goal_manager = goal_manager


    async def extract(self, user_msg: str, gideon_response: str, message_id, episode_id, session_id, context):
        extract_model = {
            "memories":[
                {
                    "content":"",
                    "memory_type":"",
                    "importance":0.8
                }
            ],

            "edges":[
                {
                    "source_entity":"",
                    "relation":"",
                    "target_entity":"",
                    "confidence":1.0
                }
            ],

            "entities":[
                {
                    "name":"",
                    "entity_type":"person"
                }
            ],

            "goals":[
                {
                    "title":"",
                    "priority":0.8,
                    "status":"active"
                }
            ],

            "state_updates":{
                "active_goal":"",
                "active_project":"",
                "conversation_mode":"",
                "current_task":""
            }
        }
        

        prompt = f"""
            You are updating Gideon's persistent cognition.

            Given:

                Current working state:
                {context.working_state}

                User message:
                {user_msg}

                Assistant response:
                {gideon_response}

            Return JSON only.

            {json.dumps(extract_model, indent=2)}
        """

        try:
            messages = [
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

            print(f"[DEBUG][MEMORY][{datetime.now():%X}] Prompt sent to API: {messages}")

            response = await self.advisor.ask(
                messages=messages,
                task="extraction"
            )

            print(f"[DEBUG][GIDEON][MEMORY][{datetime.now():%X}] {response}")

            results = (
                response.structured_data if response.structured_data
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

            for e in results.get("entities", []):
                await self.entity_service.get_or_create(
                    name=e["name"],
                    entity_type=e["entity_type"],
                )

            for g in results.get("goals", []):

                # add a duplication check for active goals soon

                await self.goal_manager.create_goal(
                    title=g["title"],
                    priority=g["priority"],
                )


            self.state_manager.update(
                session_id,
                **results["state_updates"]
            )

        except Exception as e:
            print(f"[MEMORY_EXTRACTOR] FAILED: {e}")