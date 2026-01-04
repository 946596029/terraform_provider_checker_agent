from llm_module.core.llm_client import LLMClient

if __name__ == "__main__":
    client = LLMClient(platform="alibaba")
    messages = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！很高兴认识你"},
        {"role": "user", "content": "你叫什么名字？"},
        {"role": "assistant", "content": "我叫小明"},
        {"role": "user", "content": "你今年多大了？"},
        {"role": "assistant", "content": "我今年20岁"},
    ]
    try:
        response = client.chat(messages=messages, model="qwen-turbo", max_tokens=1000, check_context=True)
        print(response)
    except Exception as e:
        print(f"Error: {e}")