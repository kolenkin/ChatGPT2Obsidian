"""
Data models for ChatGPT conversations.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class AuthorRole(str, Enum):
    """Enumeration of possible message author roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


@dataclass
class Message:
    """
    Represents a single message in a conversation.
    
    Attributes:
        role: The role of the message author.
        content: The text content of the message.
        model: The model used to generate the message (if applicable).
        timestamp: The Unix timestamp of the message creation.
    """
    role: AuthorRole
    content: str
    model: Optional[str] = None
    timestamp: Optional[float] = None


@dataclass
class Conversation:
    """
    Represents a complete ChatGPT conversation.
    
    Attributes:
        id: The unique identifier of the conversation.
        title: The title of the conversation.
        create_time: The Unix timestamp of the conversation creation.
        update_time: The Unix timestamp of the last update.
        messages: A list of Message objects in chronological order.
    """
    id: str
    title: str
    create_time: float
    update_time: float
    messages: list[Message] = field(default_factory=list)