from dataclasses import dataclass
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock


@dataclass
class ConversationMessage:

    role: str
    content: list[ContentBlock]