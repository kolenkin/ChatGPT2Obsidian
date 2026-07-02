from src.chatgpt2obsidian.parser import ChatParser
from src.chatgpt2obsidian.markdown_writer import MarkdownWriter


def main():
    parser = ChatParser("input/conversations.json")
    conversations = parser.load()

    writer = MarkdownWriter()

    exported = 0

    for conversation in conversations:
        try:
            writer.save_conversation(conversation)
            exported += 1
        except Exception as e:
            print(f"ERROR: {conversation.title}")
            print(e)

    print()
    print(f"Exported {exported} conversations.")


if __name__ == "__main__":
    main()