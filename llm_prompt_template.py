from llm_module.core.llm_client import LLMClient
from prompt_module import PromptTemplate, PromptConverter

if __name__ == "__main__":
    client = LLMClient(platform="alibaba")
    try:
        template = PromptTemplate.from_json_file("prompt_module/templates/fibonacci_example.json")
        converter = PromptConverter()
        markdown_prompt = converter.to_markdown(template)
        messages = [
            {"role": "user", "content": markdown_prompt}
        ]
        response = client.chat(messages=messages, model="qwen-turbo", max_tokens=1000, check_context=True)
        print(response)
    except Exception as e:
        print(f"Error: {e}")