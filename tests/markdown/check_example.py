"""
Example usage of the flexible checker system.

This demonstrates how different check rules can use different data structures:
- Line-based checkers for simple rules (e.g., number format)
- Tree-based checkers for complex rules requiring context
"""

from pathlib import Path
from .checkers.manager import CheckerManager
from .checkers.rules import (
    create_number_format_checker,
    create_heading_hierarchy_checker,
)


def main():
    """Run example checks on a markdown file."""
    # Read markdown file
    md_file = Path(__file__).parent / "cdn_cache_refresh.md"
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Create checker manager
    manager = CheckerManager()
    
    # Register different types of checkers
    # Line-based checker (for simple rules like number format)
    number_checker = create_number_format_checker()
    manager.register_line_checker(number_checker)
    
    # Tree-based checker (for complex rules requiring context)
    heading_checker = create_heading_hierarchy_checker()
    manager.register_tree_checker(heading_checker)
    
    # Run all checks
    print("Running all checks...")
    print(f"Registered checkers: {manager.list_checkers()}\n")
    
    results = manager.check(content)
    
    # Display results
    print(f"Found {len(results)} issues:\n")
    for result in results:
        print(result)
        print()
    
    # Example: Run only specific checkers
    print("\n" + "="*60)
    print("Running only number format checker...")
    print("="*60 + "\n")
    
    number_results = manager.check(content, checker_names=["Number Format Checker"])
    for result in number_results:
        print(result)
        print()


if __name__ == "__main__":
    main()

