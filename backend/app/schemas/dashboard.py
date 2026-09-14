from typing import List
from pydantic import BaseModel
from app.schemas.campaign import CampaignResponse
from app.schemas.ai_log import AILogResponse


class CampaignStatusCounts(BaseModel):
    draft: int = 0
    strategy_generated: int = 0
    content_generated: int = 0
    in_review: int = 0
    approved: int = 0
    total: int = 0


class ContentStatusCounts(BaseModel):
    draft: int = 0
    in_review: int = 0
    approved: int = 0
    rejected: int = 0
    total: int = 0
    email: int = 0
    social: int = 0
    advertisement: int = 0


class DashboardStatsResponse(BaseModel):
    workspace_name: str
    workspace_id: str
    total_campaigns: int
    campaign_status_counts: CampaignStatusCounts
    total_products: int
    total_audiences: int
    content_status_counts: ContentStatusCounts
    recent_campaigns: List[CampaignResponse]
    recent_ai_activity: List[AILogResponse]
