# HTML to Markdown Extractor

A Python-based tool that extracts content from HTML files and converts it to clean markdown format, preserving the original directory structure while excluding boilerplate elements like headers, footers, and navigation.

## Features

- **Content Extraction**: Extract main content from HTML files based on CSS selectors
- **Clean Conversion**: Convert HTML to well-formatted markdown
- **Structure Preservation**: Maintain original website directory structure
- **Customizable Configuration**: Control the extraction process via command line or config file
- **Selective Processing**: Include or exclude specific content types
- **Batch Processing**: Process multiple HTML files in a single operation
- **Error Handling**: Detailed logs and error reports for troubleshooting

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/html-to-markdown-extractor.git
cd html-to-markdown-extractor

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .
```

### Dependencies

The package requires Python 3.8 or higher and the following dependencies:

- beautifulsoup4>=4.12.0
- html2text>=2020.1.16
- lxml>=4.9.0
- PyYAML>=6.0.1
- click>=8.1.0
- rich>=13.0.0

## Usage

### Basic Command

```bash
html2md --input-dir <source_directory> --output-dir <target_directory> --content-selector "div.main-content"
```

### With Configuration File

```bash
html2md --config-file config.yaml
```

### Example Configuration File (YAML)

```yaml
# Input and output directories
input_dir: "./html_files"
output_dir: "./markdown_output"

# Content selection
content_selector: "div.main-content"  # CSS selector for main content container
exclude_selectors:  # CSS selectors for content to exclude
  - "div.navigation"
  - "header"
  - "footer"
  - "div.sidebar"

# Content preservation options
preserve_links: true
preserve_images: true

# Processing options
max_depth: 3  # Maximum directory depth to process (optional)
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--input-dir` | Directory containing HTML files |
| `--output-dir` | Directory for markdown output |
| `--content-selector` | CSS selector for main content container |
| `--exclude-selector` | CSS selector for content to exclude (can be used multiple times) |
| `--config-file` | Path to configuration file |
| `--preserve-links` | Keep links in the markdown output (default: true) |
| `--preserve-images` | Keep image references in the markdown output (default: true) |
| `--max-depth` | Maximum directory depth to process |
| `--verbose` | Enable detailed logging |

## Using with Real Websites

### Getting Started

1. **Create a Configuration File**
   Create a YAML configuration file (e.g., `my_site_config.yaml`):
   ```yaml
   # Configuration for converting your website to markdown
   input_dir: "/path/to/your/website"  # Replace with your website directory path
   output_dir: "./converted_site"      # Output directory for markdown files

   # Content selection
   content_selector: "div.main-content"  # Adjust this to match your site's main content container
   exclude_selectors:  # Elements to exclude
     - "header"
     - "footer"
     - "nav"
     - "div.sidebar"
     - "div.navigation"
     - "div.menu"
     - "div.advertisement"

   # Content preservation options
   preserve_links: true
   preserve_images: true

   # Processing options
   max_depth: 5  # Adjust based on your site's depth
   ```

2. **Find Your Content Selector**
   - Open your website in a browser
   - Use the browser's developer tools (F12)
   - Inspect the main content area
   - Find the CSS selector that uniquely identifies your content
   - Common selectors include:
     - `article` - For blog posts or articles
     - `main` - For main content
     - `div.content` - For content divs
     - `div.post-content` - For blog post content
     - `div.entry-content` - For WordPress content

3. **Run the Converter**
   ```bash
   html2md --config-file my_site_config.yaml
   ```

### Tips for Best Results

1. **Test on a Small Subset**
   - Create a test directory with a few pages
   - Run the converter on that
   - Check the output to ensure it's extracting the right content

2. **Common Issues and Solutions**
   - If content is missing, check if the selector matches your HTML structure
   - If too much content is included, add more exclude selectors
   - If links are broken, verify the relative paths in your HTML

3. **Directory Structure**
   - The converter maintains your original directory structure
   - Adjust `max_depth` if you want to limit how deep it goes
   - Make sure you have write permissions for the output directory

4. **Content Preservation**
   - Set `preserve_links: true` to keep internal links
   - Set `preserve_images: true` to keep image references
   - Add specific exclude selectors for unwanted content

### Example Use Cases

1. **Blog Site**
   ```yaml
   content_selector: "article"
   exclude_selectors:
     - "header"
     - "footer"
     - "nav"
     - "div.sidebar"
     - "div.comments"
   ```

2. **Documentation Site**
   ```yaml
   content_selector: "div.documentation-content"
   exclude_selectors:
     - "div.navigation"
     - "div.toc"
     - "div.footer"
   ```

3. **News Site**
   ```yaml
   content_selector: "div.article-content"
   exclude_selectors:
     - "div.advertisement"
     - "div.social-share"
     - "div.related-articles"
   ```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run tests with coverage
pytest

# Run tests without coverage
pytest --no-cov
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking

```bash
# Format code
black .

# Sort imports
isort .

# Type checking
mypy .
```

## Current Limitations

- Designed for static HTML files (no JavaScript rendering)
- Limited handling of complex HTML components (iframes, complex tables)
- No automatic content container detection in current version
- Focused on single website processing with consistent structure

## Future Plans

- Support for multiple websites with different structures
- Automatic content container detection
- Advanced content cleaning and normalization
- Site-specific configuration profiles
- Parallel processing for large websites
- Web interface for configuration and monitoring
- Metadata extraction with YAML frontmatter support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [html2text](https://github.com/Alir3z4/html2text) for HTML to Markdown conversion
