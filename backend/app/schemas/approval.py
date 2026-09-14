from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ApprovalCreate(BaseModel):
    action: str = Field(..., description="APPROVE, REJECT, REQUEST_CHANGES")
    feedback: Optional[str] = None
    user_id: Optional[str] = None


class ApprovalResponse(BaseModel):
    id: str
    workspace_id: str
    campaign_id: str
    content_asset_id: Optional[str] = None
    user_id: Optional[str] = None
    action: str
    feedback: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
