"""
Markdown checkers module.

This module provides a flexible checking system that supports different data
structures for different check rules:
- Line-based checkers: For simple rules that don't require context (e.g., number format)
- Tree-based checkers: For complex rules that require context (e.g., structure validation)
"""

from .base import CheckRule, CheckResult
from .line_checker import LineBasedChecker
from .tree_checker import TreeBasedChecker
from .manager import CheckerManager

__all__ = [
    "CheckRule",
    "CheckResult",
    "LineBasedChecker",
    "TreeBasedChecker",
    "CheckerManager",
]

