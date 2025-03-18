"""
HTML to Markdown Extractor

A Python package that extracts content from HTML files and converts it to clean markdown format,
preserving the original directory structure while excluding boilerplate elements.
"""

__version__ = "0.1.0"

from .core import convert_html_to_md, process_directory
from .config import load_config, generate_config
from .consolidate import consolidate_markdown

__all__ = [
    'convert_html_to_md',
    'process_directory',
    'load_config',
    'generate_config',
    'consolidate_markdown'
] 