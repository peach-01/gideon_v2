import uuid
from datetime import datetime, UTC

from memory.memory_models.basic_memory.memory_type import MemoryType
from memory.memory_models.provenance import Provenance
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage


class EpisodeService:

    EPISODE_TIMEOUT = 900       # 15 minutes

    def __init__(self, advisor, memory_service):
        self.advisor = advisor
        self.memory = memory_service

        self.buffers = {}
        self.last_activity = {}

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



    # ---------- CORE -----------
    async def create_episode(self, session_id: str):
        
        events = self.buffers.get(session_id, [])

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

        print(f"[DEBUG][EPISODE] Prompt sent to API: {prompt}")

        response = await self.advisor.ask(
            task="summarization",
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
        )

        print(f"[GIDEON][EPISODE] {response}")

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