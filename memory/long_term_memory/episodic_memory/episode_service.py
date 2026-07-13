import uuid
import asyncio

from datetime import datetime, UTC

from models.python.memory.enums.memory_type import MemoryType
from models.python.memory.provenance import Provenance
from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage


class EpisodeService:

    EPISODE_TIMEOUT = 900       # 15 minutes

    def __init__(self, advisor, memory_service):
        self.advisor = advisor
        self.memory = memory_service

        self.buffers = {}
        self.last_activity = {}

        self.active_jobs = set()


    async def boot(self):
        print("[EPISODE] Ready.")


    # ---------- HELPERS ----------
    # only store dialogue
    def render_dialogue(self, messages):
        lines = []

        for msg in messages:
            if msg.role == "system":
                continue
            
            text = "\n".join(
                block.content
                for block in msg.content
                if block.type == "text"
            )

            lines.append(f"{msg.role}: {text}")

        return "\n".join(lines)
    

    # cache conversations in local events
    async def add_interaction(self, session_id: str, user_msg: str, gideon_msg: str):
        now = datetime.now(UTC)

        if session_id not in self.buffers:
            self.buffers[session_id] = []

        self.buffers[session_id].append(
            {
                "user": user_msg,
                "gideon": gideon_msg,
                "timestamp": now,
            }
        )

        self.last_activity[session_id] = now


    async def should_finalize_episode(self, session_id: str):
        if session_id not in self.last_activity:
            return False
        
        elapsed = (datetime.now(UTC) - self.last_activity[session_id]).total_seconds()

        if elapsed > self.EPISODE_TIMEOUT:
            return True
        
        return len(self.buffers[session_id]) >= 20
    

    async def schedule_finalize(self, session_id: str):
        if session_id in self.active_jobs:
            return 
        
        if not await self.should_finalize_episode(session_id):
            return
        
        self.active_jobs.add(session_id)
        
        asyncio.create_task(self._background_finalize(session_id))


    async def _background_finalize(self, session_id):
        try:
            await self.finalize_episode(session_id)

        finally:
            self.active_jobs.discard(session_id)


    # ---------- CORE -----------
    async def finalize_episode(self, session_id: str):
        
        events = self.buffers.pop(session_id, [])
        self.last_activity.pop(session_id, None)

        # skip tiny conversations for more meaningful interactions
        if len(events) < 3:
            return None
        
        transcript = "\n\n".join(
            f"User: {e['user']}\n"
            f"GIDEON: {e['gideon']}"
            for e in events
        )

        prompt = f"""
            Create a concise episodic memory from the transcript provided below.

            Include:
            - what happened
            - important decisions
            - goals discussed
            - facts learned
            - future commitments

            Do NOT include greetings or small talk.

            Transcript:
            {transcript}
        """

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
        ]

        print(f"[DEBUG][EPISODE][{datetime.now():%X}] Prompt sent to API: {messages}")

        response = await self.advisor.ask(
            task="summarization",
            messages=messages,
        )

        print(f"[DEBUG][GIDEON][EPISODE][{datetime.now():%X}] {response}")

        summary = response.content

        episode_id = str(uuid.uuid4())

        await self.memory.store(
            content=summary,
            memory_type=MemoryType.EPISODE,
            source="conversation",

            importance=0.7,      # placeholder

            provenance=Provenance(episode_id=episode_id),
        )

        self.buffers.pop(session_id, None)
        self.last_activity.pop(session_id, None)

        return episode_id