from models.python.awareness.cognitive_context import CognitiveContext

from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage

from models.python.awareness.cognitive_cache import SessionCache


class ContextBuilder:

    def __init__(self, memory_service, conversation_service, state_manager, identity_service, cache, goal_manager):
        self.memory = memory_service
        self.conversation = conversation_service
        self.state_manager = state_manager
        self.identity_service = identity_service
        self.cache = cache
        self.goals = goal_manager


    async def build(self, session_id: str, query: str, cache):
        state = self.state_manager.get_state(session_id)
        session = self.cache.sessions.setdefault(session_id, SessionCache())

        working_memory = [
            f"Active Goal: {state.active_goal}",
            f"Active Project: {state.active_project}",
            f"Current Task: {state.current_task}",
        ]

        recent_messages = self.conversation.get_last_messages(
            session_id=session_id,
            limit=20,
        )

        memories = await self.memory.search(
            query=query,
            memory_types=[
                "fact", "preference", "goal", "project", "person",
                "decision", "task", "skill", "system",
            ],
            limit=15,
        )
        
        self.cache.message.retrieval_results = memories

        session.last_memories = memories
        

        # check cache for goals before recomputing
        goals = session.goals

        if goals is None:
            goals = self.cache.boot.semantic_summary.goals
            session.goals = goals


        self_model_section = cache.boot.rendered_identity

        goal_lines = self._build_goals(goals)
        memory_lines = self._build_memories(memories)
        conversation_lines = self._build_conversation(recent_messages)

        return CognitiveContext(
            identity=self_model_section,
            working_state=working_memory,
            goals=goal_lines,
            memories=memory_lines,
            conversation=conversation_lines,
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