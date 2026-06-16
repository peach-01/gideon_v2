from memory.memory_models.basic_memory.memory_type import MemoryType
from memory.memory_models.provenance import Provenance


class EpisodeService:

    def __init__(self, advisor, memory_service):
        self.advisor = advisor
        self.memory = memory_service


    async def create_episode(self, session_id: str, messages: list):
        if not messages:
            return None
        
        transcript = "\n".join(f"{m.role}: {m.content}" for m in messages)

        summary = await self.advisor.ask(
            task="summarization",
            prompt=f"""
                Summarize this conversation as a durable episodic memory.

                Transcript:
                {transcript}
                """
        )

        await self.memory.store(
            content=summary,
            memory_type=MemoryType.EPISODE,
            source="conversation",

            importance=0.7,             # placeholder

            provenance=Provenance(episode_id=session_id),

            metadata={
                "session_id": session_id,
                "start_time": str(messages[0].timestamp),
                "end_time": str(messages[-1].timestamp),
                "message_count": len(messages)
            }
        )