from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMResult(BaseModel):
    parsed: Any
    raw_response: str
    model: str
    provider: str
    latency_ms: int
    usage: TokenUsage


class BaseLLMProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def default_model(self) -> str:
        pass

    @abstractmethod
    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Type[T],
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> LLMResult:
        """
        Generate structured output validated against the provided Pydantic schema.
        """
        pass
