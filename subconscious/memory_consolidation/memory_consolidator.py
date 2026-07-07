import json
from datetime import datetime, UTC, timedelta

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import MessageRecord

from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage


class MemoryConsolidator:

    def __init__(self, advisor_service, memory_service):
        self.advisor = advisor_service
        self.memory = memory_service


    async def consolidate(self):
        db = SessionLocal()

        try:
            cutoff = datetime.now(UTC) - timedelta(days=1)

            messages = db.query(MessageRecord).filter(MessageRecord.timestamp < cutoff)\
                .order_by(MessageRecord.timestamp.asc()).all()

            if not messages:
                return
            
            transcript = "\n".join([
                f"{m.role}: {m.content}" for m in messages
            ])

            summaries = await self._extract_episodic_memories(transcript)

            for memory in summaries:
                await self.memory.store(
                    content=memory["content"],
                    memory_type=memory["memory_type"],
                    source="memory_consolidator",
                    importance=memory["importance"],
                )

            self._delete_redundant_messages(db, messages)

            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


    async def _extract_episodic_memories(self, transcript: str):
        prompt = f"""
            You are a memory consolidation engine.

            Convert conversation fragments into long-term episodic memories.

            Rules:
            - Merge duplicates
            - Remove conversational fluff
            - Focus on projects, goals, preferences, decision, skills, and important events
            - Produce only durable memories

            Use these categories as memory_types:
                "fact", "preference", "goal", "project", "person", "conversation", "task", "decision", "skill", "system"

            Return ONLY JSON:
            [
                {{
                    "content": "User is actively developing Project A and recently completed memory system implementation.",
                    "memory_type": "project",
                    "importance": 0.8
                }}
            ]

            Conversation:

            {transcript}
        """

        system_prompt = """
            You are performing memory consolidation.

            Convert conversations into durable memories that produce valuable insights.
            Return JSON only.
        """,

        result = await self.advisor.ask(
            system_prompt=system_prompt,
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
            ],
            task="summarization",
        )

        return json.loads(result.content)


    def _delete_redundant_messages(self, db, messages):
        ids = [m.id for m in messages]

        db.query(MessageRecord).filter(MessageRecord.id.in_(ids)).delete(synchronize_session=False)