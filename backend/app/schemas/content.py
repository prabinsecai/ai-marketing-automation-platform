from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# Individual AI Output Schemas
class AIEmailContentVariation(BaseModel):
    variation_number: int = Field(default=1)
    subject: str = Field(..., description="Compelling email subject line")
    preview_text: str = Field(..., description="Preheader / snippet text (35-90 chars)")
    body: str = Field(..., description="Full email body copy formatted with clear sections")
    cta: str = Field(..., description="Primary action link or button text")


class AISocialContentVariation(BaseModel):
    variation_number: int = Field(default=1)
    platform: str = Field(..., description="LinkedIn, Twitter/X, Instagram, or Threads")
    hook: str = Field(..., description="Attention-grabbing first 1-2 lines")
    caption: str = Field(..., description="Engaging body post copy")
    cta: str = Field(..., description="Action CTA (e.g., 'Comment below', 'Link in bio', 'Read case study')")
    hashtags: List[str] = Field(default_factory=list, description="Relevant hashtags without the # or with #")


class AIAdContentVariation(BaseModel):
    variation_number: int = Field(default=1)
    platform: str = Field(default="Google Ads / Meta Ads", description="Ad network target")
    headline: str = Field(..., description="Punchy ad headline (max 30-40 chars)")
    primary_text: str = Field(..., description="Main ad copy / value prop")
    cta: str = Field(..., description="Button CTA (e.g., 'Sign Up Free', 'Book a Demo', 'Learn More')")


# Batch generation output
class AIContentBatchOutput(BaseModel):
    email_variations: List[AIEmailContentVariation] = Field(default_factory=list)
    social_variations: List[AISocialContentVariation] = Field(default_factory=list)
    ad_variations: List[AIAdContentVariation] = Field(default_factory=list)


# Single variation output for regeneration
class AIRegenerateEmailOutput(BaseModel):
    subject: str
    preview_text: str
    body: str
    cta: str


class AIRegenerateSocialOutput(BaseModel):
    platform: str
    hook: str
    caption: str
    cta: str
    hashtags: List[str]


class AIRegenerateAdOutput(BaseModel):
    headline: str
    primary_text: str
    cta: str


# Database CRUD / API Request & Response Schemas
class ContentAssetUpdate(BaseModel):
    title: Optional[str] = None
    preview_text: Optional[str] = None
    body: Optional[str] = None
    hook: Optional[str] = None
    cta: Optional[str] = None
    hashtags: Optional[List[str]] = None
    platform: Optional[str] = None
    is_selected: Optional[bool] = None
    status: Optional[str] = None
    edit_summary: Optional[str] = Field(None, description="Note explaining what was edited")


class ContentRegenerateRequest(BaseModel):
    instructions: Optional[str] = Field(None, description="Specific feedback or tone adjustment for regeneration")


class ContentAssetResponse(BaseModel):
    id: str
    campaign_id: str
    channel: str
    variation_number: int
    title: Optional[str] = None
    preview_text: Optional[str] = None
    body: str
    hook: Optional[str] = None
    cta: Optional[str] = None
    hashtags: List[str] = Field(default_factory=list)
    platform: Optional[str] = None
    status: str
    is_selected: bool
    edit_history: List[Dict[str, Any]] = Field(default_factory=list)
    model_used: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
