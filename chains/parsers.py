"""Output parsers for LangChain examples."""

from langchain_core.output_parsers import StrOutputParser

default_parser = StrOutputParser()

__all__ = ["default_parser"]