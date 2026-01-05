"""
Prompt Converter - Converts JSON prompt templates to Markdown format
"""

import json
from typing import Dict, Any, List
from .prompt_template import PromptTemplate


class PromptConverter:
    """Converts structured JSON prompt templates to Markdown format"""

    @staticmethod
    def to_markdown(template: PromptTemplate, wrap_width: int = 120) -> str:
        """
        Convert prompt template to Markdown format
        
        Args:
            template: PromptTemplate instance
            wrap_width: Maximum line width for wrapping (default: 120)
            
        Returns:
            Markdown formatted string
        """
        data = template.to_dict()
        markdown_parts = []
        
        # Role
        if data.get("role"):
            markdown_parts.append(f"# 角色：{data['role']}")
            markdown_parts.append("")
        
        # Task
        if data.get("task"):
            markdown_parts.append(f"# 任务：{data['task']}")
            markdown_parts.append("")
        
        # Context
        context = data.get("context", [])
        if context:
            markdown_parts.append("# 上下文：")
            for item in context:
                if isinstance(item, str):
                    markdown_parts.append(f"- {PromptConverter._wrap_text(item, wrap_width)}")
                elif isinstance(item, dict):
                    # Handle nested context items
                    for key, value in item.items():
                        if isinstance(value, list):
                            markdown_parts.append(f"- {key}:")
                            for sub_item in value:
                                markdown_parts.append(f"  - {PromptConverter._wrap_text(str(sub_item), wrap_width)}")
                        else:
                            markdown_parts.append(f"- {key}: {PromptConverter._wrap_text(str(value), wrap_width)}")
            markdown_parts.append("")
        
        # Input
        input_data = data.get("input", [])
        if input_data:
            markdown_parts.append("# 输入：")
            for item in input_data:
                if isinstance(item, str):
                    markdown_parts.append(f"- {PromptConverter._wrap_text(item, wrap_width)}")
                elif isinstance(item, dict):
                    for key, value in item.items():
                        markdown_parts.append(f"- {key}: {PromptConverter._wrap_text(str(value), wrap_width)}")
            markdown_parts.append("")
        
        # Output Requirements
        output_req = data.get("output_requirements", {})
        if output_req and any(output_req.values()):
            markdown_parts.append("# 输出要求：")
            for key, value in output_req.items():
                if value:
                    markdown_parts.append(f"- {key}：{PromptConverter._wrap_text(str(value), wrap_width)}")
            markdown_parts.append("")
        
        # Examples
        examples = data.get("examples", {})
        if examples and (examples.get("input") or examples.get("output")):
            markdown_parts.append("# 示例：")
            if examples.get("input"):
                markdown_parts.append(f"- 输入：")
                input_example = examples["input"]
                if isinstance(input_example, str):
                    markdown_parts.append(f"  {PromptConverter._wrap_text(input_example, wrap_width)}")
                else:
                    markdown_parts.append(f"  {json.dumps(input_example, ensure_ascii=False, indent=2)}")
            if examples.get("output"):
                markdown_parts.append(f"- 输出：")
                output_example = examples["output"]
                if isinstance(output_example, str):
                    # Check if it's code block
                    if "```" in output_example:
                        markdown_parts.append(f"  {output_example}")
                    else:
                        markdown_parts.append(f"  {PromptConverter._wrap_text(output_example, wrap_width)}")
                else:
                    markdown_parts.append(f"  {json.dumps(output_example, ensure_ascii=False, indent=2)}")
            markdown_parts.append("")
        
        # Additional Instructions
        additional = data.get("additional_instructions", "")
        if additional:
            markdown_parts.append(f"# 请按照以上要求完成任务。")
            if additional.strip():
                markdown_parts.append("")
                markdown_parts.append(PromptConverter._wrap_text(additional, wrap_width))
        else:
            markdown_parts.append(f"# 请按照以上要求完成任务。")
        
        return "\n".join(markdown_parts)

    @staticmethod
    def _wrap_text(text: str, width: int) -> str:
        """
        Wrap text to specified width
        
        Args:
            text: Text to wrap
            width: Maximum line width
            
        Returns:
            Wrapped text
        """
        if len(text) <= width:
            return text
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            # If adding this word would exceed width, start a new line
            if current_length + word_length + len(current_line) > width and current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length + 1
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return "\n  ".join(lines)

