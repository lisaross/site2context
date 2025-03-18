"""
Configuration management for HTML to Markdown conversion.
"""

import os
import re
from pathlib import Path
from typing import Dict, Set, Optional, List, Tuple
import yaml
from bs4 import BeautifulSoup, Tag
from collections import Counter

def load_config(config_path: str) -> dict:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def analyze_element_content(element: Tag) -> Dict[str, float]:
    """
    Analyze an element's content to determine if it's likely main content.
    
    Args:
        element: BeautifulSoup Tag to analyze
        
    Returns:
        dict: Dictionary of metrics about the element
    """
    # Get text length excluding scripts, styles, etc.
    text = element.get_text(strip=True)
    text_length = len(text)
    
    # Count different types of content
    paragraphs = len(element.find_all('p'))
    headings = len(element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
    links = len(element.find_all('a'))
    images = len(element.find_all('img'))
    lists = len(element.find_all(['ul', 'ol']))
    
    # Calculate content density
    total_elements = paragraphs + headings + links + images + lists
    if total_elements == 0:
        content_density = 0
    else:
        content_density = text_length / total_elements if total_elements > 0 else 0
    
    # Calculate content diversity (ratio of different element types)
    element_types = {'p': paragraphs, 'heading': headings, 'a': links, 'img': images, 'list': lists}
    non_zero_types = sum(1 for count in element_types.values() if count > 0)
    content_diversity = non_zero_types / len(element_types)
    
    return {
        'text_length': text_length,
        'content_density': content_density,
        'content_diversity': content_diversity,
        'total_elements': total_elements
    }

def extract_content_selectors(html_content: str) -> List[Tuple[str, float]]:
    """
    Extract potential content selectors from HTML content with priority scores.
    
    Args:
        html_content: The HTML content to analyze
        
    Returns:
        list: List of tuples (selector, priority_score)
    """
    soup = BeautifulSoup(html_content, 'lxml')
    selectors = []
    
    # Analyze all major container elements
    containers = soup.find_all(['main', 'article', 'section', 'div'])
    
    for element in containers:
        # Skip empty or tiny elements
        if not element.get_text(strip=True) or len(element.get_text(strip=True)) < 50:
            continue
            
        metrics = analyze_element_content(element)
        score = 0.0
        
        # Base score from content analysis
        score += min(metrics['text_length'] / 1000, 5)  # Up to 5 points for length
        score += metrics['content_diversity'] * 3  # Up to 3 points for diversity
        score += min(metrics['content_density'] / 100, 2)  # Up to 2 points for density
        
        # Bonus points for semantic elements
        if element.name == 'main':
            score += 3
            if element.get('role') == 'main':
                score += 2
        elif element.name == 'article':
            score += 2
        elif element.name == 'section':
            score += 1
            
        # Bonus points for content-related classes
        classes = element.get('class', [])
        if isinstance(classes, str):
            classes = [classes]
            
        class_score = 0
        content_class_indicators = {
            'content': 2,
            'main': 2,
            'article': 1.5,
            'container': 1,
            'section': 0.5
        }
        
        for cls in classes:
            cls_lower = cls.lower()
            for indicator, points in content_class_indicators.items():
                if indicator in cls_lower:
                    class_score += points
                    
        score += min(class_score, 3)  # Cap class bonus at 3 points
        
        # Build selector
        selector_parts = [element.name]
        
        # Add role if present
        if element.get('role'):
            selector_parts.append(f'[role="{element.get("role")}"]')
            
        # Add significant classes
        significant_classes = [cls for cls in classes if any(indicator in cls.lower() for indicator in content_class_indicators)]
        if significant_classes:
            if len(significant_classes) == 1:
                selector_parts.append(f'.{significant_classes[0]}')
            else:
                selector_parts.append(f'[class*="{significant_classes[0]}"]')
        
        selector = ''.join(selector_parts)
        selectors.append((selector, score))
    
    # Sort by score and remove duplicates while preserving order
    seen = set()
    unique_selectors = []
    for selector, score in sorted(selectors, key=lambda x: x[1], reverse=True):
        if selector not in seen:
            seen.add(selector)
            unique_selectors.append((selector, score))
    
    return unique_selectors

def extract_boilerplate_selectors(html_content: str) -> Dict[str, Set[str]]:
    """
    Extract boilerplate selectors from HTML content.
    
    Args:
        html_content: The HTML content to analyze
        
    Returns:
        dict: Dictionary containing sets of boilerplate selectors
    """
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Common boilerplate elements
    boilerplate_elements = {
        'header', 'footer', 'nav', 'script', 'style', 'noscript',
        'iframe', 'form', 'button', 'input', 'select'
    }
    
    # Common boilerplate classes
    boilerplate_classes = {
        'navbar', 'nav-item', 'btn', 'footer', 'banner',
        'slidecontainer', 'ratio'
    }
    
    # Find all elements with classes
    elements_with_classes = soup.find_all(class_=True)
    found_classes = set()
    
    for element in elements_with_classes:
        classes = element.get('class', [])
        if isinstance(classes, str):
            classes = [classes]
        found_classes.update(cls for cls in classes if any(indicator in cls.lower() for indicator in boilerplate_classes))
    
    # Find all elements
    all_elements = {tag.name for tag in soup.find_all() if tag.name in boilerplate_elements}
    
    return {
        'elements': all_elements,
        'classes': found_classes
    }

def analyze_html_files(directory: str) -> Dict[str, Set[str] | List[str]]:
    """
    Analyze all HTML files in the given directory and its subdirectories.
    
    Args:
        directory: Directory to analyze
        
    Returns:
        dict: Dictionary containing analysis results
    """
    all_content_selectors = []
    all_boilerplate = {'elements': set(), 'classes': set()}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract content selectors
                        content_selectors = extract_content_selectors(content)
                        all_content_selectors.extend(content_selectors)
                        # Extract boilerplate
                        boilerplate = extract_boilerplate_selectors(content)
                        all_boilerplate['elements'].update(boilerplate['elements'])
                        all_boilerplate['classes'].update(boilerplate['classes'])
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    # Combine selectors that appear multiple times with high scores
    selector_scores = {}
    for selector, score in all_content_selectors:
        if selector in selector_scores:
            selector_scores[selector] = max(selector_scores[selector], score)
        else:
            selector_scores[selector] = score
    
    # Get top selectors (those with scores above 5)
    top_selectors = sorted(
        [(s, score) for s, score in selector_scores.items() if score > 5],
        key=lambda x: x[1],
        reverse=True
    )
    
    return {
        'content_selectors': [selector for selector, _ in top_selectors],
        'boilerplate': all_boilerplate
    }

def generate_config(directory: str, output_file: Optional[str] = None) -> None:
    """
    Generate a configuration file based on HTML analysis.
    
    Args:
        directory: Directory containing HTML files to analyze
        output_file: Optional path for the output configuration file
    """
    # Get directory name for output folder
    dir_path = Path(directory)
    dir_name = dir_path.name
    output_dir = "markdown_output"  # Changed from f"{dir_name}_output_md"
    
    # If no output file specified, use directory name
    if output_file is None:
        output_file = str(dir_path / 'config.yaml')
    
    # Analyze HTML files
    analysis = analyze_html_files(directory)
    
    # Create content selector from top selectors
    content_selector = ', '.join(analysis['content_selectors'][:3])  # Use top 3 selectors
    
    # Create configuration
    config = {
        'input_dir': str(dir_path),
        'output_dir': str(dir_path / output_dir),
        'content_selector': content_selector,
        'exclude_selectors': [
            # Add element selectors
            *sorted(analysis['boilerplate']['elements']),
            # Add class selectors
            *sorted(f".{cls}" for cls in analysis['boilerplate']['classes'])
        ],
        'preserve_links': True,
        'preserve_images': True,
        'max_depth': 3,
        'frontmatter': {
            'title': {'selector': 'title'},
            'description': {'selector': 'meta[name="description"]'}
        }
    }
    
    # Write configuration to file
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"Configuration file generated: {output_file}")
    print(f"Output directory will be: {config['output_dir']}")
    print(f"\nDetected content selector: {content_selector}")
    print("Excluded elements:", len(analysis['boilerplate']['elements']))
    print("Excluded classes:", len(analysis['boilerplate']['classes'])) 