from pathlib import Path
from bs4 import BeautifulSoup
from html2text import HTML2Text
import yaml

def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def convert_html_to_md(html_content: str, config: dict) -> str:
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
    
    # Convert to markdown
    markdown = h2t.handle(str(main_content))
    return markdown.strip()

def process_directory(input_dir: Path, output_dir: Path, config: dict, max_depth: int = None) -> None:
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

def main():
    # Load config
    config = load_config('obesitycanada_config.yaml')
    
    # Process directory
    process_directory(
        input_dir=config['input_dir'],
        output_dir=config['output_dir'],
        config=config,
        max_depth=config.get('max_depth')
    )

if __name__ == '__main__':
    main() 