from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class AudienceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    demographics: Dict[str, Any] = Field(default_factory=dict)
    pain_points: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    preferred_channels: List[str] = Field(default_factory=list)


class AudienceCreate(AudienceBase):
    workspace_id: str


class AudienceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    demographics: Optional[Dict[str, Any]] = None
    pain_points: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    goals: Optional[List[str]] = None
    preferred_channels: Optional[List[str]] = None


class AudienceResponse(AudienceBase):
    id: str
    workspace_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
