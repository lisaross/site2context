"""
Core functionality for HTML to Markdown conversion.
"""

from pathlib import Path
from bs4 import BeautifulSoup
from html2text import HTML2Text
from typing import Dict, Optional
import re

def clean_markdown(markdown: str) -> str:
    """
    Clean up markdown output by removing common issues.
    
    Args:
        markdown: The markdown content to clean
        
    Returns:
        str: The cleaned markdown content
    """
    # Remove redundant horizontal rules
    markdown = re.sub(r'\n\* \* \*\n+', '\n\n', markdown)
    
    # Remove empty lines with placeholder text
    markdown = re.sub(r'\nOur\s*\n', '\n', markdown)
    
    # Remove standalone underscores
    markdown = re.sub(r'\n__\n', '\n', markdown)
    
    # Normalize header spacing
    markdown = re.sub(r'(\n#{1,6} .+)\n+', r'\1\n\n', markdown)
    
    # Remove multiple consecutive empty lines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    return markdown.strip()

def convert_html_to_md(html_content: str, config: dict) -> str:
    """
    Convert HTML content to markdown based on configuration.
    
    Args:
        html_content: The HTML content to convert
        config: Configuration dictionary with conversion settings
        
    Returns:
        str: The converted markdown content
    """
    # Create HTML2Text instance
    h2t = HTML2Text()
    h2t.ignore_links = not config.get('preserve_links', True)
    h2t.ignore_images = not config.get('preserve_images', True)
    h2t.body_width = 0  # Disable line wrapping
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Find main content container
    selectors = config['content_selector'].split(',')
    main_content = None
    for selector in selectors:
        main_content = soup.select_one(selector.strip())
        if main_content:
            break
            
    if not main_content:
        return ""
    
    # Remove excluded elements
    for selector in config.get('exclude_selectors', []):
        for element in main_content.select(selector):
            element.decompose()
    
    # Convert to markdown and clean up
    markdown = h2t.handle(str(main_content))
    return clean_markdown(markdown)

def process_directory(input_dir: Path, output_dir: Path, config: dict, max_depth: Optional[int] = None) -> None:
    """
    Process all HTML files in a directory and convert them to markdown.
    
    Args:
        input_dir: Directory containing HTML files
        output_dir: Directory for markdown output
        config: Configuration dictionary
        max_depth: Maximum directory depth to process
    """
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all HTML files
    input_dir = Path(input_dir)
    for html_file in input_dir.rglob("*.html"):
        try:
            # Check depth if specified
            if max_depth is not None:
                rel_path = html_file.relative_to(input_dir)
                if len(rel_path.parts) > max_depth:
                    continue
            
            # Calculate output path
            rel_path = html_file.relative_to(input_dir)
            output_path = output_dir / rel_path.with_suffix('.md')
            
            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert file
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            markdown_content = convert_html_to_md(html_content, config)
            
            # Save if content was extracted
            if markdown_content:
                output_path.write_text(markdown_content, encoding='utf-8')
                print(f"Converted {html_file} -> {output_path}")
            else:
                print(f"No content found in {html_file}")
                
        except Exception as e:
            print(f"Error processing {html_file}: {str(e)}") 