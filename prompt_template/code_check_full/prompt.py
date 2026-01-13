from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

from ..prompt_builder import build_chat_prompt, escape_braces_for_langchain

def read_file_content(file_path: Path) -> str:
    """Read file content from the given path."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def build_code_check_full_prompt() -> ChatPromptTemplate:
    """Build the code check full prompt template.
    
    This function reads the checker rules and Go code file, then builds
    a ChatPromptTemplate for code checking.
    
    Returns:
        ChatPromptTemplate: The configured prompt template for code checking.
    """
    role = "code checker"
    task = "检查代码是否代码规范"

    checker_rules = read_file_content(Path(__file__).parent / "resource-auto-gen.md")
    checker_rules = escape_braces_for_langchain(checker_rules)
    checker_rules_block = f"```markdown\n{checker_rules}\n```"
    context = checker_rules_block

    instructions = []
    limitations = [
        "仅遵从传入的代码规范"
    ]

    go_code_content = read_file_content(Path(__file__).parent / "resource_huaweicloud_aom_application.go")
    go_code_content = escape_braces_for_langchain(go_code_content)
    code_block = f"```go\n{go_code_content}\n```"
    input = [code_block]
    
    output_requirements = {
        "format": "markdown",
        "language": "中文",
        "description": "按条展示检查结果，并给出详细解释"
    }

    examples = {}
    
    # Write parameters to output.txt before building the prompt
    output_path = Path(__file__).parent / "output.txt"
    # Clear the file before writing
    output_path.write_text("", encoding="utf-8")
    
    output_content = []
    output_content.append("=== Prompt Parameters ===")
    output_content.append("")
    output_content.append(f"role: {role}")
    output_content.append("")
    output_content.append(f"task: {task}")
    output_content.append("")
    output_content.append(f"context:\n{context}")
    output_content.append("")
    output_content.append(f"instructions: {instructions}")
    output_content.append("")
    output_content.append(f"limitations: {limitations}")
    output_content.append("")
    output_content.append(f"input_desc:\n" + "\n".join(input))
    output_content.append("")
    output_content.append(f"output_req: {output_requirements}")
    output_content.append("")
    output_content.append(f"examples: {examples}")
    output_content.append("")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_content))
    
    return build_chat_prompt(
        role=role,
        task=task,
        context=context,
        instructions=instructions,
        limitations=limitations,
        input_desc=input,
        output_req=output_requirements,
        examples=examples,
    )

# Export the prompt as an object (not a function) for use in LCEL chains
code_check_full_prompt = build_code_check_full_prompt()

__all__ = ["code_check_full_prompt"]