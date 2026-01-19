"""
Heading hierarchy checking rule.
"""

from ..tree_checker import TreeBasedChecker
from ..base import CheckResult, CheckSeverity
from typing import List
import marko
from ...utils.tree_viewer import extract_text_from_node


def create_heading_hierarchy_checker() -> TreeBasedChecker:
    """
    Create a checker for heading hierarchy validation.
    
    Checks that headings follow a proper hierarchy (h1 -> h2 -> h3, etc.)
    """
    def check_heading_hierarchy(node: marko.ast.Node, context: dict) -> List[CheckResult]:
        """Check heading hierarchy."""
        results = []
        node_type = type(node).__name__
        
        if node_type == "Heading":
            current_level = node.level if hasattr(node, 'level') else None
            parent = context.get('parent')
            
            if current_level and parent:
                # Check parent heading level
                parent_level = None
                if hasattr(parent, 'level'):
                    parent_level = parent.level
                else:
                    # Walk up the tree to find the nearest heading
                    walk_parent = context.get('parent')
                    while walk_parent:
                        if hasattr(walk_parent, 'level'):
                            parent_level = walk_parent.level
                            break
                        # Get parent's parent from context
                        if 'parent' in context:
                            walk_parent = context.get('parent')
                        else:
                            break
                
                if parent_level is not None:
                    # Heading should not skip levels (e.g., h1 -> h3)
                    if current_level > parent_level + 1:
                        results.append(CheckResult(
                            rule_name="Heading Hierarchy",
                            severity=CheckSeverity.ERROR,
                            message=f"Heading level {current_level} should not skip from level {parent_level}",
                            context=f"Parent: {extract_text_from_node(parent)[:50]}, Current: {extract_text_from_node(node)[:50]}"
                        ))
        
        return results
    
    return TreeBasedChecker(
        name="Heading Hierarchy Checker",
        description="Checks that headings follow a proper hierarchy without skipping levels",
        check_function=check_heading_hierarchy
    )

