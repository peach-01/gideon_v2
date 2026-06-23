from google.genai import types
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock


class MessageAdapter:

    @staticmethod
    def to_openai(messages: list[dict]) -> list[dict]:
        result = []

        for msg in messages:
            role = msg["role"]

            parts = []

            for block in msg["content"]:

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
                "role": role,
                "content": parts,
            })

        return result
    

    @staticmethod
    def to_gemini(messages: list[dict]):

        result = []

        for msg in messages:

            parts = []

            for block in msg["content"]:

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

            if msg["role"] in ["assistant", "gideon"]:
                role = "model"

            result.append(
                types.Content(
                    role=role,
                    parts=parts
                )
            )

        return result