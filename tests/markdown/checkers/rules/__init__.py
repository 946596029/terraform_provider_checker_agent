"""
Predefined check rules.
"""

from .number_format import create_number_format_checker
from .heading_hierarchy import create_heading_hierarchy_checker

__all__ = [
    "create_number_format_checker",
    "create_heading_hierarchy_checker",
]

