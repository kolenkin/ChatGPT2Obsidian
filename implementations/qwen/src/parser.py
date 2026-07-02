"""
Parser module for reading and processing ChatGPT conversations.json.
"""
import logging
from typing import Any
from .models import Conversation, Message, AuthorRole

logger = logging.getLogger(__name__)


def parse_conversations(data: list[dict[str, Any]]) -> list[Conversation]:
    """
    Parses the raw JSON data of conversations into a list of Conversation objects.
    
    This function traverses the directed acyclic graph (DAG) of messages starting 
    from the current_node, ensuring that discarded branches are ignored.
    
    Args:
        data: A list of dictionaries representing raw chat objects from conversations.json.
        
    Returns:
        A list of parsed Conversation objects with messages in chronological order.
    """
    conversations = []
    
    for chat in data:
        title = chat.get("title")
        create_time = chat.get("create_time", 0.0)
        update_time = chat.get("update_time", 0.0)
        current_node = chat.get("current_node")
        mapping = chat.get("mapping", {})
        
        if not title:
            title = f"New_chat_{int(create_time)}"
            
        messages = []
        node_id = current_node
        
        while node_id is not None:
            node = mapping.get(node_id)
            if not node:
                logger.warning(f"Node {node_id} not found in mapping for chat {chat.get('id')}")
                break
                
            message_data = node.get("message")
            if message_data:
                author = message_data.get("author", {})
                role_str = author.get("role", "user")
                content = message_data.get("content", {})
                parts = content.get("parts", [])
                
                text_parts = []
                for part in parts:
                    if isinstance(part, str):
                        text_parts.append(part)
                    elif isinstance(part, dict):
                        asset_pointer = part.get("asset_pointer")
                        if asset_pointer:
                            text_parts.append(f"![Image]({asset_pointer})")
                            
                text = "\n".join(text_parts).strip()
                
                # Ignore empty system prompts
                if role_str == "system" and not text:
                    node_id = node.get("parent")
                    continue
                    
                try:
                    role = AuthorRole(role_str)
                except ValueError:
                    role = AuthorRole.USER
                    
                model = message_data.get("metadata", {}).get("model_slug")
                msg_create_time = message_data.get("create_time")
                
                msg = Message(
                    role=role,
                    content=text,
                    model=model,
                    timestamp=msg_create_time
                )
                messages.append(msg)
                
            node_id = node.get("parent")
            
        # Reverse to get chronological order (from root to current_node)
        messages.reverse()
        
        conv = Conversation(
            id=chat.get("id", ""),
            title=title,
            create_time=create_time,
            update_time=update_time,
            messages=messages
        )
        conversations.append(conv)
        
    return conversations