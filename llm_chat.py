from llm_module.core.llm_client import LLMClient

if __name__ == "__main__":
    client = LLMClient(platform="alibaba")
    try:
        messages = [
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ]
        response = client.chat(messages=messages, model="qwen-turbo", max_tokens=1000, check_context=True)
        print(response)
    except Exception as e:
        print(f"Error: {e}")