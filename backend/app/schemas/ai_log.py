from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AILogResponse(BaseModel):
    id: str
    workspace_id: str
    campaign_id: Optional[str] = None
    agent_name: str
    provider: str
    model: str
    prompt_template: Optional[str] = None
    prompt_preview: Optional[str] = None
    response_preview: Optional[str] = None
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_ms: int
    status: str
    error_message: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
