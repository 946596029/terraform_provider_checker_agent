"""
LLM Module - Multi-Cloud Platform LLM API Examples
Supports: OpenAI, Azure OpenAI, AWS Bedrock, Google Cloud, Alibaba Cloud, Tencent Cloud, Baidu
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMClient:
    """Unified LLM client supporting multiple cloud platforms"""

    def __init__(self, platform: str = "openai"):
        """
        Initialize LLM client for specified platform
        
        Args:
            platform: Platform name (openai, azure, aws, google, alibaba, tencent, baidu)
        """
        self.platform = platform.lower()
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize client based on platform"""
        if self.platform == "openai":
            self._init_openai()
        elif self.platform == "alibaba":
            self._init_alibaba()
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")

    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            self._client = openai.OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("Please install openai: pip install openai")

    def _init_alibaba(self):
        """Initialize Alibaba Cloud Tongyi client"""
        try:
            import dashscope
            api_key = os.getenv("DASHSCOPE_API_KEY")
            if not api_key:
                raise ValueError("DASHSCOPE_API_KEY not found")
            dashscope.api_key = api_key
            self._client = dashscope
        except ImportError:
            raise ImportError("Please install dashscope: pip install dashscope")

    def chat(
        self,
        messages: list,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send chat completion request
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (optional, uses default if not provided)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional platform-specific parameters
            
        Returns:
            Response dict with 'content' and metadata
        """
        if self.platform == "openai":
            return self._chat_openai(messages, model, temperature, max_tokens, **kwargs)
        elif self.platform == "alibaba":
            return self._chat_alibaba(messages, model, temperature, max_tokens, **kwargs)

    def _chat_openai(self, messages, model, temperature, max_tokens, **kwargs):
        """OpenAI chat completion"""
        model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        response = self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }

    def _chat_alibaba(self, messages, model, temperature, max_tokens, **kwargs):
        """Alibaba Cloud Tongyi chat completion"""
        from dashscope import Generation
        model = model or os.getenv("DASHSCOPE_MODEL", "qwen-turbo")
        
        # Convert messages format
        prompt = messages[-1]["content"] if messages else ""
        history = []
        for i in range(len(messages) - 1):
            if messages[i]["role"] == "user":
                history.append({"user": messages[i]["content"], "bot": messages[i+1]["content"]})
        
        response = Generation.call(
            model=model,
            prompt=prompt,
            history=history,
            temperature=temperature,
            max_tokens=max_tokens or 2000
        )
        
        if response.status_code == 200:
            return {
                "content": response.output.text,
                "model": model,
                "usage": response.usage
            }
        else:
            raise Exception(f"API Error: {response.message}")

# Example usage
if __name__ == "__main__":    
    # Example 1: Alibaba Cloud Tongyi
    print("\n=== Alibaba Cloud Tongyi Example ===")
    try:
        client = LLMClient(platform="alibaba")
        messages = [
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ]
        response = client.chat(messages=messages)
        print(f"Response: \n{response['content']}")
    except Exception as e:
        print(f"Error: {e}")
