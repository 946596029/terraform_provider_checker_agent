"""
Command-line entrypoint for the LangChain code check example.
"""

from pathlib import Path

from ..chains import code_check_full_chain
from ..config import ensure_api_key

def code_check_full() -> str:
    """Run the code check chain for the provided code."""

    ensure_api_key()
    return code_check_full_chain.invoke({})


def main() -> None:
    code_check_full_sequence = code_check_full()
    print(code_check_full_sequence)
    
    # Write result to result.txt
    result_path = Path(__file__).parent / "result.txt"
    result_path.write_text(code_check_full_sequence, encoding="utf-8")

if __name__ == "__main__":
    main()