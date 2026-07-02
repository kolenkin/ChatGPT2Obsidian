"""
Markdown writer module for formatting conversations into Obsidian-compatible Markdown.
"""
import re
from datetime import datetime, timezone
from .models import Conversation, Message, AuthorRole


def sanitize_filename(title: str) -> str:
    """
    Sanitizes a string to be used as a valid filename.
    
    Removes invalid characters and trims whitespace and dots.
    
    Args:
        title: The original title string.
        
    Returns:
        A sanitized string safe for use as a filename.
    """
    sanitized = re.sub(r'[\\/:*?"<>|]', '', title)
    sanitized = sanitized.strip(' .')
    return sanitized if sanitized else "Untitled"


def format_frontmatter(conv: Conversation) -> str:
    """
    Generates the YAML frontmatter block for a conversation.
    
    Args:
        conv: The Conversation object.
        
    Returns:
        A string containing the formatted YAML frontmatter.
    """
    date_str = datetime.fromtimestamp(conv.create_time, tz=timezone.utc).strftime('%Y-%m-%d')
    updated_str = datetime.fromtimestamp(conv.update_time, tz=timezone.utc).strftime('%Y-%m-%d')
    
    models = set()
    for msg in conv.messages:
        if msg.model:
            models.add(msg.model)
    model_str = ", ".join(sorted(models)) if models else "unknown"
    
    fm = [
        "---",
        f"title: \"{conv.title}\"",
        f"date: {date_str}",
        f"updated: {updated_str}",
        f"model: {model_str}",
        "tags:",
        "  - chatgpt",
        "---"
    ]
    return "\n".join(fm)


def format_message(msg: Message) -> str:
    """
    Formats a single message into Markdown with an appropriate header.
    
    Args:
        msg: The Message object.
        
    Returns:
        A formatted Markdown string for the message.
    """
    if msg.role == AuthorRole.USER:
        header = "## User"
    elif msg.role == AuthorRole.ASSISTANT:
        header = "## Assistant"
    elif msg.role == AuthorRole.SYSTEM:
        header = "## System"
    else:
        header = f"## {msg.role.value.capitalize()}"
        
    return f"{header}\n\n{msg.content}\n"


def conversation_to_markdown(conv: Conversation) -> str:
    """
    Converts an entire Conversation object into a complete Markdown document.
    
    Args:
        conv: The Conversation object.
        
    Returns:
        A string containing the full Markdown content including frontmatter and body.
    """
    parts = []
    parts.append(format_frontmatter(conv))
    parts.append(f"# {conv.title}\n")
    
    for msg in conv.messages:
        if msg.content:
            parts.append(format_message(msg))
            
    return "\n".join(parts)