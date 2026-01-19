"""
Base classes for markdown checkers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Any
from enum import Enum


class CheckSeverity(Enum):
    """Severity level of a check result."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class CheckResult:
    """Result of a single check."""
    rule_name: str
    severity: CheckSeverity
    message: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    context: Optional[str] = None
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        """String representation of the check result."""
        location = ""
        if self.line_number is not None:
            location = f"Line {self.line_number}"
            if self.column_number is not None:
                location += f", Column {self.column_number}"
            location += ": "
        
        result = f"[{self.severity.value.upper()}] {self.rule_name}: {location}{self.message}"
        
        if self.suggestion:
            result += f"\n  Suggestion: {self.suggestion}"
        
        if self.context:
            result += f"\n  Context: {self.context}"
        
        return result


class CheckRule(ABC):
    """Base class for all check rules."""
    
    def __init__(self, name: str, description: str):
        """
        Initialize a check rule.
        
        Args:
            name: Name of the check rule
            description: Description of what this rule checks
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def check(self, *args, **kwargs) -> List[CheckResult]:
        """
        Perform the check and return results.
        
        Returns:
            List of CheckResult objects
        """
        pass

