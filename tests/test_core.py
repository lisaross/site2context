"""
Tests for the core HTML to Markdown conversion functionality.
"""

import pytest
from pathlib import Path
from html2md.core import convert_html_to_md, process_directory

def test_convert_html_to_md():
    """Test basic HTML to Markdown conversion."""
    html_content = """
    <div class="main-content">
        <h1>Test Title</h1>
        <p>Test paragraph with <strong>bold</strong> text.</p>
        <div class="navigation">Should be excluded</div>
    </div>
    """
    
    config = {
        'content_selector': 'div.main-content',
        'exclude_selectors': ['div.navigation'],
        'preserve_links': True,
        'preserve_images': True
    }
    
    expected = "# Test Title\n\nTest paragraph with **bold** text."
    result = convert_html_to_md(html_content, config)
    assert result.strip() == expected.strip()

def test_process_directory(tmp_path):
    """Test processing a directory of HTML files."""
    # Create test HTML files
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    
    (input_dir / "test1.html").write_text("""
    <div class="main-content">
        <h1>Test 1</h1>
        <p>Content 1</p>
    </div>
    """)
    
    (input_dir / "test2.html").write_text("""
    <div class="main-content">
        <h1>Test 2</h1>
        <p>Content 2</p>
    </div>
    """)
    
    # Create output directory
    output_dir = tmp_path / "output"
    
    # Process files
    config = {
        'content_selector': 'div.main-content',
        'exclude_selectors': [],
        'preserve_links': True,
        'preserve_images': True
    }
    
    process_directory(input_dir, output_dir, config)
    
    # Check output files
    assert (output_dir / "test1.md").exists()
    assert (output_dir / "test2.md").exists()
    
    # Check content
    test1_content = (output_dir / "test1.md").read_text()
    assert "Test 1" in test1_content
    assert "Content 1" in test1_content
    
    test2_content = (output_dir / "test2.md").read_text()
    assert "Test 2" in test2_content
    assert "Content 2" in test2_content
