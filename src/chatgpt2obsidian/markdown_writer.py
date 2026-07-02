from pathlib import Path

from .models import Conversation


class MarkdownWriter:

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save_conversation(self, conversation: Conversation):

        safe_name = "".join(
            c
            for c in conversation.title
            if c not in r'<>:"/\|?*'
        ).strip()

        path = self.output_dir / f"{safe_name}.md"

        with path.open("w", encoding="utf-8") as f:

            f.write("---\n")
            f.write("source: ChatGPT\n")
            f.write("imported: true\n")
            f.write("---\n\n")

            f.write(f"# {conversation.title}\n\n")

            for message in conversation.messages:

                if message.role == "user":
                    f.write("## 👤 User\n\n")
                else:
                    f.write("## 🤖 ChatGPT\n\n")

                f.write(message.text)
                f.write("\n\n---\n\n")

        print(f"Saved: {path}")