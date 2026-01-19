# Markdown Checker System

A flexible checking system that supports different data structures for different
check rules.

## Overview

Different check rules have different requirements:
- **Simple rules** (e.g., number format checking) don't require context and are
  better suited for line-by-line processing
- **Complex rules** (e.g., structure validation) require understanding the
  document structure and are better suited for tree traversal

This system provides two types of checkers:
1. **LineBasedChecker**: Processes content line by line
2. **TreeBasedChecker**: Processes content as an AST tree

## Architecture

### Base Classes

- `CheckRule`: Abstract base class for all check rules
- `CheckResult`: Data class representing a single check result
- `CheckSeverity`: Enum for severity levels (ERROR, WARNING, INFO)

### Checker Types

#### LineBasedChecker

Suitable for rules that:
- Don't require document structure understanding
- Can be checked independently on each line
- Examples: number format, simple pattern matching

```python
from checkers.line_checker import LineBasedChecker
from checkers.base import CheckResult, CheckSeverity

def my_check_function(line: str, line_num: int) -> Optional[CheckResult]:
    # Your check logic here
    if some_condition:
        return CheckResult(
            rule_name="My Rule",
            severity=CheckSeverity.WARNING,
            message="Issue found",
            line_number=line_num
        )
    return None

checker = LineBasedChecker(
    name="My Line Checker",
    description="Checks something line by line",
    check_function=my_check_function
)
```

#### TreeBasedChecker

Suitable for rules that:
- Require understanding document structure
- Need context from parent/child nodes
- Examples: heading hierarchy, cross-references, structure validation

```python
from checkers.tree_checker import TreeBasedChecker
from checkers.base import CheckResult, CheckSeverity
import marko

def my_tree_check_function(node: marko.ast.Node, context: dict) -> List[CheckResult]:
    results = []
    # Your check logic here
    # context contains: 'parent', 'siblings', 'lines', etc.
    if some_condition:
        results.append(CheckResult(
            rule_name="My Tree Rule",
            severity=CheckSeverity.ERROR,
            message="Structure issue found"
        ))
    return results

checker = TreeBasedChecker(
    name="My Tree Checker",
    description="Checks document structure",
    check_function=my_tree_check_function
)
```

### CheckerManager

The `CheckerManager` coordinates different types of checkers:

```python
from checkers.manager import CheckerManager
from checkers.rules import (
    create_number_format_checker,
    create_heading_hierarchy_checker,
)

# Create manager
manager = CheckerManager()

# Register checkers
manager.register_line_checker(create_number_format_checker())
manager.register_tree_checker(create_heading_hierarchy_checker())

# Run all checks
results = manager.check(markdown_content)

# Or run specific checkers
results = manager.check(markdown_content, checker_names=["Number Format Checker"])

# List all registered checkers
print(manager.list_checkers())
```

## Predefined Rules

### Number Format Checker

Checks that large numbers (>= 1000) are formatted with comma separators.

Example:
- `4096` → Should be `4,096`
- `1000` → Should be `1,000`

### Heading Hierarchy Checker

Checks that headings follow a proper hierarchy without skipping levels.

Example:
- Valid: h1 → h2 → h3
- Invalid: h1 → h3 (skipping h2)

## Usage Example

See `check_example.py` for a complete example:

```python
from pathlib import Path
from checkers.manager import CheckerManager
from checkers.rules import (
    create_number_format_checker,
    create_heading_hierarchy_checker,
)

# Read markdown file
md_file = Path("cdn_cache_refresh.md")
with open(md_file, "r", encoding="utf-8") as f:
    content = f.read()

# Create and configure manager
manager = CheckerManager()
manager.register_line_checker(create_number_format_checker())
manager.register_tree_checker(create_heading_hierarchy_checker())

# Run checks
results = manager.check(content)

# Display results
for result in results:
    print(result)
```

## Creating Custom Rules

### Line-based Rule

1. Create a check function that takes `(line: str, line_num: int)` and returns
   `Optional[CheckResult]`
2. Wrap it in a `LineBasedChecker`
3. Register with the manager

### Tree-based Rule

1. Create a check function that takes `(node: marko.ast.Node, context: dict)`
   and returns `List[CheckResult]`
2. Wrap it in a `TreeBasedChecker`
3. Register with the manager

The context dictionary contains:
- `parent`: Parent node
- `siblings`: List of sibling nodes
- `index`: Index of current node among siblings
- `lines`: Original content lines

## Benefits

1. **Flexibility**: Each rule uses the most appropriate data structure
2. **Performance**: Simple rules don't need to parse the entire AST
3. **Extensibility**: Easy to add new rules of either type
4. **Separation of Concerns**: Different rule types are clearly separated

