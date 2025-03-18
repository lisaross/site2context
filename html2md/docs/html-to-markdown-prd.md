# Product Requirements Document (PRD): HTML to Markdown Extractor - POC Version

## 1. Project Overview

### Purpose
Create a Python-based proof-of-concept tool that extracts content from HTML files within a static website structure and converts it to clean markdown format, specifically targeting a single website for initial validation.

### Objectives
- Successfully parse HTML files from a downloaded website structure
- Extract meaningful content by targeting specific container elements
- Convert the extracted content to well-formatted markdown
- Preserve document hierarchy and important semantic elements
- Exclude boilerplate elements like headers, footers, and navigation

### Success Criteria
- Accurate extraction of main content from at least 90% of pages
- Clean markdown output without HTML artifacts
- Preservation of content hierarchy and basic formatting
- Simple command-line interface for initial operation

## 2. Technical Requirements

### Input
- Local directory containing HTML files from a single website (downloaded via Site Sucker or similar tool)
- Configuration file or command-line parameters specifying:
  - Content container selector (CSS or XPath)
  - Output directory
  - Optional: content exclusion selectors

### Output
- Directory of markdown files mirroring the original site structure
- Log file documenting the process and any issues encountered

### Processing Requirements
- HTML parsing with noise reduction
- Container-based content extraction
- HTML-to-markdown conversion with proper formatting
- Basic error handling and reporting

## 3. User Interface

### Command-Line Interface
```
html2md.py --input-dir <source_directory> --output-dir <target_directory> --content-selector <css_selector> [--exclude-selector <css_selector>] [--config-file <path>]
```

### Configuration File (Optional)
Simple YAML or JSON format specifying:
```
{
  "content_selector": "div.main-content",
  "exclude_selectors": ["div.navigation", "footer", "header"],
  "preserve_links": true,
  "preserve_images": false,
  "max_depth": 3
}
```

## 4. Core Features

### Content Extraction
- Identify and extract content based on specified container selector
- Remove specified boilerplate elements
- Support basic HTML structure components (headings, paragraphs, lists)

### Markdown Conversion
- Convert HTML formatting to markdown equivalents
- Handle basic formatting (headings, bold, italic, lists, links, etc.)
- Option to include or exclude images and links

### File Handling
- Maintain directory structure from original website
- Generate clean filenames based on original HTML files
- Log processing statistics and errors

## 5. Implementation Approach

### Libraries
- BeautifulSoup or lxml for HTML parsing
- html2text or custom conversion logic for HTML to markdown
- Standard Python libraries for file operations

### Process Flow
1. Read configuration settings
2. Recursively scan input directory for HTML files
3. For each HTML file:
   - Parse HTML content
   - Locate and extract content from specified container
   - Convert extracted content to markdown
   - Write to output file preserving directory structure
4. Generate summary report

## 6. Limitations for POC
- Focus on a single website with consistent structure
- Limited handling of complex HTML components (iframes, complex tables)
- No JavaScript parsing or rendering
- No automatic content container detection
- No bulk processing or parallelization

## 7. Future Extensions
- Support for multiple websites with different structures
- Automatic content container detection
- Advanced content cleaning and normalization
- Support for site-specific configuration profiles
- Parallel processing for large websites
- Web interface for configuration and monitoring

## 8. Timeline
- POC development: 2-3 weeks
- Testing with target website: 1 week
- Documentation and refinement: 1 week
