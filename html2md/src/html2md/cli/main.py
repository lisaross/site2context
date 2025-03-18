"""
Main command-line interface for HTML to Markdown conversion.
"""

import sys
import click
from pathlib import Path
from ..core import process_directory
from ..config import load_config, generate_config
from ..consolidate import consolidate_markdown

@click.group()
def cli():
    """HTML to Markdown Extractor - Convert HTML files to clean markdown format."""
    pass

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output', '-o', type=click.Path(), help='Output configuration file path')
def generate(input_dir: str, output: str):
    """Generate a configuration file by analyzing HTML files."""
    generate_config(input_dir, output)

@cli.command()
@click.argument('config_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
def convert(config_file: str):
    """Convert HTML files to markdown using a configuration file."""
    config = load_config(config_file)
    process_directory(
        input_dir=Path(config['input_dir']),
        output_dir=Path(config['output_dir']),
        config=config,
        max_depth=config.get('max_depth')
    )

@cli.command()
@click.argument('config_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
def consolidate(config_file: str):
    """Consolidate markdown files into a single file with metadata."""
    consolidate_markdown(config_file)

def main():
    """Entry point for the command-line interface."""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 