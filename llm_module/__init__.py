"""
LLM Module - Multi-Cloud Platform LLM API
Supports: OpenAI, Azure OpenAI, AWS Bedrock, Google Cloud, Alibaba Cloud, Tencent Cloud, Baidu
"""

from .core.llm_client import LLMClient
from .utils.token_counter import TokenCounter, MODEL_CONTEXT_LIMITS

# Export main classes and constants
__all__ = [
    "LLMClient",
    "TokenCounter",
    "MODEL_CONTEXT_LIMITS",
]

# Module metadata
__version__ = "1.0.0"
__author__ = "Terraform Provider Checker Agent"

