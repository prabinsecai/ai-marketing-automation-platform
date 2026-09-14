from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ChannelStrategyItem(BaseModel):
    channel: str = Field(..., description="e.g. Email, LinkedIn, Twitter/X, Google Search Ads, Meta Ads")
    priority: str = Field(..., description="Primary, Secondary, Supporting")
    rationale: str = Field(..., description="Why this channel suits the target audience")
    tactics: List[str] = Field(default_factory=list, description="Tactical execution approaches")


class CampaignThemeItem(BaseModel):
    theme: str = Field(..., description="Name of the strategic angle or theme")
    hook: str = Field(..., description="Engaging hook or angle")
    description: str = Field(..., description="How this theme addresses audience pain points")


class ContentRecommendationItem(BaseModel):
    channel: str = Field(..., description="Channel name")
    asset_type: str = Field(..., description="e.g. Nurture Sequence, Thought Leadership Post, Value-Prop Ad")
    objective: str = Field(..., description="Asset specific objective")
    best_practices: List[str] = Field(default_factory=list)


class MetricItem(BaseModel):
    metric: str = Field(..., description="e.g. Conversion Rate, Demo Bookings, Engagement Rate, CAC")
    rationale: str = Field(..., description="Why this metric matters for this campaign")
    target_benchmark: str = Field(..., description="Suggested target or range")


class RiskAssumptionItem(BaseModel):
    risk: str = Field(..., description="Identified risk or key assumption")
    mitigation: str = Field(..., description="Recommended mitigation strategy")


# AI Structured Output Schema for Marketing Strategist
class AIStrategyOutput(BaseModel):
    summary: str = Field(..., description="Executive summary of the marketing campaign strategy")
    audience_reasoning: str = Field(..., description="Deep analysis of why the target audience will convert")
    positioning: str = Field(..., description="Market positioning statement and differentiation")
    key_message: str = Field(..., description="Core memorable narrative or value proposition")
    channel_strategy: List[ChannelStrategyItem] = Field(..., description="Channel breakdown with rationale")
    campaign_themes: List[CampaignThemeItem] = Field(..., description="Campaign core thematic angles")
    content_recommendations: List[ContentRecommendationItem] = Field(..., description="Specific recommended content pieces")
    cta_strategy: str = Field(..., description="Call-to-action ladder and conversion strategy")
    timeline_suggestion: str = Field(..., description="Phase-by-phase rollout timeline suggestion")
    future_success_metrics: List[MetricItem] = Field(..., description="Target KPIs and benchmarks")
    risks_assumptions: List[RiskAssumptionItem] = Field(..., description="Risks and assumptions")


class StrategyResponse(BaseModel):
    id: str
    campaign_id: str
    summary: str
    audience_reasoning: str
    positioning: str
    key_message: str
    channel_strategy: List[Dict[str, Any]]
    campaign_themes: List[Dict[str, Any]]
    content_recommendations: List[Dict[str, Any]]
    cta_strategy: str
    timeline_suggestion: str
    future_success_metrics: List[Dict[str, Any]]
    risks_assumptions: List[Dict[str, Any]]
    model_used: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
