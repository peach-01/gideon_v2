from models.python.awareness.cognitive_context import CognitiveContext

from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage

from models.python.awareness.cognitive_cache import SessionCache


class ContextBuilder:

    def __init__(self, conversation_service, state_manager, cache_service, memory_service):
        self.conversation = conversation_service
        self.state_manager = state_manager
        self.memory_service = memory_service
        self.cache = cache_service


    async def build(self, session_id: str, query: str, cache):
        boot = cache.boot
        session = cache.sessions.setdefault(session_id, SessionCache())
        message = cache.message

        state = self.state_manager.get_state(session_id)

        working_memory = [
            f"Active Goal: {state.active_goal}",
            f"Active Project: {state.active_project}",
            f"Current Task: {state.current_task}",
        ]

        recent_messages = self.conversation.get_last_messages(
            session_id=session_id,
            limit=20,
        )

        memories = await self.memory_service.search(
            query=query,
            memory_types=[
                "fact", "preference", "goal", "project", "person",
                "decision", "task", "skill", "system",
            ],
            limit=15,
        )
        
        message.retrieval_results = memories
        session.last_memories = memories

        # check cache for goals before recomputing
        if session.goals is None:
            semantic = boot.semantic_summary

            if semantic:
                session.goals = semantic.goals
            else:
                session.goals = []

        return CognitiveContext(
            identity = boot.rendered_identity,
            working_state = working_memory,
            goals = self._build_goals(session.goals),
            memories = self._build_memories(memories),
            conversation = self._build_conversation(recent_messages),
        )
    


    # ------------ FORMATTERS -------------
    def _build_goals(self, goals):
        if not goals:
            return "None"

        return [
            f"{goal.title} (priority={goal.priority})"
            for goal in goals
        ]


    def _build_memories(self, memories):
        if not memories:
            return "None"

        return [
            f"[{m.memory_type}] {m.context}"
            for m in memories
        ]


    def _build_conversation(self, messages: list[ConversationMessage]):
        if not messages:
            return "No conversation history"

        return [
            f"{msg.role}: {self._flatten_content(msg.content)}"
            for msg in messages
        ]


    # ---------- HELPERS -----------
    def _flatten_content(self, blocks: list[ContentBlock]):
        return " ".join(
            block.content
            for block in blocks
            if block.type == "text"
        )