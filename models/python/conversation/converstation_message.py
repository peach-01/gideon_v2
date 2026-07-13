from dataclasses import dataclass
from models.python.conversation.content_block import ContentBlock


@dataclass
class ConversationMessage:

    role: str
    content: list[ContentBlock]