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

    base_url: str = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    api_key: str = os.getenv("QWEN_API_KEY")
    model: str = os.getenv("QWEN_MODEL", "qwen-turbo")
    temperature: float = float(os.getenv("QWEN_TEMPERATURE", "0"))

    host: str = os.getenv("CODE_CHECKER_HOST", "0.0.0.0")
    port: int = int(os.getenv("CODE_CHECKER_PORT", "8000"))

def ensure_api_key() -> str:
    """
    Ensure an OpenAI API key is available for the ChatOpenAI client.

    If QWEN_API_KEY is missing, prompt the user interactively to avoid
    accidental plaintext commits.
    """

    if not settings.api_key:
        settings.api_key = getpass.getpass("Enter API_KEY: ")
        os.environ["QWEN_API_KEY"] = settings.api_key
    return settings.api_key

def get_settings() -> Settings:
    """Return immutable settings object."""

    return Settings()


settings = get_settings()

__all__ = ["Settings", "ensure_api_key", "get_settings", "settings"]