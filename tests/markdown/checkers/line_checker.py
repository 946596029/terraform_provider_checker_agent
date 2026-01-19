"""
Line-based checker for simple rules that don't require context.

This checker is suitable for rules like:
- Number format checking
- Simple pattern matching
- Line-level validation
"""

from typing import List, Callable, Optional
from .base import CheckRule, CheckResult


class LineBasedChecker(CheckRule):
    """
    Checker that processes markdown content line by line.
    
    Suitable for rules that don't require understanding the document structure
    or context from other parts of the document.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        check_function: Callable[[str, int], Optional[CheckResult]]
    ):
        """
        Initialize a line-based checker.
        
        Args:
            name: Name of the check rule
            description: Description of what this rule checks
            check_function: Function that takes (line_content, line_number) and
                          returns CheckResult or None
        """
        super().__init__(name, description)
        self.check_function = check_function
    
    def check(self, content: str) -> List[CheckResult]:
        """
        Check the content line by line.
        
        Args:
            content: The markdown content to check
            
        Returns:
            List of CheckResult objects
        """
        results = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            result = self.check_function(line, line_num)
            if result:
                results.append(result)
        
        return results

