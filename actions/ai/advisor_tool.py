from models.python.conversation.converstation_message import ConversationMessage

class AdvisorTool:

    name = "model"

    def __init__(self, advisor_service):
        self.advisor = advisor_service


    async def ask(self, task: str, messages: list[ConversationMessage], system_prompt: str = ""):
        return await self.advisor.ask(messages=messages, system_prompt=system_prompt, task=task)