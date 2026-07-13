from google.genai import types
from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage


class MessageAdapter:

    @staticmethod
    def to_openai(messages: list[ConversationMessage]) -> list[dict]:
        result = []

        for msg in messages:
            parts = []

            for block in msg.content:

                if block.type == "text":
                    parts.append({
                        "type": "text",
                        "text": block.content,
                    })

                elif block.type == "image":
                    parts.append({
                        "type": "image_url",
                        "image_url": {
                            "url": block.content,
                        }
                    })

            result.append({
                "role": msg.role,
                "content": parts,
            })

        return result
    

    @staticmethod
    def to_gemini(messages: list[ConversationMessage]):

        result = []

        for msg in messages:
            parts = []

            for block in msg.content:

                if block.type == "text":
                    parts.append(
                        types.Part.from_text(
                            text=block.content
                        )
                    )

                elif block.type == "image":
                    parts.append(
                        types.Part.from_uri(
                            file_uri=block.content,
                            mime_type="image/jpeg"
                        )
                    )

            role = "user"

            if msg.role in ["assistant", "gideon"]:
                role = "model"

            result.append(
                types.Content(
                    role=role,
                    parts=parts
                )
            )

        return result
    

    @staticmethod
    def to_ollama(messages: list[ConversationMessage]) -> list[dict]:
        result = []

        for msg in messages:

            text = "\n".join(
                block.content
                for block in msg.content
                if block.type == "text"
            )

            role = msg.role

            if role == "gideon":
                role = "assistant"

            result.append({
                "role": role,
                "content": text,
            })

        return result