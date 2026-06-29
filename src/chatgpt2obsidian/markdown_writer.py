from pathlib import Path


class MarkdownWriter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save_conversation(self, conversation: dict) -> None:
        title = conversation.get("title") or "Untitled"

        safe_name = "".join(
            c for c in title
            if c not in r'<>:"/\|?*'
        ).strip()

        path = self.output_dir / f"{safe_name}.md"

        with path.open("w", encoding="utf-8") as f:

            f.write("---\n")
            f.write("source: ChatGPT\n")
            f.write("imported: true\n")
            f.write("---\n\n")

            f.write(f"# {title}\n\n")

            mapping = conversation["mapping"]

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

                author = message.get("author", {}).get("role", "unknown")

                if author == "user":
                    f.write("## 👤 User\n\n")
                else:
                    f.write("## 🤖 ChatGPT\n\n")

                text = "\n".join(
                    str(part)
                    for part in parts
                    if part
                )

                f.write(text)
                f.write("\n\n---\n\n")

        print(f"Saved: {path}")