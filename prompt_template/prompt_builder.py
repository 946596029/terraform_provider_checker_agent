"""
Build LangChain prompt templates from a JSON schema.

The JSON schema is demonstrated by `fibonacci_example.json`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from langchain_core.prompts import ChatPromptTemplate


def load_json_template(path: str | Path) -> dict[str, Any]:
    """Load a prompt template JSON file into a dict."""

    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))


def build_chat_prompt_from_json_template(
    template: Mapping[str, Any],
) -> ChatPromptTemplate:
    """Build a ChatPromptTemplate from a JSON template dict."""

    role = str(template.get("role", "")).strip()
    task = str(template.get("task", "")).strip()

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
        fmt = str(output_req.get("format", "")).strip()
        lang = str(output_req.get("language", "")).strip()
        length = str(output_req.get("length", "")).strip()
        if fmt:
            system_lines.append(f"- Format: {fmt}")
        if lang:
            system_lines.append(f"- Language: {lang}")
        if length:
            system_lines.append(f"- Length: {length}")
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


def build_fibonacci_prompt() -> ChatPromptTemplate:
    """Build a ChatPromptTemplate using fibonacci_example.json."""

    template_path = Path(__file__).resolve().parent / "fibonacci_example.json"
    template = load_json_template(template_path)
    return build_chat_prompt_from_json_template(template)


__all__ = [
    "build_chat_prompt_from_json_template",
    "build_fibonacci_prompt",
    "load_json_template",
]

