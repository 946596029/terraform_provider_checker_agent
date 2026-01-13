"""
Command-line entrypoint for the LangChain translation example.
"""

import argparse

from .chains import translation_chain
from .config import ensure_api_key

def translate(language: str, text: str) -> str:
    """Run the translation chain for the provided language and text."""

    ensure_api_key()
    return translation_chain.invoke({"language": language, "text": text})


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Translate text using the LangChain LCEL example."
    )
    parser.add_argument(
        "--language",
        "-l",
        default="chinese",
        help="Target language, e.g., 'english' or 'chinese'.",
    )
    parser.add_argument(
        "--text",
        "-t",
        default="hi!",
        help="Text to translate.",
    )
    args = parser.parse_args()

    translated = translate(args.language, args.text)
    print(translated)

    fibonacci = fibonacci(args.n)
    print(fibonacci)

if __name__ == "__main__":
    main()