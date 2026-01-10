"""Model factory for LangChain examples."""

from typing import Optional

from langchain_openai import ChatOpenAI

from ..config import settings, ensure_api_key


def build_chat_model(
    model: Optional[str] = None,
    temperature: Optional[float] = None,
) -> ChatOpenAI:
    """
    Construct a ChatOpenAI client with sensible defaults.

    Environment variables:
        OPENAI_API_KEY: required for authentication.
        OPENAI_MODEL:   overrides default model name.
        OPENAI_TEMPERATURE: overrides default temperature.
    """

    ensure_api_key()
    return ChatOpenAI(
        model=model or settings.model,
        temperature=temperature if temperature is not None else settings.temperature,
    )


__all__ = ["build_chat_model"]