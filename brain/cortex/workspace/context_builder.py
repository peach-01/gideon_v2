from brain.frontal_lobe.goal_management.goal_service import GoalService

from mind.self_model.self_model_service import SelfModelService
from mind.self_model.self_model_formatter import SelfModelFormatter

from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage


class ContextBuilder:

    def __init__(self, memory_service, conversation_service, state_manager, identity_service):
        self.memory = memory_service
        self.conversation = conversation_service
        self.state_manager = state_manager
        self.identity_service = identity_service

        self.goals = GoalService(memory_service=self.memory)
        self.self_model = SelfModelService(memory_service=self.memory, identity_service=self.identity_service)
        self.self_model_formatter = SelfModelFormatter()


    async def build(self, session_id: str, query: str):
        state = self.state_manager.get_state(session_id)

        working_memory = f"""
            ACTIVE GOAL:
            {state.active_goal}

            ACTIVE PROJECT:
            {state.active_project}

            CURRENT TASK:
            {state.current_task}
        """

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

        goals = await self.goals.list_goals(active_only=True)
        self_snapshot = await self.self_model.snapshot()

        self_model_section = self.self_model_formatter.format(snapshot=self_snapshot)
        goals_section = self._build_goals(goals)
        memory_section = self._build_memories(memories)
        conversation_section = self._build_conversation(recent_messages)

        return f"""
            SELF MODEL
            {self_model_section}

            WORKING MEMORY
            {working_memory}

            ACTIVE GOALS
            {goals_section}

            RELEVANT MEMORIES
            {memory_section}

            RECENT CHAT
            {conversation_section}
        """
    

    # ------------ FORMATTERS -------------
    def _build_goals(self, goals):
        if not goals:
            return "None"

        return "\n".join(
            f"- {goal.title} (priority={goal.priority})"
            for goal in goals
        )

    def _build_memories(self, memories):
        if not memories:
            return "None"

        return "\n".join(
            f"- [{m.memory_type}] {m.context}"
            for m in memories
        )

    def _build_conversation(self, messages: list[ConversationMessage]):
        if not messages:
            return "No conversation history"

        return "\n".join(
            f"{msg.role}: {self._flatten_content(msg.content)}"
            for msg in messages
        )


    # ---------- HELPERS -----------
    def _flatten_content(self, blocks: list[ContentBlock]):
        return " ".join(
            block.content
            for block in blocks
            if block.type == "text"
        )