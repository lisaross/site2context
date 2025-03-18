"""
Configuration management for HTML to Markdown conversion.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml
from click import Context

@dataclass
class Config:
    """Configuration settings for HTML to Markdown conversion."""
    
    input_dir: Path
    output_dir: Path
    content_selector: str
    exclude_selectors: List[str]
    preserve_links: bool = True
    preserve_images: bool = True
    max_depth: Optional[int] = None
    
    @classmethod
    def from_file(cls, config_path: Path) -> 'Config':
        """
        Create configuration from a YAML file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Config instance with settings from file
        """
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return cls(
            input_dir=Path(data['input_dir']),
            output_dir=Path(data['output_dir']),
            content_selector=data['content_selector'],
            exclude_selectors=data.get('exclude_selectors', []),
            preserve_links=data.get('preserve_links', True),
            preserve_images=data.get('preserve_images', True),
            max_depth=data.get('max_depth')
        )
    
    def to_dict(self) -> dict:
        """Convert config to dictionary for YAML serialization."""
        return {
            'input_dir': str(self.input_dir),
            'output_dir': str(self.output_dir),
            'content_selector': self.content_selector,
            'exclude_selectors': self.exclude_selectors,
            'preserve_links': self.preserve_links,
            'preserve_images': self.preserve_images,
            'max_depth': self.max_depth
        }

def get_config(ctx: Context) -> Config:
    """Get configuration from command line options or config file."""
    params = ctx.params
    
    # If config file is provided, use it
    if params.get('config_file'):
        return Config.from_file(params['config_file'])
    
    # Otherwise, use command line options
    return Config(
        input_dir=params['input_dir'],
        output_dir=params['output_dir'],
        content_selector=params['content_selector'],
        exclude_selectors=list(params.get('exclude_selector', [])),
        preserve_links=params.get('preserve_links', True),
        preserve_images=params.get('preserve_images', True),
        max_depth=params.get('max_depth')
    ) 