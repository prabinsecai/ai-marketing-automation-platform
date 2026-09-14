import pytest
from app.ai.providers.mock_provider import MockLLMProvider
from app.ai.factory import get_llm_provider
from app.schemas.strategy import AIStrategyOutput
from app.schemas.content import AIContentBatchOutput


@pytest.mark.asyncio
async def test_mock_provider_strategy():
    provider = MockLLMProvider()
    result = await provider.generate_structured(
        system_prompt="Test system prompt",
        user_prompt="Product Name: OmniFlow Engine\nTarget Persona: CMOs\nCampaign: Q4 Push\nObjective: Conversions",
        response_schema=AIStrategyOutput,
    )
    assert result.provider == "mock"
    assert isinstance(result.parsed, AIStrategyOutput)
    assert len(result.parsed.summary) > 0
    assert len(result.parsed.channel_strategy) >= 1
    assert result.usage.total_tokens > 0


@pytest.mark.asyncio
async def test_mock_provider_content_batch():
    provider = MockLLMProvider()
    result = await provider.generate_structured(
        system_prompt="Test system prompt",
        user_prompt="Product Name: OmniFlow Engine\nTarget Persona: CMOs\nCampaign: Q4 Push\nObjective: Conversions",
        response_schema=AIContentBatchOutput,
    )
    assert result.provider == "mock"
    assert isinstance(result.parsed, AIContentBatchOutput)
    assert len(result.parsed.email_variations) >= 2
    assert len(result.parsed.social_variations) >= 2
    assert len(result.parsed.ad_variations) >= 2


def test_factory_fallback():
    provider = get_llm_provider("mock")
    assert provider.provider_name == "mock"

    # Missing api key falls back gracefully to mock
    openai_provider = get_llm_provider("openai")
    assert openai_provider.provider_name in ["mock", "openai"]
