from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.strategy import StrategyResponse
from app.schemas.content import ContentAssetResponse
from app.schemas.product import ProductResponse
from app.schemas.audience import AudienceResponse


class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    objective: str = Field(..., min_length=1, max_length=255)
    budget: Optional[str] = None
    target_timeline: Optional[str] = None
    product_id: Optional[str] = None
    audience_id: Optional[str] = None


class CampaignCreate(CampaignBase):
    workspace_id: str


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    objective: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[str] = None
    target_timeline: Optional[str] = None
    product_id: Optional[str] = None
    audience_id: Optional[str] = None


class CampaignStatusUpdate(BaseModel):
    status: str = Field(..., description="DRAFT, STRATEGY_GENERATED, CONTENT_GENERATED, IN_REVIEW, APPROVED")


class CampaignResponse(CampaignBase):
    id: str
    workspace_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignDetailResponse(CampaignResponse):
    product: Optional[ProductResponse] = None
    audience: Optional[AudienceResponse] = None
    strategy: Optional[StrategyResponse] = None
    content_assets: List[ContentAssetResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
