"""
Tree-based checker for complex rules that require context.

This checker is suitable for rules like:
- Document structure validation
- Heading hierarchy checks
- Cross-reference validation
- Context-dependent formatting
"""

import marko
from typing import List, Callable, Optional, Any
from .base import CheckRule, CheckResult, CheckSeverity
from ..utils.tree_viewer import extract_text_from_node


class TreeBasedChecker(CheckRule):
    """
    Checker that processes markdown as an AST tree.
    
    Suitable for rules that require understanding the document structure
    or need context from parent/child nodes.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        check_function: Callable[[marko.ast.Node, dict], List[CheckResult]]
    ):
        """
        Initialize a tree-based checker.
        
        Args:
            name: Name of the check rule
            description: Description of what this rule checks
            check_function: Function that takes (node, context) and returns
                          a list of CheckResult objects.
                          Context dict can contain parent nodes, siblings, etc.
        """
        super().__init__(name, description)
        self.check_function = check_function
    
    def check(self, content: str) -> List[CheckResult]:
        """
        Check the content by traversing the AST tree.
        
        Args:
            content: The markdown content to check
            
        Returns:
            List of CheckResult objects
        """
        # Parse markdown to AST
        doc = marko.parse(content)
        
        # Get original lines for line number mapping
        lines = content.split('\n')
        
        # Traverse tree and collect results
        results = []
        self._traverse(doc, None, lines, results, {})
        
        return results
    
    def _traverse(
        self,
        node: marko.ast.Node,
        parent: Optional[marko.ast.Node],
        lines: List[str],
        results: List[CheckResult],
        context: dict
    ):
        """
        Recursively traverse the AST tree and run checks.
        
        Args:
            node: Current AST node
            parent: Parent node (None for root)
            lines: Original content lines for line number mapping
            results: List to accumulate check results
            context: Context dictionary for passing information between nodes
        """
        # Build context for this node
        node_context = {
            'parent': parent,
            'lines': lines,
            **context
        }
        
        # Run check function on this node
        node_results = self.check_function(node, node_context)
        
        # Add line numbers to results if not already set
        for result in node_results:
            if result.line_number is None:
                # Try to extract line number from node if possible
                # This is a simplified version - you may need to enhance it
                result.line_number = self._get_node_line_number(node, lines)
            results.append(result)
        
        # Traverse children
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                if isinstance(child, marko.ast.Node):
                    # Update context with sibling information
                    siblings = [c for c in node.children if isinstance(c, marko.ast.Node)]
                    node_context['siblings'] = siblings
                    node_context['index'] = siblings.index(child) if child in siblings else -1
                    
                    self._traverse(child, node, lines, results, node_context)
    
    def _get_node_line_number(self, node: marko.ast.Node, lines: List[str]) -> Optional[int]:
        """
        Try to extract line number from node.
        
        This is a simplified implementation. You may need to enhance it
        based on the marko library's capabilities.
        """
        # Try to get text from node
        text = extract_text_from_node(node)
        if not text:
            return None
        
        # Find the first line containing this text
        for i, line in enumerate(lines, start=1):
            if text[:50] in line:  # Match first 50 chars
                return i
        
        return None



