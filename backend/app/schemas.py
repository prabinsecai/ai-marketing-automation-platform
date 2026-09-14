from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    settings: dict[str, Any] = {}
class Workspace(WorkspaceCreate, ORM): pass
class ProductCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    workspace_id: int
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    url: HttpUrl | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict, alias="metadata")
class Product(ProductCreate, ORM): pass
class AudienceCreate(BaseModel):
    workspace_id: int
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    criteria: dict[str, Any] = {}
class Audience(AudienceCreate, ORM): pass
class CampaignCreate(BaseModel):
    workspace_id: int
    name: str = Field(min_length=1, max_length=200)
    objective: str | None = None
class CampaignUpdate(BaseModel):
    name: str | None = None
    objective: str | None = None
    status: str | None = None
    strategy: dict[str, Any] | None = None
    content: dict[str, Any] | None = None
class Campaign(CampaignCreate, ORM):
    status: str
    strategy: dict[str, Any] | None
    content: dict[str, Any] | None
    approval_status: str
class StrategyRequest(BaseModel):
    context: dict[str, Any] = {}
class ContentRequest(BaseModel):
    channel: str = Field(min_length=1)
    instructions: str | None = None
class ApprovalCreate(BaseModel):
    status: str = Field(pattern="^(pending|approved|rejected)$")
    reviewer: str | None = None
    comment: str | None = None
class Approval(ApprovalCreate, ORM):
    campaign_id: int
