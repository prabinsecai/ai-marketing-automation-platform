from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.workspace import Workspace
from app.models.product import Product
from app.models.audience import Audience
from app.models.campaign import Campaign, CampaignStatus
from app.models.content import ContentAsset, ContentChannel, ContentStatus
from app.models.ai_log import AILog
from app.schemas.dashboard import DashboardStatsResponse, CampaignStatusCounts, ContentStatusCounts
from app.schemas.campaign import CampaignResponse
from app.schemas.ai_log import AILogResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    workspace_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    # Find active workspace
    workspace = None
    if workspace_id:
        workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        workspace = db.query(Workspace).order_by(Workspace.created_at.desc()).first()

    if not workspace:
        # Return empty shell
        return DashboardStatsResponse(
            workspace_name="Default Workspace",
            workspace_id="none",
            total_campaigns=0,
            campaign_status_counts=CampaignStatusCounts(),
            total_products=0,
            total_audiences=0,
            content_status_counts=ContentStatusCounts(),
            recent_campaigns=[],
            recent_ai_activity=[],
        )

    # 1. Campaign counts
    campaigns = db.query(Campaign).filter(Campaign.workspace_id == workspace.id).all()
    total_campaigns = len(campaigns)

    camp_counts = CampaignStatusCounts(
        draft=sum(1 for c in campaigns if c.status == CampaignStatus.DRAFT),
        strategy_generated=sum(1 for c in campaigns if c.status == CampaignStatus.STRATEGY_GENERATED),
        content_generated=sum(1 for c in campaigns if c.status == CampaignStatus.CONTENT_GENERATED),
        in_review=sum(1 for c in campaigns if c.status == CampaignStatus.IN_REVIEW),
        approved=sum(1 for c in campaigns if c.status == CampaignStatus.APPROVED),
        total=total_campaigns,
    )

    # 2. Product & Audience counts
    total_products = db.query(Product).filter(Product.workspace_id == workspace.id).count()
    total_audiences = db.query(Audience).filter(Audience.workspace_id == workspace.id).count()

    # 3. Content status counts
    content_assets = (
        db.query(ContentAsset)
        .join(Campaign)
        .filter(Campaign.workspace_id == workspace.id)
        .all()
    )
    content_counts = ContentStatusCounts(
        draft=sum(1 for a in content_assets if a.status == ContentStatus.DRAFT),
        in_review=sum(1 for a in content_assets if a.status == ContentStatus.IN_REVIEW),
        approved=sum(1 for a in content_assets if a.status == ContentStatus.APPROVED),
        rejected=sum(1 for a in content_assets if a.status == ContentStatus.REJECTED),
        total=len(content_assets),
        email=sum(1 for a in content_assets if a.channel == ContentChannel.EMAIL),
        social=sum(1 for a in content_assets if a.channel == ContentChannel.SOCIAL),
        advertisement=sum(1 for a in content_assets if a.channel == ContentChannel.ADVERTISEMENT),
    )

    # 4. Recent campaigns
    recent_campaigns_db = (
        db.query(Campaign)
        .filter(Campaign.workspace_id == workspace.id)
        .order_by(Campaign.created_at.desc())
        .limit(5)
        .all()
    )
    recent_campaigns = [CampaignResponse.model_validate(c) for c in recent_campaigns_db]

    # 5. Recent AI activity
    recent_ai_db = (
        db.query(AILog)
        .filter(AILog.workspace_id == workspace.id)
        .order_by(AILog.created_at.desc())
        .limit(6)
        .all()
    )
    recent_ai_activity = [AILogResponse.model_validate(log) for log in recent_ai_db]

    return DashboardStatsResponse(
        workspace_name=workspace.name,
        workspace_id=workspace.id,
        total_campaigns=total_campaigns,
        campaign_status_counts=camp_counts,
        total_products=total_products,
        total_audiences=total_audiences,
        content_status_counts=content_counts,
        recent_campaigns=recent_campaigns,
        recent_ai_activity=recent_ai_activity,
    )
