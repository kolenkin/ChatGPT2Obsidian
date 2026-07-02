"""
Command-line interface module for ChatGPT2Obsidian.
"""
import argparse
import json
import logging
import sys
from pathlib import Path
from .parser import parse_conversations
from .exporter import export_conversations


def setup_logging(verbose: bool) -> None:
    """
    Configures the logging system based on verbosity level.
    
    Args:
        verbose: If True, sets logging level to DEBUG; otherwise, INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main() -> None:
    """
    Main entry point for the CLI application.
    
    Parses command-line arguments, reads the input JSON, processes conversations, 
    and triggers the export process.
    """
    parser = argparse.ArgumentParser(
        description="Convert ChatGPT conversations.json to Obsidian Markdown vault."
    )
    parser.add_argument(
        "-i", "--input", type=Path, required=True, help="Path to conversations.json"
    )
    parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Path to output directory"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    if not args.input.exists():
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)
        
    logger.info(f"Reading conversations from {args.input}...")
    try:
        with args.input.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to read or parse JSON: {e}")
        sys.exit(1)
        
    logger.info("Parsing conversations...")
    conversations = parse_conversations(data)
    logger.info(f"Parsed {len(conversations)} conversations.")
    
    logger.info(f"Exporting to {args.output}...")
    export_conversations(conversations, args.output)
    logger.info("Export completed successfully.")