from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ExecutionStepResponse(BaseModel):
    id: str
    execution_id: str
    step_name: str
    step_type: str
    status: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExecutionCreateRequest(BaseModel):
    idempotency_key: Optional[str] = None
    trigger_source: str = "manual_ui"
    channels: Optional[List[str]] = None


class CampaignExecutionResponse(BaseModel):
    id: str
    campaign_id: str
    workspace_id: str
    status: str
    idempotency_key: str
    retry_count: int
    max_retries: int
    n8n_execution_id: Optional[str] = None
    n8n_workflow_id: Optional[str] = None
    error_message: Optional[str] = None
    agent_trace: List[Dict[str, Any]] = Field(default_factory=list)
    trigger_source: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    steps: List[ExecutionStepResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class N8NWebhookResultPayload(BaseModel):
    execution_id: str
    n8n_execution_id: Optional[str] = None
    workflow_id: Optional[str] = None
    status: str = Field(..., description="SUCCESS or FAILED")
    data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    error: Optional[str] = None
