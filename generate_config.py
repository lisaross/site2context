#!/usr/bin/env python3
"""
Script to analyze HTML files and generate a unique configuration file for html2md.
This script will:
1. Scan HTML files for common boilerplate elements
2. Extract unique classes and elements to exclude
3. Generate a YAML configuration file
"""

import os
from bs4 import BeautifulSoup
from typing import Set, Dict, List
import yaml
from pathlib import Path

def extract_classes_and_elements(html_content: str) -> Dict[str, Set[str]]:
    """
    Extract unique classes and elements from HTML content.
    Returns a dictionary with 'classes' and 'elements' sets.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Common boilerplate elements to look for
    boilerplate_elements = {
        'header', 'footer', 'nav', 'aside', 'script', 'style',
        'noscript', 'iframe', 'form', 'button', 'input', 'select',
        'textarea', 'meta', 'link', 'img'
    }
    
    # Common boilerplate classes
    boilerplate_classes = {
        'header', 'footer', 'nav', 'navigation', 'menu', 'sidebar',
        'advertisement', 'ad', 'social', 'share', 'comment', 'form',
        'search', 'login', 'signup', 'button', 'btn', 'modal',
        'popup', 'cookie', 'banner', 'alert', 'notification'
    }
    
    # Find all elements with classes
    elements_with_classes = soup.find_all(class_=True)
    found_classes = set()
    for element in elements_with_classes:
        classes = element.get('class', [])
        if isinstance(classes, str):
            classes = [classes]
        found_classes.update(classes)
    
    # Find all elements
    all_elements = {tag.name for tag in soup.find_all()}
    
    # Filter for boilerplate elements and classes
    boilerplate_found = {
        'elements': all_elements.intersection(boilerplate_elements),
        'classes': found_classes.intersection(boilerplate_classes)
    }
    
    return boilerplate_found

def analyze_html_files(directory: str) -> Dict[str, Set[str]]:
    """
    Analyze all HTML files in the given directory and its subdirectories.
    Returns a dictionary with combined unique classes and elements.
    """
    all_classes = set()
    all_elements = set()
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        result = extract_classes_and_elements(content)
                        all_classes.update(result['classes'])
                        all_elements.update(result['elements'])
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    return {
        'classes': sorted(all_classes),
        'elements': sorted(all_elements)
    }

def generate_config(directory: str, output_file: str = None):
    """
    Generate a configuration file based on HTML analysis.
    """
    # Get directory name for output folder
    dir_path = Path(directory)
    dir_name = dir_path.name
    output_dir = f"{dir_name}_output_md"
    
    # If no output file specified, use directory name
    if output_file is None:
        output_file = f"{dir_name}_config.yaml"
    
    # Analyze HTML files
    analysis = analyze_html_files(directory)
    
    # Create configuration
    config = {
        'input_dir': directory,
        'output_dir': output_dir,
        'content_selector': 'main[role="main"]',
        'exclude_selectors': [
            # Add element selectors
            *[f"{element}" for element in analysis['elements']],
            # Add class selectors
            *[f".{cls}" for cls in analysis['classes']]
        ],
        'preserve_links': True,
        'preserve_images': True,
        'max_depth': 3
    }
    
    # Write configuration to file
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"Configuration file generated: {output_file}")
    print(f"Output directory will be: {output_dir}")
    print("\nExcluded elements:", len(analysis['elements']))
    print("Excluded classes:", len(analysis['classes']))

if __name__ == '__main__':
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    # Look for mwmcc.ca directory in the same directory as the script
    website_dir = script_dir / 'mwmcc.ca'
    
    if not website_dir.exists():
        print("Error: mwmcc.ca directory not found in the same directory as this script")
        exit(1)
    
    generate_config(str(website_dir)) 