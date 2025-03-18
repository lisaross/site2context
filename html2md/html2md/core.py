"""
Core functionality for HTML to Markdown conversion.
"""
from pathlib import Path
from typing import List, Optional, Dict, Any

import click
from bs4 import BeautifulSoup
from html2text import HTML2Text
from rich.console import Console
from rich.progress import Progress

from .config import Config
from .exceptions import ConversionError

console = Console()

class HTMLConverter:
    """Main class for HTML to Markdown conversion."""
    
    def __init__(self, config: Config):
        """
        Initialize the converter with configuration.
        
        Args:
            config: Configuration object containing conversion settings
        """
        self.config = config
        self.h2t = HTML2Text()
        self._setup_html2text()
    
    def _setup_html2text(self) -> None:
        """Configure html2text settings based on config."""
        self.h2t.ignore_links = not self.config.preserve_links
        self.h2t.ignore_images = not self.config.preserve_images
        self.h2t.body_width = 0  # Disable line wrapping
    
    def convert_file(self, input_path: Path) -> str:
        """
        Convert a single HTML file to markdown.
        
        Args:
            input_path: Path to the HTML file
            
        Returns:
            Converted markdown content
            
        Raises:
            ConversionError: If conversion fails
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Find main content container
            main_content = soup.select_one(self.config.content_selector)
            if not main_content:
                raise ConversionError(f"No content found with selector: {self.config.content_selector}")
            
            # Remove excluded elements
            for selector in self.config.exclude_selectors:
                for element in main_content.select(selector):
                    element.decompose()
            
            # Convert to markdown
            markdown = self.h2t.handle(str(main_content))
            return markdown.strip()
            
        except Exception as e:
            raise ConversionError(f"Failed to convert {input_path}: {str(e)}")
    
    def process_directory(self, input_dir: Path, output_dir: Path) -> None:
        """
        Process all HTML files in a directory recursively.
        
        Args:
            input_dir: Input directory containing HTML files
            output_dir: Output directory for markdown files
        """
        html_files = list(input_dir.rglob("*.html"))
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Converting files...", total=len(html_files))
            
            for html_file in html_files:
                try:
                    # Calculate relative path and create output path
                    rel_path = html_file.relative_to(input_dir)
                    output_path = output_dir / rel_path.with_suffix('.md')
                    
                    # Create output directory if needed
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Convert and save
                    markdown_content = self.convert_file(html_file)
                    output_path.write_text(markdown_content, encoding='utf-8')
                    
                except Exception as e:
                    console.print(f"[red]Error processing {html_file}: {str(e)}")
                
                progress.advance(task)
    
    @classmethod
    def from_config_file(cls, config_path: Path) -> 'HTMLConverter':
        """
        Create a converter instance from a config file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Configured HTMLConverter instance
        """
        config = Config.from_file(config_path)
        return cls(config) 