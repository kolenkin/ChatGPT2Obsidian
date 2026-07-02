from dataclasses import dataclass, field


@dataclass
class Message:
    role: str
    text: str


@dataclass
class Conversation:
    id: str
    title: str
    messages: list[Message] = field(default_factory=list)