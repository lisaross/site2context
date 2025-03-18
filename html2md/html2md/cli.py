"""
Command-line interface for HTML to Markdown conversion.
"""
import click
from pathlib import Path
from typing import List

from .core import HTMLConverter
from .config import get_config

@click.command()
@click.option('--input-dir', type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
              help='Directory containing HTML files')
@click.option('--output-dir', type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
              help='Directory for markdown output')
@click.option('--content-selector',
              help='CSS selector for main content container')
@click.option('--exclude-selector', multiple=True,
              help='CSS selector for content to exclude (can be used multiple times)')
@click.option('--config-file', type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help='Path to configuration file')
@click.option('--preserve-links/--no-preserve-links', default=True,
              help='Keep links in the markdown output')
@click.option('--preserve-images/--no-preserve-images', default=True,
              help='Keep image references in the markdown output')
@click.option('--max-depth', type=int,
              help='Maximum directory depth to process')
@click.option('--verbose/--quiet', default=False,
              help='Enable detailed logging')
@click.pass_context
def main(ctx: click.Context, **kwargs) -> None:
    """
    Convert HTML files to markdown format.
    
    This tool extracts content from HTML files and converts it to clean markdown format,
    preserving the original directory structure while excluding boilerplate elements.
    """
    try:
        # Validate that either config file or required options are provided
        if not kwargs.get('config_file'):
            if not all([kwargs.get('input_dir'), kwargs.get('output_dir'), kwargs.get('content_selector')]):
                raise click.UsageError("When not using a config file, --input-dir, --output-dir, and --content-selector are required")
        
        config = get_config(ctx)
        converter = HTMLConverter(config)
        converter.process_directory(config.input_dir, config.output_dir)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        ctx.exit(1)

if __name__ == '__main__':
    main() 