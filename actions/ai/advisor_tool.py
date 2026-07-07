from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage

class AdvisorTool:

    name = "model"

    def __init__(self, advisor_service):
        self.advisor = advisor_service


    async def ask(self, task: str, messages: list[ConversationMessage], system_prompt: str = "", advisor=None):
        return await self.advisor.ask(advisor=advisor, messages=messages, system_prompt=system_prompt, task=task)