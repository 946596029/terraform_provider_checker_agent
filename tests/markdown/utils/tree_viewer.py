def get_node_preview(node) -> str:
    """
    Get a preview string for a node to display in the tree.
    
    Args:
        node: The AST node
        
    Returns:
        str: Preview string
    """
    node_type = type(node).__name__
    preview_parts = []
    
    # For Heading nodes, show level and text
    if node_type == "Heading":
        if hasattr(node, "level"):
            preview_parts.append(f"level={node.level}")
        if hasattr(node, "children") and node.children:
            text = extract_text_from_node(node)
            if text:
                # preview_parts.append(f'"{text[:40]}"')
                preview_parts.append(f'"{text}"')
    
    # For CodeBlock, show language if available
    elif node_type == "CodeBlock":
        if hasattr(node, "lang") and node.lang:
            preview_parts.append(f"lang={node.lang}")
        if hasattr(node, "children") and node.children:
            text = extract_text_from_node(node)
            if text:
                # preview_parts.append(f"({len(text)} chars)")
                preview_parts.append(f'"{text}"')
    
    # For ListItem, show marker if available
    elif node_type == "ListItem":
        if hasattr(node, "children") and node.children:
            text = extract_text_from_node(node)
            if text:
                # preview_parts.append(f'"{text[:30]}"')
                preview_parts.append(f'"{text}"')
    
    # For Paragraph and other text nodes
    elif hasattr(node, "children") and node.children:
        text = extract_text_from_node(node)
        if text:
            # preview = text[:50].replace("\n", " ").strip()
            # if len(text) > 50:
            #     preview += "..."
            # preview_parts.append(f'"{preview}"')
            preview_parts.append(f'"{text}"')
    elif node_type == "RawText" or node_type == "CodeSpan":
        # Direct text nodes
        if hasattr(node, "children") and node.children:
            text = "".join(str(c) for c in node.children if hasattr(c, "children") or isinstance(c, str))
            if text:
                # preview_parts.append(f'"{text[:40]}"')
                preview_parts.append(f'"{text}"')
    
    # Show children count for container nodes
    if hasattr(node, "children") and node.children and not preview_parts:
        preview_parts.append(f"({len(node.children)} children)")
    
    return ": " + ", ".join(preview_parts) if preview_parts else ""
    return ": " + ", ".join(preview_parts) if preview_parts else ""


def extract_text_from_node(node) -> str:
    """
    Recursively extract text content from a node and its children.
    
    Args:
        node: The AST node
        
    Returns:
        str: Extracted text content
    """
    if not hasattr(node, "children"):
        return ""
    
    text_parts = []
    for child in node.children:
        if isinstance(child, str):
            text_parts.append(child)
        elif hasattr(child, "children"):
            if type(child).__name__ == "RawText":
                # RawText nodes contain text directly
                if child.children:
                    text_parts.extend(str(c) for c in child.children if isinstance(c, str))
            else:
                # Recursively extract from other nodes
                text_parts.append(extract_text_from_node(child))
        elif hasattr(child, "__str__"):
            text_parts.append(str(child))
    
    return "".join(text_parts).strip()


def print_ast_tree(node, prefix: str = "", is_last: bool = True, file=None) -> None:
    """
    Recursively print AST tree structure in a tree-like format.
    
    Args:
        node: The AST node to print
        prefix: Current prefix string for tree visualization
        is_last: Whether this is the last child of its parent
    """
    # Determine the connector symbol
    connector = "└── " if is_last else "├── "
    
    # Get node type name
    node_type = type(node).__name__
    
    # Get preview information
    content_preview = get_node_preview(node)
    
    # Print current node
    if file:
        file.write(f"{prefix}{connector}{node_type}{content_preview}\n")
    else:
        print(f"{prefix}{connector}{node_type}{content_preview}")
    
    # Update prefix for children
    extension = "    " if is_last else "│   "
    new_prefix = prefix + extension
    
    # Recursively print children
    if hasattr(node, "children") and node.children:
        children = node.children
        for i, child in enumerate(children):
            node_type = type(child).__name__
            if node_type == "str":
                continue
            is_last_child = (i == len(children) - 1)
            print_ast_tree(child, new_prefix, is_last_child, file)

__all__ = ["print_ast_tree"]

