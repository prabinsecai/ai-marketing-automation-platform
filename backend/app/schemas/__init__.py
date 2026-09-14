from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.audience import AudienceCreate, AudienceUpdate, AudienceResponse
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignStatusUpdate,
    CampaignResponse,
    CampaignDetailResponse,
)
from app.schemas.strategy import (
    AIStrategyOutput,
    StrategyResponse,
    ChannelStrategyItem,
    CampaignThemeItem,
    ContentRecommendationItem,
    MetricItem,
    RiskAssumptionItem,
)
from app.schemas.content import (
    AIEmailContentVariation,
    AISocialContentVariation,
    AIAdContentVariation,
    AIContentBatchOutput,
    AIRegenerateEmailOutput,
    AIRegenerateSocialOutput,
    AIRegenerateAdOutput,
    ContentAssetUpdate,
    ContentRegenerateRequest,
    ContentAssetResponse,
)
from app.schemas.approval import ApprovalCreate, ApprovalResponse
from app.schemas.ai_log import AILogResponse
from app.schemas.dashboard import DashboardStatsResponse, CampaignStatusCounts, ContentStatusCounts

__all__ = [
    "WorkspaceCreate",
    "WorkspaceUpdate",
    "WorkspaceResponse",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "AudienceCreate",
    "AudienceUpdate",
    "AudienceResponse",
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignStatusUpdate",
    "CampaignResponse",
    "CampaignDetailResponse",
    "AIStrategyOutput",
    "StrategyResponse",
    "ChannelStrategyItem",
    "CampaignThemeItem",
    "ContentRecommendationItem",
    "MetricItem",
    "RiskAssumptionItem",
    "AIEmailContentVariation",
    "AISocialContentVariation",
    "AIAdContentVariation",
    "AIContentBatchOutput",
    "AIRegenerateEmailOutput",
    "AIRegenerateSocialOutput",
    "AIRegenerateAdOutput",
    "ContentAssetUpdate",
    "ContentRegenerateRequest",
    "ContentAssetResponse",
    "ApprovalCreate",
    "ApprovalResponse",
    "AILogResponse",
    "DashboardStatsResponse",
    "CampaignStatusCounts",
    "ContentStatusCounts",
]
