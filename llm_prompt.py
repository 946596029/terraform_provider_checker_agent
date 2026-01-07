from llm_module.core.llm_client import LLMClient

if __name__ == "__main__":
    client = LLMClient(platform="alibaba")
    try:

        prompt = """
# 角色：你是一位专业的编程专家

# 任务：编写一个 斐波那契数列 的程序

# 上下文：
- 你需要使用 Rust 语言

# 输入：
- 不需要输入

# 输出要求：
- 格式：代码
- 语言：Rust
- 长度：100 行以内

# 示例：
- 输入：

- 输出：
```rust
fn main() {
    println!("Hello, World!");
}
```

# 请按照以上要求完成任务。
        """
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        response = client.chat(messages=messages, model="qwen-turbo", max_tokens=1000, check_context=True)
        print(response)
    except Exception as e:
        print(f"Error: {e}")