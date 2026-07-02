// File: README.md
# ChatGPT2Obsidian

A professional CLI tool to convert OpenAI's `conversations.json` export into a structured Obsidian Markdown vault.

## Features
- Deep deserialization of ChatGPT exports.
- DAG traversal to accurately reconstruct conversation history (ignoring discarded branches).
- Year-based directory structure.
- YAML frontmatter with metadata (title, date, model, tags).
- Generation of an `Index.md` with Obsidian wiki-links.
- Zero external dependencies (Python 3.11+ standard library only).

## Installation
No installation required. Just ensure you have Python 3.11 or higher.

## Usage
```bash
python main.py --input path/to/conversations.json --output path/to/obsidian/vault