"""Model factory for LangChain examples."""

from typing import Optional

from langchain_openai import ChatOpenAI

from ..config import settings, ensure_api_key


def build_chat_model(
    temperature: Optional[float] = None,
) -> ChatOpenAI:
    """
    Construct a ChatOpenAI client with sensible defaults.

    Environment variables:
        QWEN_BASE_URL:      overrides default base url.
        QWEN_API_KEY:       required for authentication.
        QWEN_MODEL:         overrides default model name.
        QWEN_TEMPERATURE:   overrides default temperature.
    """

    ensure_api_key()
    return ChatOpenAI(
        base_url=settings.base_url,
        api_key=settings.api_key,
        model=settings.model,
        temperature=temperature if temperature is not None else settings.temperature,
    )


__all__ = ["build_chat_model"]