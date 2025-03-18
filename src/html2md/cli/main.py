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

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--config', '-c', type=click.Path(), help='Output configuration file path')
@click.option('--max-depth', '-d', type=int, default=None, help='Maximum directory depth to process')
def process(input_dir: str, config: str, max_depth: int):
    """Process HTML files: generate config, convert to markdown, and consolidate.
    
    This command combines all three operations into a single workflow:
    1. Generates a configuration file by analyzing the HTML files
    2. Converts HTML files to markdown using the generated config
    3. Consolidates all markdown files into a single file with metadata
    """
    input_path = Path(input_dir)
    
    # Generate config if not provided
    if not config:
        config = str(input_path / 'config.yaml')
    
    click.echo("Generating configuration...")
    generate_config(input_dir, config)
    
    click.echo("Loading configuration...")
    config_data = load_config(config)
    if max_depth:
        config_data['max_depth'] = max_depth
    
    # Set output directories within the input directory
    config_data['input_dir'] = str(input_path)
    config_data['output_dir'] = str(input_path / 'markdown_output')
    config_data['consolidated_output'] = str(input_path / 'markdown_output' / 'consolidated.md')
    
    click.echo("Converting HTML to Markdown...")
    process_directory(
        input_dir=Path(config_data['input_dir']),
        output_dir=Path(config_data['output_dir']),
        config=config_data,
        max_depth=config_data.get('max_depth')
    )
    
    click.echo("Consolidating markdown files...")
    consolidate_markdown(config)
    
    click.echo("Processing complete!")

def main():
    """Entry point for the command-line interface."""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 