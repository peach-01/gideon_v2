from dataclasses import dataclass, field


@dataclass
class CognitiveContext:

    identity: str

    working_state: list

    goals: list[str] = field(default_factory=list)

    memories: list[str] = field(default_factory=list)
    
    conversation: list[str] = field(default_factory=list)


    def render(self):

        goals = "\n".join(self.goals) if self.goals else "None"

        memories = "\n".join(self.memories) if self.memories else "None"

        conversation = (
            "\n".join(self.conversation)
            if self.conversation
            else "No conversation history"
        )

        return f"""
            IDENTITY:
            {self.identity}


            WORKING MEMORY:
            {self.working_state}


            GOALS:
            {goals}


            MEMORIES:
            {memories}


            CONVERSATION:
            {conversation}
        """.strip()