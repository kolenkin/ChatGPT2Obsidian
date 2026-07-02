import json
from pathlib import Path

from .models import Conversation, Message


class ChatParser:

    def __init__(self, filename):
        self.filename = Path(filename)

    def load(self):

        with self.filename.open("r", encoding="utf-8") as f:
            raw = json.load(f)

        conversations = []

        for chat in raw:

            conversation = Conversation(
                id=chat.get("id", ""),
                title=chat.get("title", "Untitled"),
            )

            mapping = chat.get("mapping", {})

            for node in mapping.values():

                message = node.get("message")

                if not message:
                    continue

                content = message.get("content", {})

                if content.get("content_type") != "text":
                    continue

                parts = content.get("parts", [])

                if not parts:
                    continue

                text = "\n".join(
                    str(part)
                    for part in parts
                    if part
                )

                role = message.get("author", {}).get("role", "unknown")

                conversation.messages.append(
                    Message(
                        role=role,
                        text=text,
                    )
                )

            conversations.append(conversation)

        return conversations