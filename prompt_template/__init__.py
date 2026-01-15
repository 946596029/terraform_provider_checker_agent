"""
Prompt templates for LangChain.
"""

from .fibonacci.prompt import fibonacci_prompt
from .translation.prompt import translation_prompt
from .code_check_full.prompt import code_check_full_prompt
from .code_check_small.prompt import code_check_small_prompt

__all__ = [
    "fibonacci_prompt",
    "translation_prompt",
    "code_check_full_prompt",
    "code_check_small_prompt",
]