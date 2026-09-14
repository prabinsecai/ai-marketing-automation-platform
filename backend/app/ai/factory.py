import logging
from typing import Optional
from app.ai.base import BaseLLMProvider
from app.ai.providers.mock_provider import MockLLMProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.anthropic_provider import AnthropicProvider
from app.config import settings

logger = logging.getLogger("app.ai.factory")


def get_llm_provider(mode: Optional[str] = None) -> BaseLLMProvider:
    configured_mode = (mode or settings.LLM_MODE or "mock").lower()

    if configured_mode == "openai":
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY is not set. Falling back to MockLLMProvider.")
            return MockLLMProvider()
        return OpenAIProvider()
    elif configured_mode == "anthropic":
        if not settings.ANTHROPIC_API_KEY:
            logger.warning("ANTHROPIC_API_KEY is not set. Falling back to MockLLMProvider.")
            return MockLLMProvider()
        return AnthropicProvider()
    elif configured_mode == "mock":
        return MockLLMProvider()
    else:
        logger.warning(f"Unknown LLM_MODE '{configured_mode}'. Falling back to MockLLMProvider.")
        return MockLLMProvider()
