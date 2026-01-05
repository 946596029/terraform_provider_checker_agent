"""
Prompt Module - Structured Prompt Template System
Supports JSON-based prompt templates and converts them to Markdown format for LLM
"""

from .core.prompt_template import PromptTemplate
from .core.prompt_converter import PromptConverter

# Export main classes
__all__ = [
    "PromptTemplate",
    "PromptConverter",
]

# Module metadata
__version__ = "1.0.0"
__author__ = "Terraform Provider Checker Agent"

