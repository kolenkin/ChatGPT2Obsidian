"""
Exporter module for handling file system operations and generating the vault structure.
"""
import logging
from pathlib import Path
from datetime import datetime, timezone
from .models import Conversation
from .markdown_writer import conversation_to_markdown, sanitize_filename

logger = logging.getLogger(__name__)


def export_conversations(conversations: list[Conversation], output_dir: Path) -> None:
    """
    Exports a list of conversations to the file system, organizing them by year.
    
    Creates year-based subdirectories, writes Markdown files, and generates 
    an Index.md file with Obsidian wiki-links.
    
    Args:
        conversations: A list of Conversation objects to export.
        output_dir: The root directory for the Obsidian vault.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    index_entries = []
    
    for conv in conversations:
        year = datetime.fromtimestamp(conv.create_time, tz=timezone.utc).year
        year_dir = output_dir / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        
        filename = sanitize_filename(conv.title) + ".md"
        filepath = year_dir / filename
        
        # Handle duplicate filenames
        counter = 1
        original_filepath = filepath
        while filepath.exists():
            filepath = original_filepath.with_stem(f"{original_filepath.stem}_{counter}")
            counter += 1
            
        md_content = conversation_to_markdown(conv)
        filepath.write_text(md_content, encoding="utf-8")
        logger.debug(f"Exported: {filepath}")
        
        rel_path = filepath.relative_to(output_dir)
        # Obsidian wiki-link format: [[path/to/file|alias]]
        wiki_link = f"[[{rel_path.as_posix().replace('.md', '')}|{conv.title}]]"
        
        index_entries.append({
            "date": conv.create_time,
            "link": wiki_link,
            "title": conv.title
        })
        
    # Sort index entries by date descending (latest first)
    index_entries.sort(key=lambda x: x["date"], reverse=True)
    
    # Generate Index.md
    index_lines = ["# ChatGPT Conversations Index\n"]
    current_year = None
    for entry in index_entries:
        year = datetime.fromtimestamp(entry["date"], tz=timezone.utc).year
        if year != current_year:
            index_lines.append(f"\n## {year}\n")
            current_year = year
        index_lines.append(f"- {entry['link']}")
        
    index_path = output_dir / "Index.md"
    index_path.write_text("\n".join(index_lines), encoding="utf-8")
    logger.info(f"Generated Index.md with {len(index_entries)} entries.")