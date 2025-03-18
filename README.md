# HTML to Markdown Extractor

A Python-based tool that converts HTML websites to clean markdown format, with intelligent content extraction and consolidation capabilities.

## Features

- **Smart Content Detection**: Automatically analyzes HTML structure to identify main content and boilerplate elements
- **Config Generation**: Creates a configuration file by analyzing your website's structure
- **Clean Conversion**: Converts HTML to well-formatted markdown while preserving core content
- **Content Consolidation**: Combines multiple markdown files into a single structured document with metadata
- **Directory Structure**: Maintains original website directory structure during conversion
- **Progress Tracking**: Shows real-time progress of conversion operations

## Installation

### Dependencies

The script requires Python 3.8 or higher and the following dependencies:

- beautifulsoup4>=4.12.0
- html2text>=2020.1.16
- lxml>=4.9.0
- PyYAML>=6.0.1
- click>=8.1.0

Install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Single Command Processing

The simplest way to use the tool is with the `process` command, which handles all operations in one go:

```bash
python html2md.py process /path/to/your/website
```

This will:
1. Generate a configuration file by analyzing your website
2. Convert all HTML files to markdown
3. Consolidate all markdown files into a single file with metadata

Optional flags:
- `--config` or `-c`: Specify a custom path for the configuration file
- `--max-depth` or `-d`: Set the maximum directory depth to process

Example:
```bash
python html2md.py process /path/to/website --config custom_config.yaml --max-depth 3
```

### Individual Commands

If you need more control, you can run each step separately:

1. **Generate Configuration**
   ```bash
   python html2md.py generate /path/to/website --output config.yaml
   ```

2. **Convert HTML to Markdown**
   ```bash
   python html2md.py convert config.yaml
   ```

3. **Consolidate Markdown Files**
   ```bash
   python html2md.py consolidate config.yaml
   ```

### Example Configuration File

The generated configuration file will look something like this:

```yaml
input_dir: "/absolute/path/to/your/website"
output_dir: "/absolute/path/to/your/website/markdown_output"
consolidated_output: "/absolute/path/to/your/website/markdown_output/consolidated.md"
content_selector: "main, article, div.content"
exclude_selectors:
  - "header"
  - "footer"
  - "nav"
  - "div.sidebar"
  - "div.navigation"
preserve_links: true
preserve_images: true
max_depth: 3
frontmatter:
  title:
    selector: "title"
  description:
    selector: "meta[name='description']"
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

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

## License

MIT License - see LICENSE file for details 