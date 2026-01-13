"""FastAPI router exposing the translation chain via LangServe."""

from .server import app

__all__ = ["app"]
