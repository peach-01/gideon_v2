import json

from memory.memory_models.memory_type import MemoryType
from runtime.orchestrator import parse_json_response

class MemoryExtractor:

    def __init__(self, advisor_service, memory_service, graph_memory):
        self.advisor = advisor_service
        self.memory = memory_service
        self.graph_memory = graph_memory


    async def extract(self, user_msg: str, gideon_response: str):
        prompt = f"""
            Extract durable memories only.

            Rules:
            - Extract durable facts
            - Extract user preferences
            - Extract goals
            - Extract projects
            - Extract people
            - Extract relationships
            - Extract locations
            - Extract workflows
            - Extract life events
            - Extract skills
            - Extract important decisions

            - Ignore temporary requests
            - Ignore greetings
            - Ignore conversational fluff
            - Ignore small talk

            Valid memory_types:
                fact
                preference
                goal
                project
                person
                relationship
                location
                workflow
                life_event
                skill
                decision

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
            results = await self.advisor.ask(
                system_prompt="""
                    You are a memory extraction engine.
                    Only extract durable memories.
                    Return JSON only.
                """,
                prompt=prompt,
                task="extraction"
            )

            memories = parse_json_response(results)

            for m in results["memories"]:
                await self.memory.store(
                    content=m["memories"],
                    memory_type=m.get("memory_type", MemoryType.FACT),
                    source="conversation",
                    importance=m.get("importance", 0.5),
                )

            for e in results["edges"]:
                await self.graph_memory.add_edge(
                    source_entity=e["source_entity"],
                    relation=e["relation"],
                    target_entity=e["target_entity"],
                    confidence=e.get("confidence", 1.0),
                )

        except Exception as e:
            print(f"[MEMORY_EXTRACTOR] FAILED: {e}")