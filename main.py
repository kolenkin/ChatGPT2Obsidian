from src.chatgpt2obsidian.parser import ChatParser
from src.chatgpt2obsidian.markdown_writer import MarkdownWriter


def main():
    parser = ChatParser("input/conversations.json")
    conversations = parser.load()

    writer = MarkdownWriter()

    writer.save_conversation(conversations[0])


if __name__ == "__main__":
    main()