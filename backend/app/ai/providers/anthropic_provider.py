import json
import time
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
import anthropic
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.ai.base import BaseLLMProvider, LLMResult, TokenUsage
from app.config import settings

T = TypeVar("T", bound=BaseModel)


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self._model = model or settings.ANTHROPIC_MODEL or "claude-3-5-haiku-20241022"
        self.client = AsyncAnthropic(api_key=self.api_key) if self.api_key else None

    @property
    def provider_name(self) -> str:
        return "anthropic"

    @property
    def default_model(self) -> str:
        return self._model

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APITimeoutError)),
        reraise=True,
    )
    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Type[T],
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> LLMResult:
        if not self.client:
            raise ValueError("Anthropic API key is missing. Set ANTHROPIC_API_KEY in .env or switch to LLM_MODE=mock.")

        selected_model = model or self.default_model
        start_time = time.time()

        # Generate JSON schema for tool call/structured output
        schema_json = response_schema.model_json_schema()
        tool_name = f"record_{response_schema.__name__.lower()}"

        tools = [
            {
                "name": tool_name,
                "description": f"Output structured marketing data matching {response_schema.__name__}",
                "input_schema": schema_json,
            }
        ]

        response = await self.client.messages.create(
            model=selected_model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            tools=tools,
            tool_choice={"type": "tool", "name": tool_name},
            temperature=temperature,
            timeout=settings.AI_TIMEOUT_SECONDS,
        )

        latency_ms = int((time.time() - start_time) * 1000)

        # Extract tool call
        tool_use_block = None
        for block in response.content:
            if block.type == "tool_use" and block.name == tool_name:
                tool_use_block = block
                break

        if not tool_use_block:
            raise ValueError(f"Anthropic did not return tool call for {tool_name}")

        parsed_data = response_schema.model_validate(tool_use_block.input)
        raw_content = json.dumps(tool_use_block.input, indent=2)

        prompt_tokens = response.usage.input_tokens if hasattr(response, "usage") else 0
        completion_tokens = response.usage.output_tokens if hasattr(response, "usage") else 0

        return LLMResult(
            parsed=parsed_data,
            raw_response=raw_content,
            model=selected_model,
            provider=self.provider_name,
            latency_ms=latency_ms,
            usage=TokenUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            ),
        )
