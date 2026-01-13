"""
Build LangChain prompt templates from a JSON schema.

The JSON schema is demonstrated by `fibonacci_example.json`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

from langchain_core.prompts import ChatPromptTemplate


def load_json_template(path: str | Path) -> dict[str, Any]:
    """Load a prompt template JSON file into a dict."""

    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))

def escape_braces_for_langchain(text: str) -> str:
    """
    Escape all curly braces in text for LangChain prompt templates.
    
    This is a simpler version that escapes ALL curly braces, not just
    those in code blocks. Use this when you want to ensure no variable
    substitution occurs.
    
    Args:
        text: The text to escape.
    
    Returns:
        Text with all curly braces escaped as {{}}.
    """
    if not text:
        return text
    return text.replace("{", "{{").replace("}", "}}")

def build_chat_prompt_from_json_template(
    template: Mapping[str, Any],
) -> ChatPromptTemplate:
    """Build a ChatPromptTemplate from a JSON template dict."""

    role = str(template.get("role", "")).strip()
    task = str(template.get("task", "")).strip()
    context = str(template.get("context", "")).strip()

    instructions = template.get("instructions", [])
    limitations = template.get("limitations", [])
    input_desc = template.get("input", [])
    output_req = template.get("output_requirements", {}) or {}
    examples = template.get("examples", {}) or {}

    def _as_bullets(value: Any) -> list[str]:
        if not value:
            return []
        if isinstance(value, list):
            return [f"- {str(v).strip()}" for v in value if str(v).strip()]
        return [f"- {str(value).strip()}"]

    system_lines: list[str] = []
    if role:
        system_lines.append(role)
        system_lines.append("")
    if task:
        system_lines.append(f"Task: {task}")
        system_lines.append("")
    if context:
        system_lines.append("Context:")
        system_lines.append(context)
        system_lines.append("")

    if instructions:
        system_lines.append("Instructions:")
        system_lines.extend(_as_bullets(instructions))
        system_lines.append("")

    if limitations:
        system_lines.append("Limitations:")
        system_lines.extend(_as_bullets(limitations))
        system_lines.append("")

    if input_desc:
        system_lines.append("Input:")
        system_lines.extend(_as_bullets(input_desc))
        system_lines.append("")

    if output_req:
        system_lines.append("Output requirements:")
        for key, value in output_req.items():
            value_str = str(value).strip()
            if value_str:
                # Capitalize the key for better readability
                key_display = key.replace("_", " ").title()
                system_lines.append(f"- {key_display}: {value_str}")
        system_lines.append("")

    ex_in = str(examples.get("input", "")).strip()
    ex_out = str(examples.get("output", "")).strip()
    if ex_in or ex_out:
        system_lines.append("Examples:")
        if ex_in:
            system_lines.append("Input:")
            system_lines.append(ex_in)
        if ex_out:
            system_lines.append("Output:")
            system_lines.append(ex_out)
        system_lines.append("")

    user_lines: list[str] = []
    if task:
        user_lines.append(task)

    system_message = "\n".join(system_lines).strip()
    user_message = "\n".join(user_lines).strip() or "Please follow the task above."

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("user", user_message),
        ]
    )

def build_chat_prompt(
    role: str,
    task: str,
    context: str,
    instructions: list[str],
    limitations: list[str],
    input_desc: list[str],
    output_req: dict[str, Any],
    examples: dict[str, Any],
) -> ChatPromptTemplate:
    """Build a ChatPromptTemplate from a JSON template dict with dynamic parameters."""
    template = {
        "role": role,
        "task": task,
        "context": context,
        "instructions": instructions,
        "limitations": limitations,
        "input": input_desc,
        "output_requirements": output_req,
        "examples": examples,
    }
    return build_chat_prompt_from_json_template(template)

__all__ = [
    "build_chat_prompt_from_json_template",
    "build_chat_prompt",
    "load_json_template",
    "escape_braces_for_langchain",
]
