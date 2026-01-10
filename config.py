"""
Shared configuration for LangChain examples.
"""

import getpass
import os

from dotenv import load_dotenv

from dataclasses import dataclass

load_dotenv()

@dataclass(frozen=True)
class Settings:
    """Runtime settings with environment variable overrides."""

    model: str = os.getenv("QWEN_MODEL", "qwen-turbo")
    temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0"))
    host: str = os.getenv("LANGCHAIN_HOST", "0.0.0.0")
    port: int = int(os.getenv("LANGCHAIN_PORT", "8000"))


def ensure_api_key() -> str:
    """
    Ensure an OpenAI API key is available for the ChatOpenAI client.

    If OPENAI_API_KEY is missing, prompt the user interactively to avoid
    accidental plaintext commits.
    """

    api_key = os.getenv("QWEN_API_KEY")
    if not api_key:
        api_key = getpass.getpass("Enter API_KEY: ")
        os.environ["QWEN_API_KEY"] = api_key
    return api_key


def get_settings() -> Settings:
    """Return immutable settings object."""

    return Settings()


settings = get_settings()

__all__ = ["Settings", "ensure_api_key", "get_settings", "settings"]