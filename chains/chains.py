"""Composable LCEL chains."""

from .models import build_chat_model
from .parsers import default_parser
from .prompts import translation_prompt

# Build once so the chain can be re-used by both CLI and server.
translation_chain = translation_prompt | build_chat_model() | default_parser

__all__ = ["translation_chain"]