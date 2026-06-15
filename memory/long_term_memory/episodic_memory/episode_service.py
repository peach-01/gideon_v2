import uuid
from episode_model import Episode
from datetime import datetime, UTC


class EpisodeService:

    def __init__(self, advisor):
        self.advisor = advisor


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

        return Episode(
            id=str(uuid.uuid4()),
            session_id=session_id,
            summary=summary,
            start_time=messages[0].timestamp,
            end_time=messages[-1].timestamp,
            importance=0.7,                     # placeholder
            emotional_weight=0.5,           # placeholder
            created_at=datetime.now(UTC)
        )