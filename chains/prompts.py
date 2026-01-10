"""Prompt templates for the translation chain."""

from langchain_core.prompts import ChatPromptTemplate

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

__all__ = ["translation_prompt"]