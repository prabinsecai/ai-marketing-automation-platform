import json
import time
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
import openai
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.ai.base import BaseLLMProvider, LLMResult, TokenUsage
from app.config import settings

T = TypeVar("T", bound=BaseModel)


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self._model = model or settings.OPENAI_MODEL or "gpt-4o-mini"
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def default_model(self) -> str:
        return self._model

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((openai.RateLimitError, openai.APIConnectionError, openai.APITimeoutError)),
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
            raise ValueError("OpenAI API key is missing. Set OPENAI_API_KEY in .env or switch to LLM_MODE=mock.")

        selected_model = model or self.default_model
        start_time = time.time()

        # Request structured response via OpenAI response_format / JSON schema
        response = await self.client.beta.chat.completions.parse(
            model=selected_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=response_schema,
            temperature=temperature,
            timeout=settings.AI_TIMEOUT_SECONDS,
        )

        latency_ms = int((time.time() - start_time) * 1000)
        parsed_result = response.choices[0].message.parsed
        raw_content = response.choices[0].message.content or json.dumps(parsed_result.model_dump())

        prompt_tokens = response.usage.prompt_tokens if response.usage else 0
        completion_tokens = response.usage.completion_tokens if response.usage else 0
        total_tokens = response.usage.total_tokens if response.usage else (prompt_tokens + completion_tokens)

        return LLMResult(
            parsed=parsed_result,
            raw_response=raw_content,
            model=selected_model,
            provider=self.provider_name,
            latency_ms=latency_ms,
            usage=TokenUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
            ),
        )
