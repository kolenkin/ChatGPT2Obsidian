"""
Unit tests for the parser module.
"""
import unittest
from src.parser import parse_conversations
from src.models import AuthorRole


class TestParser(unittest.TestCase):
    """Test cases for conversation parsing and DAG traversal."""
    
    def test_parse_simple_conversation(self) -> None:
        """Tests parsing of a standard linear conversation."""
        data = [
            {
                "id": "conv1",
                "title": "Test Chat",
                "create_time": 1672531200.0,
                "update_time": 1672531200.0,
                "current_node": "node3",
                "mapping": {
                    "node1": {
                        "id": "node1",
                        "parent": None,
                        "message": {
                            "author": {"role": "user"},
                            "content": {"parts": ["Hello"]},
                            "metadata": {"model_slug": "text-davinci-002-render-sha"}
                        }
                    },
                    "node2": {
                        "id": "node2",
                        "parent": "node1",
                        "message": {
                            "author": {"role": "assistant"},
                            "content": {"parts": ["Hi there!"]},
                            "metadata": {"model_slug": "gpt-4"}
                        }
                    },
                    "node3": {
                        "id": "node3",
                        "parent": "node2",
                        "message": {
                            "author": {"role": "user"},
                            "content": {"parts": ["How are you?"]},
                            "metadata": {}
                        }
                    }
                }
            }
        ]
        
        convs = parse_conversations(data)
        self.assertEqual(len(convs), 1)
        conv = convs[0]
        self.assertEqual(conv.title, "Test Chat")
        self.assertEqual(len(conv.messages), 3)
        
        self.assertEqual(conv.messages[0].role, AuthorRole.USER)
        self.assertEqual(conv.messages[0].content, "Hello")
        
        self.assertEqual(conv.messages[1].role, AuthorRole.ASSISTANT)
        self.assertEqual(conv.messages[1].content, "Hi there!")
        
        self.assertEqual(conv.messages[2].role, AuthorRole.USER)
        self.assertEqual(conv.messages[2].content, "How are you?")

    def test_ignore_empty_system(self) -> None:
        """Tests that empty system prompts are correctly ignored."""
        data = [
            {
                "id": "conv2",
                "title": None,
                "create_time": 1672531200.0,
                "update_time": 1672531200.0,
                "current_node": "node2",
                "mapping": {
                    "node1": {
                        "id": "node1",
                        "parent": None,
                        "message": {
                            "author": {"role": "system"},
                            "content": {"parts": []},
                            "metadata": {}
                        }
                    },
                    "node2": {
                        "id": "node2",
                        "parent": "node1",
                        "message": {
                            "author": {"role": "user"},
                            "content": {"parts": ["Test"]},
                            "metadata": {}
                        }
                    }
                }
            }
        ]
        
        convs = parse_conversations(data)
        self.assertEqual(len(convs[0].messages), 1)
        self.assertEqual(convs[0].title, "New_chat_1672531200")

    def test_asset_pointer(self) -> None:
        """Tests transformation of asset_pointer dictionaries into Markdown image links."""
        data = [
            {
                "id": "conv3",
                "title": "Image Chat",
                "create_time": 1672531200.0,
                "update_time": 1672531200.0,
                "current_node": "node1",
                "mapping": {
                    "node1": {
                        "id": "node1",
                        "parent": None,
                        "message": {
                            "author": {"role": "assistant"},
                            "content": {"parts": [{"asset_pointer": "file://image.png"}, "Look at this"]},
                            "metadata": {}
                        }
                    }
                }
            }
        ]
        
        convs = parse_conversations(data)
        self.assertIn("![Image](file://image.png)", convs[0].messages[0].content)
        self.assertIn("Look at this", convs[0].messages[0].content)


if __name__ == "__main__":
    unittest.main()