from brain.frontal_lobe.goal_management.goal_service import GoalService
from mind.self_model.identity_service import IdentityService


class ContextBuilder:

    def __init__(self, memory_service, conversation_service, state_manager):
        self.memory = memory_service
        self.conversation = conversation_service
        self.state_manager = state_manager

        self.goals = GoalService()
        self.identity = IdentityService()


    async def build(self, session_id: str, query: str):
        state = self.state_manager.get_state(session_id)

        working_memory = f"""
            ACTIVE GOAL:
            {state.active_goal}

            ACTIVE PROJECT:
            {state.active_project}

            CURRENT TASK:
            {state.current_task}

            MODE:
            {state.conversation_mode}
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

        identity_section = self._build_identity()
        goals_section = self._build_goals(goals)
        memory_section = self._build_memories(memories)
        conversation_section = self._build_conversation(recent_messages)

        return f"""
            IDENTITY
            {identity_section}

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
    def _build_identity(self):
        principles = "\n".join(f"- {p}" for p in self.identity.identity["principles"])

        return f"""
            Name: {self.identity.name}
            Version: {self.identity.version}

            Purpose:
            {self.identity.identity["identity"]["purpose"]}

            Mission:
            {self.identity.identity["identity"]["mission"]}

            Principles:
            {principles}
        """

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

    def _build_conversation(self, messages):
        if not messages:
            return "No conversation history"

        return "\n".join(
            f"{m.role}: {m.content}"
            for m in messages
        )