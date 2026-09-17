from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import date, datetime

class CampaignMetricCreate(BaseModel):
    campaign_id: str
    channel: str
    date: date
    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    leads: int = 0
    conversions: int = 0
    revenue: float = 0.0

class CampaignMetricOut(CampaignMetricCreate):
    id: str
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class OptimizationRecommendationOut(BaseModel):
    id: str
    campaign_id: str
    type: str
    description: str
    evidence: Dict[str, Any]
    status: str
    created_at: datetime
    applied_at: Optional[datetime] = None
    class Config:
        orm_mode = True

class CampaignPerformanceOut(BaseModel):
    spend: float
    impressions: int
    clicks: int
    leads: int
    conversions: int
    revenue: float
    ctr: float
    cpc: float
    cpl: float
    cpa: float
    conversion_rate: float
    roas: float
    roi: float
    channels: Dict[str, Dict[str, float]]

class AIAnalyticsInsight(BaseModel):
    category: str
    message: str
    evidence: str

class AIAnalyticsRecommendation(BaseModel):
    type: str
    description: str
    evidence: Dict[str, Any]

class CampaignAnalyticsReport(BaseModel):
    performance: CampaignPerformanceOut
    diagnostics: List[Dict[str, Any]]
    insights: List[AIAnalyticsInsight]
    recommendations: List[AIAnalyticsRecommendation]
