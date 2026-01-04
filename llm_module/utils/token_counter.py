from typing import Optional, Dict, Any, Tuple

# Model context window limits (in tokens)
MODEL_CONTEXT_LIMITS = {
    # OpenAI models
    "gpt-4o": 128000,
    "gpt-4o-mini": 128000,
    "gpt-4-turbo": 128000,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-3.5-turbo": 16385,
    "gpt-3.5-turbo-16k": 16385,
    # Alibaba Cloud models
    "qwen-turbo": 8000,
    "qwen-plus": 32000,
    "qwen-max": 8000,
    "qwen-max-longcontext": 30000,
    # Default fallback
    "default": 8000,
}

class TokenCounter:
    """Token counter for LLM models"""

    def __init__(self, model: str = "qwen-turbo"):
        self.model = model

    def count_tokens(self, messages: list, model: Optional[str] = None) -> int:
        """
        Count tokens in messages for the specified model
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (optional, uses default if not provided)
            
        Returns:
            Number of tokens
        """
        if self.platform == "openai":
            return self._count_tokens_openai(messages, model)
        elif self.platform == "alibaba":
            return self._count_tokens_alibaba(messages, model)
        else:
            # Fallback: rough estimation (1 token ≈ 4 characters for English, 1.5 for Chinese)
            total_chars = sum(len(msg.get("content", "")) for msg in messages)
            return int(total_chars / 1.5)  # Rough estimate for Chinese

    def _count_tokens_openai(self, messages: list, model: Optional[str] = None) -> int:
        """Count tokens for OpenAI models using tiktoken"""
        try:
            import tiktoken
        except ImportError:
            raise ImportError("Please install tiktoken: pip install tiktoken")
        
        model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        # Map model names to encoding
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            encoding = tiktoken.get_encoding("cl100k_base")
        
        tokens_per_message = 3  # Every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = 1  # If there's a name, the role is omitted
        
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                if isinstance(value, str):
                    num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # Every reply is primed with <|start|>assistant<|message|>
        
        return num_tokens
    
    def _count_tokens_alibaba(self, messages: list, model: Optional[str] = None) -> int:
        """Count tokens for Alibaba Cloud models"""
        # Alibaba Cloud uses character-based estimation
        # Rough estimation: 1 token ≈ 1.5 characters for Chinese text
        total_chars = 0
        for message in messages:
            content = message.get("content", "")
            if isinstance(content, str):
                total_chars += len(content)
        return int(total_chars / 1.5)

    def get_context_limit(self, model: Optional[str] = None) -> int:
        """
        Get context window limit for the specified model
        
        Args:
            model: Model name (optional, uses default if not provided)
            
        Returns:
            Context window limit in tokens
        """
        if not model:
            if self.platform == "openai":
                model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            elif self.platform == "alibaba":
                model = os.getenv("DASHSCOPE_MODEL", "qwen-turbo")
            else:
                return MODEL_CONTEXT_LIMITS["default"]
        
        # Check exact match first
        if model in MODEL_CONTEXT_LIMITS:
            return MODEL_CONTEXT_LIMITS[model]
        
        # Check partial match (e.g., "gpt-4-turbo-preview" matches "gpt-4-turbo")
        for key, value in MODEL_CONTEXT_LIMITS.items():
            if key in model or model in key:
                return value
        
        return MODEL_CONTEXT_LIMITS["default"]

    def check_context_limit(
        self, 
        messages: list, 
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        raise_error: bool = False
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Check if messages exceed context window limit
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (optional, uses default if not provided)
            max_tokens: Maximum tokens to generate (for output)
            raise_error: If True, raise ValueError when limit exceeded
            
        Returns:
            Tuple of (is_within_limit, info_dict)
            info_dict contains: input_tokens, context_limit, remaining_tokens, 
                               estimated_output_tokens, is_safe
        """
        input_tokens = self.count_tokens(messages, model)
        context_limit = self.get_context_limit(model)
        estimated_output_tokens = max_tokens or 1000  # Default estimate
        total_estimated_tokens = input_tokens + estimated_output_tokens
        remaining_tokens = context_limit - input_tokens
        is_within_limit = total_estimated_tokens <= context_limit
        is_safe = remaining_tokens > estimated_output_tokens * 1.2  # 20% safety margin
        
        info = {
            "input_tokens": input_tokens,
            "context_limit": context_limit,
            "remaining_tokens": remaining_tokens,
            "estimated_output_tokens": estimated_output_tokens,
            "total_estimated_tokens": total_estimated_tokens,
            "is_within_limit": is_within_limit,
            "is_safe": is_safe,
            "usage_percentage": (input_tokens / context_limit) * 100
        }
        
        if not is_within_limit and raise_error:
            raise ValueError(
                f"Context limit exceeded! Input tokens: {input_tokens}, "
                f"Estimated total: {total_estimated_tokens}, "
                f"Context limit: {context_limit}"
            )
        
        return is_within_limit, info