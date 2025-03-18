# HTML to Markdown Extractor

A Python-based tool that extracts content from HTML files and converts it to clean markdown format, preserving the original directory structure while excluding boilerplate elements like headers, footers, and navigation.

## Overview

HTML to Markdown Extractor is designed for content managers, technical writers, data scientists, and developers who need to extract the meaningful content from HTML files while converting it to markdown format. This tool is particularly useful for:

- Preparing content for documentation systems
- Creating clean datasets for LLM training
- Archiving website content in a readable format
- Content migration projects

## Features

- **Content Extraction**: Extract main content from HTML files based on CSS selectors
- **Clean Conversion**: Convert HTML to well-formatted markdown
- **Structure Preservation**: Maintain original website directory structure
- **Customizable Configuration**: Control the extraction process via command line or config file
- **Selective Processing**: Include or exclude specific content types
- **Batch Processing**: Process multiple HTML files in a single operation
- **Error Handling**: Detailed logs and error reports for troubleshooting

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/html-to-markdown-extractor.git
cd html-to-markdown-extractor

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Command

```bash
python html2md.py --input-dir <source_directory> --output-dir <target_directory> --content-selector "div.main-content"
```

### With Configuration File

```bash
python html2md.py --config-file config.json
```

### Example Configuration File (JSON)

```json
{
  "input_dir": "./html_files",
  "output_dir": "./markdown_output",
  "content_selector": "div.main-content",
  "exclude_selectors": ["div.navigation", "footer", "header"],
  "preserve_links": true,
  "preserve_images": false,
  "max_depth": 3
}
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--input-dir` | Directory containing HTML files |
| `--output-dir` | Directory for markdown output |
| `--content-selector` | CSS selector for main content container |
| `--exclude-selector` | CSS selector for content to exclude (can be used multiple times) |
| `--config-file` | Path to configuration file |
| `--preserve-links` | Keep links in the markdown output (default: true) |
| `--preserve-images` | Keep image references in the markdown output (default: true) |
| `--verbose` | Enable detailed logging |

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
