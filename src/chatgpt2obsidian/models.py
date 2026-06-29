from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Author:
    role: str
    name: str | None = None


@dataclass(slots=True)
class Attachment:
    id: str
    filename: str
    mime_type: str | None = None
    size: int | None = None


@dataclass(slots=True)
class Message:
    id: str
    author: Author
    created_at: datetime | None
    text: str
    attachments: list[Attachment] = field(default_factory=list)


@dataclass(slots=True)
class Conversation:
    id: str
    title: str
    created_at: datetime | None
    updated_at: datetime | None
    model: str | None
    messages: list[Message] = field(default_factory=list)