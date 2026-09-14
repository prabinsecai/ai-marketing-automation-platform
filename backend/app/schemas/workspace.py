from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class WorkspaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    brand_guidelines: Optional[str] = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    brand_guidelines: Optional[str] = None


class WorkspaceResponse(WorkspaceBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
