from dataclasses import dataclass, field

from models.python.conversation.converstation_message import ConversationMessage
from models.python.awareness.cognitive_context import CognitiveContext


@dataclass
class ProcessingContext:

    session_id: str
    
    user_message: str
    user_message_id: str | None = None

    cognitive_context: CognitiveContext | None = None
    prompt: str = ""

    llm_messages: list[ConversationMessage] = field(default_factory=list)
    tool_results: list[ConversationMessage] = field(default_factory=list)

    answer: str = ""

    state: dict = field(default_factory=dict)

    episode_id: str | None = None