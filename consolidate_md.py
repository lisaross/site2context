#!/usr/bin/env python3
"""
Script to consolidate markdown files into a single file for LLM context.
This script will:
1. Read all markdown files from the output directory
2. Combine them with clear section headers
3. Create a single consolidated markdown file with LLM-friendly metadata
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import re
from datetime import datetime
import json
import yaml

def clean_filename(filename: str) -> str:
    """
    Convert filename to a readable title.
    Removes extension and converts underscores/hyphens to spaces.
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
    """
    # Fix special characters
    content = content.replace('&#x2019;', "'")
    content = content.replace('&amp;', '&')
    
    # Remove multiple consecutive newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Fix markdown formatting
    content = re.sub(r'[\s\n]*---[\s\n]*', '\n\n---\n\n', content)  # Fix horizontal rules
    content = re.sub(r'[\s\n]*\*\s*\*\s*\*[\s\n]*', '\n\n---\n\n', content)  # Convert *** to horizontal rules
    content = re.sub(r'__+', '---', content)  # Convert multiple underscores to horizontal rules
    
    # Fix headers
    content = re.sub(r'\n#+\s*', '\n\n# ', content)  # Fix header spacing
    
    # Fix lists
    content = re.sub(r'\n\s*-\s*--', '\n-', content)  # Fix malformed list items
    content = re.sub(r'\n\s*-\s*', '\n- ', content)  # Fix list item spacing
    
    # Fix bold/italic text
    content = re.sub(r'\*\*\s+', '**', content)  # Remove space after opening bold
    content = re.sub(r'\s+\*\*', '**', content)  # Remove space before closing bold
    
    # Fix links
    content = re.sub(r'\[(.*?)\]\((.*?)\)', r'[\1](\2)', content)  # Normalize link formatting
    
    # Remove any remaining multiple spaces
    content = re.sub(r' {2,}', ' ', content)
    
    # Clean up line endings
    content = re.sub(r'\s+\n', '\n', content)  # Remove trailing spaces
    content = re.sub(r'\n{3,}', '\n\n', content)  # Remove extra blank lines
    
    # Remove empty lines at start and end
    content = content.strip()
    
    return content

def extract_metadata(content: str) -> Dict[str, str]:
    """
    Extract metadata from content such as main topics, key terms, etc.
    """
    # Extract main topics (headers)
    headers = re.findall(r'#+ (.*)', content)
    
    # Extract potential key terms (words in bold)
    key_terms = re.findall(r'\*\*(.*?)\*\*', content)
    
    # Extract links and their text
    links = re.findall(r'\[(.*?)\]\((.*?)\)', content)
    
    return {
        'headers': list(set(headers)),
        'key_terms': list(set(key_terms)),
        'links': list(set([link[0] for link in links]))
    }

def generate_table_of_contents(content: str) -> str:
    """
    Generate a table of contents from the headers in the content.
    """
    toc = ["## Table of Contents\n"]
    lines = content.split('\n')
    for line in lines:
        if line.startswith('#'):
            level = line.count('#') - 1
            text = line.strip('#').strip()
            if level > 0:  # Skip the main title
                indent = '  ' * (level - 1)
                toc.append(f"{indent}- {text}")
    return '\n'.join(toc)

def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_site_name(config: dict) -> str:
    # Extract site name from input_dir path
    input_dir = Path(config['input_dir'])
    return input_dir.name

def consolidate_markdown(config_path: str) -> None:
    # Load config
    config = load_config(config_path)
    site_name = get_site_name(config)
    
    # Setup paths
    output_dir = Path(config['output_dir'])
    consolidated_file = f"{site_name}_consolidated.md"
    metadata_file = f"{site_name}_consolidated_metadata.json"
    
    # Initialize metadata
    metadata = {
        "title": site_name.upper(),
        "source": site_name,
        "date_processed": datetime.now().isoformat(),
        "total_sections": 0,
        "document_type": "Website Content",
        "processing_script": "consolidate_md.py",
        "sections": []
    }
    
    # Process all markdown files
    all_content = []
    file_count = 0
    
    if output_dir.exists():
        for md_file in output_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                if content.strip():
                    # Add section metadata
                    section_name = md_file.stem.replace('-', ' ').title()
                    section_metadata = {
                        "name": section_name,
                        "path": str(md_file.relative_to(output_dir)),
                        "size": len(content)
                    }
                    metadata["sections"].append(section_metadata)
                    
                    # Add content with section header
                    section_content = f"## {section_name}\n\n{content}\n\n---\n\n"
                    all_content.append(section_content)
                    file_count += 1
                    
            except Exception as e:
                print(f"Error processing {md_file}: {str(e)}")
    
    if all_content:
        # Update metadata
        metadata["total_sections"] = file_count
        
        # Create consolidated content with metadata
        header = f"# {metadata['title']}\n\n"
        header += "## Document Metadata\n\n"
        for key, value in metadata.items():
            if key != "sections":
                header += f"- **{key}**: {value}\n"
        header += "\n## Content Overview\n\n"
        for section in metadata["sections"]:
            header += f"- {section['name']}\n"
        header += "\n---\n\n"
        
        # Write consolidated file
        consolidated_content = header + "".join(all_content)
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            f.write(consolidated_content)
        print(f"Consolidated markdown file created: {consolidated_file}")
        print(f"Processed {file_count} markdown files")
        
        # Write metadata file
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadata file created: {metadata_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python consolidate_md.py <config_file>")
        sys.exit(1)
    
    consolidate_markdown(sys.argv[1]) 