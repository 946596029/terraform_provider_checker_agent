"""
Command-line entrypoint for the LangChain prompt template example.
"""

from ..chains import fibonacci_chain
from ..config import ensure_api_key

def fibonacci() -> str:
    """Run the fibonacci chain for the provided number of Fibonacci numbers."""

    ensure_api_key()
    return fibonacci_chain.invoke({})


def main() -> None:
    fibonacci_sequence = fibonacci()
    print(fibonacci_sequence)

if __name__ == "__main__":
    main()