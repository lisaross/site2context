"""
Custom exceptions for HTML to Markdown conversion.
"""

class ConversionError(Exception):
    """Raised when HTML to Markdown conversion fails."""
    pass

class ConfigError(Exception):
    """Raised when there's an error in configuration."""
    pass 