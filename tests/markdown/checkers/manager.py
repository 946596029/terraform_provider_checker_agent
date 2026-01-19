"""
Checker manager for coordinating different types of checkers.
"""

from typing import List, Dict
from .base import CheckRule, CheckResult
from .line_checker import LineBasedChecker
from .tree_checker import TreeBasedChecker


class CheckerManager:
    """
    Manager for coordinating different types of checkers.
    
    This manager allows you to register different checkers and run them
    on markdown content, automatically using the appropriate data structure
    for each checker type.
    """
    
    def __init__(self):
        """Initialize the checker manager."""
        self.line_checkers: List[LineBasedChecker] = []
        self.tree_checkers: List[TreeBasedChecker] = []
        self.all_checkers: Dict[str, CheckRule] = {}
    
    def register_line_checker(self, checker: LineBasedChecker):
        """
        Register a line-based checker.
        
        Args:
            checker: The line-based checker to register
        """
        self.line_checkers.append(checker)
        self.all_checkers[checker.name] = checker
    
    def register_tree_checker(self, checker: TreeBasedChecker):
        """
        Register a tree-based checker.
        
        Args:
            checker: The tree-based checker to register
        """
        self.tree_checkers.append(checker)
        self.all_checkers[checker.name] = checker
    
    def check(self, content: str, checker_names: List[str] = None) -> List[CheckResult]:
        """
        Run all registered checkers (or specified ones) on the content.
        
        Args:
            content: The markdown content to check
            checker_names: Optional list of checker names to run.
                          If None, runs all registered checkers.
        
        Returns:
            List of all CheckResult objects from all checkers
        """
        all_results = []
        
        # Run line-based checkers
        for checker in self.line_checkers:
            if checker_names is None or checker.name in checker_names:
                results = checker.check(content)
                all_results.extend(results)
        
        # Run tree-based checkers
        for checker in self.tree_checkers:
            if checker_names is None or checker.name in checker_names:
                results = checker.check(content)
                all_results.extend(results)
        
        return all_results
    
    def get_checker_info(self) -> Dict[str, str]:
        """
        Get information about all registered checkers.
        
        Returns:
            Dictionary mapping checker names to their descriptions
        """
        return {
            name: checker.description
            for name, checker in self.all_checkers.items()
        }
    
    def list_checkers(self) -> List[str]:
        """
        List all registered checker names.
        
        Returns:
            List of checker names
        """
        return list(self.all_checkers.keys())

