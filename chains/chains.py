"""Composable LCEL chains."""

from .models import build_chat_model
from .parsers import default_parser
from .prompts import translation_prompt, fibonacci_prompt, code_check_full_prompt, code_check_small_prompt

# Build once so the chain can be re-used by both CLI and server.
translation_chain = translation_prompt | build_chat_model() | default_parser

# Build fibonacci chain
fibonacci_chain = fibonacci_prompt | build_chat_model() | default_parser

# Build code check full chain
code_check_full_chain = code_check_full_prompt | build_chat_model() | default_parser

# Build code check small chain
code_check_small_chain = code_check_small_prompt | build_chat_model() | default_parser

__all__ = [
    "translation_chain", 
    "fibonacci_chain",
    "code_check_full_chain",
    "code_check_small_chain"
]