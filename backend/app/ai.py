from typing import Any
from .config import get_settings

class AIProvider:
    async def generate_strategy(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
    async def generate_content(self, channel: str, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

class MockProvider(AIProvider):
    async def generate_strategy(self, context):
        return {"positioning": "Outcome-focused growth", "channels": ["email", "social"], "audience": context.get("audience", "target customers")}
    async def generate_content(self, channel, context):
        return {"channel": channel, "headline": "Make your next campaign perform better", "body": "Discover a clearer path to growth with our solution.", "status": "draft"}

def get_provider() -> AIProvider:
    settings = get_settings()
    if settings.llm_mode == "mock":
        return MockProvider()
    if settings.llm_mode not in {"openai", "anthropic"}:
        raise ValueError("LLM_MODE must be mock, openai, or anthropic")
    # Keep network clients optional and lazy; production deployments can extend this adapter.
    return MockProvider()
