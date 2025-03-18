"""
Tests for the core HTML to Markdown conversion functionality.
"""
import pytest
from pathlib import Path
from html2md.config import Config
from html2md.core import HTMLConverter
from html2md.exceptions import ConversionError

@pytest.fixture
def sample_html():
    """Create a sample HTML file for testing."""
    html_content = """
    <html>
        <body>
            <div class="main-content">
                <h1>Test Page</h1>
                <p>This is a test paragraph.</p>
                <div class="navigation">Should be excluded</div>
            </div>
        </body>
    </html>
    """
    return html_content

@pytest.fixture
def config():
    """Create a test configuration."""
    return Config(
        input_dir=Path("test_input"),
        output_dir=Path("test_output"),
        content_selector="div.main-content",
        exclude_selectors=["div.navigation"],
        preserve_links=True,
        preserve_images=True
    )

@pytest.fixture
def converter(config):
    """Create a converter instance for testing."""
    return HTMLConverter(config)

def test_convert_file(converter, sample_html, tmp_path):
    """Test converting a single HTML file to markdown."""
    # Create a temporary HTML file
    input_file = tmp_path / "test.html"
    input_file.write_text(sample_html)
    
    # Convert the file
    markdown = converter.convert_file(input_file)
    
    # Check the output
    assert "# Test Page" in markdown
    assert "This is a test paragraph." in markdown
    assert "Should be excluded" not in markdown

def test_convert_file_no_content(converter, tmp_path):
    """Test handling of HTML file with no matching content."""
    html_content = "<html><body><div>No main content here</div></body></html>"
    input_file = tmp_path / "test.html"
    input_file.write_text(html_content)
    
    with pytest.raises(ConversionError):
        converter.convert_file(input_file)

def test_process_directory(converter, sample_html, tmp_path):
    """Test processing a directory of HTML files."""
    # Create input directory with test files
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "test1.html").write_text(sample_html)
    (input_dir / "test2.html").write_text(sample_html)
    
    # Create output directory
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    # Process the directory
    converter.process_directory(input_dir, output_dir)
    
    # Check output files
    assert (output_dir / "test1.md").exists()
    assert (output_dir / "test2.md").exists()
    
    # Check content of output files
    content = (output_dir / "test1.md").read_text()
    assert "# Test Page" in content
    assert "This is a test paragraph." in content
    assert "Should be excluded" not in content 