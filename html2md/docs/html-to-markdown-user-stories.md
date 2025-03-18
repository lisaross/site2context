# User Stories: HTML to Markdown Extractor

## Core Functionality

### US-01: Basic Content Extraction
**As a** content manager,  
**I want to** extract the main content from HTML files while excluding headers and footers,  
**So that** I can focus on the actual information without distractions.

*Acceptance Criteria:*
- Tool accepts a directory of HTML files as input
- Tool extracts content based on a specified CSS selector
- Extracted content excludes navigation, headers, and footers
- Output contains only the primary content

### US-02: HTML to Markdown Conversion
**As a** technical writer,  
**I want to** convert HTML content to clean markdown format,  
**So that** I can use it in documentation or for LLM training.

*Acceptance Criteria:*
- HTML formatting elements are converted to markdown equivalents
- Basic formatting (headings, lists, links, emphasis) is preserved
- Complex HTML artifacts are handled gracefully
- Output is valid markdown that renders correctly

### US-03: Directory Structure Preservation
**As a** content analyst,  
**I want to** maintain the original website's directory structure in the output,  
**So that** I can understand the content organization and hierarchy.

*Acceptance Criteria:*
- Output directory mirrors the structure of input directory
- File names are preserved or sensibly derived from original HTML files
- Original paths can be traced back to source files

### US-04: Configuration Options
**As a** developer,  
**I want to** specify configuration options via command line or config file,  
**So that** I can customize the extraction process for different websites.

*Acceptance Criteria:*
- Command-line arguments for essential options
- Support for configuration file with all available options
- Clear documentation of configuration parameters
- Configuration overrides work as expected

## Extended Functionality

### US-05: Selective Content Processing
**As a** data scientist,  
**I want to** include or exclude specific types of content,  
**So that** I can create focused datasets for analysis or training.

*Acceptance Criteria:*
- Support for exclusion selectors to remove unwanted content
- Option to preserve or strip specific HTML elements
- Control over link and image handling

### US-06: Batch Processing
**As a** content administrator,  
**I want to** process multiple HTML files in a single operation,  
**So that** I can efficiently convert large websites.

*Acceptance Criteria:*
- Tool recursively processes all HTML files in the input directory
- Processing works consistently across different file structures
- Basic progress reporting during execution

### US-07: Error Handling and Reporting
**As a** system administrator,  
**I want to** receive detailed logs and error reports,  
**So that** I can identify and resolve issues with the conversion process.

*Acceptance Criteria:*
- Failures don't terminate the entire process
- Detailed error logging with file names and error types
- Summary report after processing is complete
- Option to set verbosity level

### US-08: Output Customization
**As a** content curator,  
**I want to** control the format and style of the markdown output,  
**So that** it matches my specific requirements.

*Acceptance Criteria:*
- Options to control heading style (ATX vs. Setext)
- Control over list formatting
- Options for handling special characters
- Control over whitespace and formatting

## Future Considerations

### US-09: Content Metadata Extraction
**As a** knowledge manager,  
**I want to** extract and preserve metadata from HTML files,  
**So that** I can maintain important context about the content.

*Acceptance Criteria:*
- Extraction of title, author, publication date when available
- Option to include metadata as YAML frontmatter in markdown
- Preservation of relevant meta tags

### US-10: Automatic Content Detection
**As a** non-technical user,  
**I want to** automatically detect the main content container,  
**So that** I don't need to manually specify CSS selectors.

*Acceptance Criteria:*
- Heuristic-based detection of main content areas
- Reasonable success rate across different site designs
- Fallback options when automatic detection fails
