"""
Markdown file consolidation functionality.
"""

import os
import re
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List
from .config import load_config

def clean_filename(filename: str) -> str:
    """
    Convert filename to a readable title.
    
    Args:
        filename: The filename to clean
        
    Returns:
        str: Cleaned filename
    """
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Replace underscores and hyphens with spaces
    name = re.sub(r'[_-]', ' ', name)
    # Capitalize first letter of each word
    name = name.title()
    # Fix common abbreviations
    name = name.replace('Mwm', 'MWM')
    name = name.replace('Ca', 'CA')
    return name

def clean_content(content: str) -> str:
    """
    Clean up markdown content by removing extra whitespace and formatting.
    
    Args:
        content: The markdown content to clean
        
    Returns:
        str: Cleaned markdown content
    """
    # Fix special characters
    content = content.replace('&#x2019;', "'")
    content = content.replace('&amp;', '&')
    
    # Remove multiple consecutive newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def consolidate_markdown(config_file: str) -> None:
    """
    Consolidate all markdown files into a single file with metadata.
    
    Args:
        config_file: Path to the configuration file
    """
    config = load_config(config_file)
    input_dir = Path(config['input_dir'])
    output_dir = Path(config['output_dir'])
    consolidated_output = Path(config.get('consolidated_output', output_dir / 'consolidated.md'))
    
    # Ensure output directory exists
    consolidated_output.parent.mkdir(parents=True, exist_ok=True)
    
    # Get all markdown files
    markdown_files = list(output_dir.rglob('*.md'))
    
    # Sort files by path for consistent ordering
    markdown_files.sort()
    
    # Prepare metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'source_directory': str(input_dir),
        'total_files': len(markdown_files),
        'files': []
    }
    
    # Build consolidated content
    consolidated_content = []
    consolidated_content.append('# Consolidated Markdown Content\n\n')
    
    # Process each file
    for md_file in markdown_files:
        # Get relative path for metadata
        rel_path = md_file.relative_to(output_dir)
        
        # Read content
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean content
        content = clean_content(content)
        
        # Add to consolidated content
        consolidated_content.append(f'## {clean_filename(rel_path.stem)}\n\n')
        consolidated_content.append(content)
        consolidated_content.append('\n\n---\n\n')
        
        # Add to metadata
        metadata['files'].append({
            'path': str(rel_path),
            'title': clean_filename(rel_path.stem),
            'size': os.path.getsize(md_file)
        })
    
    # Write consolidated content
    with open(consolidated_output, 'w', encoding='utf-8') as f:
        f.write(''.join(consolidated_content))
    
    # Write metadata
    metadata_file = consolidated_output.parent / 'metadata.json'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2) 