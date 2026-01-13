from ..prompt_builder import build_chat_prompt_from_json_template, load_json_template

fibonacci_prompt = build_chat_prompt_from_json_template(
    load_json_template("code_checker/prompt_template/fibonacci/fibonacci_example.json")
)

__all__ = ["fibonacci_prompt"]