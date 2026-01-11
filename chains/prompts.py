"""Prompt templates for LCEL chains."""

from langchain_core.prompts import ChatPromptTemplate

from code_checker.prompt_template.prompt_builder import (
    build_chat_prompt_from_json_template,
    load_json_template,
)

# Translation prompt
translation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Translate the following into {language}:",
        ),
        (
            "user", 
            "{text}"
        ),
    ]
)

# Fibonacci prompt
fibonacci_prompt = build_chat_prompt_from_json_template(
    load_json_template(
        "code_checker/prompt_template/fibonacci_example.json"
    )
)

__all__ = ["translation_prompt", "fibonacci_prompt"]