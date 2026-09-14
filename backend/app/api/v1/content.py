from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.campaign import Campaign, CampaignStatus
from app.models.content import ContentAsset, ContentChannel, ContentStatus
from app.models.approval import Approval, ApprovalAction
from app.schemas.content import (
    ContentAssetResponse,
    ContentAssetUpdate,
    ContentRegenerateRequest,
)
from app.schemas.approval import ApprovalCreate, ApprovalResponse
from app.ai.agents.content_agent import ContentAgent

router = APIRouter(tags=["AI Content"])


# 1. Campaign-scoped content endpoints
@router.get("/campaigns/{campaign_id}/content", response_model=List[ContentAssetResponse])
def list_campaign_content(
    campaign_id: str,
    channel: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    query = db.query(ContentAsset).filter(ContentAsset.campaign_id == campaign_id)
    if channel:
        query = query.filter(ContentAsset.channel == channel)
    if status_filter:
        query = query.filter(ContentAsset.status == status_filter)
    return query.order_by(ContentAsset.channel, ContentAsset.variation_number).all()


@router.post("/campaigns/{campaign_id}/content/generate", response_model=List[ContentAssetResponse])
async def generate_campaign_content(campaign_id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    workspace = campaign.workspace
    agent = ContentAgent()

    try:
        result = await agent.generate_batch_content(
            db=db,
            campaign=campaign,
            workspace=workspace,
            strategy=campaign.strategy,
            product=campaign.product,
            audience=campaign.audience,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate content: {str(e)}"
        )

    data = result.parsed
    new_assets: List[ContentAsset] = []

    # Process Email Variations
    for idx, email_var in enumerate(data.email_variations, start=1):
        asset = ContentAsset(
            campaign_id=campaign.id,
            channel=ContentChannel.EMAIL,
            variation_number=email_var.variation_number or idx,
            title=email_var.subject,
            preview_text=email_var.preview_text,
            body=email_var.body,
            cta=email_var.cta,
            status=ContentStatus.DRAFT,
            is_selected=(idx == 1),
            raw_response=result.raw_response,
            model_used=result.model,
        )
        db.add(asset)
        new_assets.append(asset)

    # Process Social Variations
    for idx, social_var in enumerate(data.social_variations, start=1):
        asset = ContentAsset(
            campaign_id=campaign.id,
            channel=ContentChannel.SOCIAL,
            variation_number=social_var.variation_number or idx,
            platform=social_var.platform,
            hook=social_var.hook,
            body=social_var.caption,
            cta=social_var.cta,
            hashtags=social_var.hashtags,
            status=ContentStatus.DRAFT,
            is_selected=(idx == 1),
            raw_response=result.raw_response,
            model_used=result.model,
        )
        db.add(asset)
        new_assets.append(asset)

    # Process Ad Variations
    for idx, ad_var in enumerate(data.ad_variations, start=1):
        asset = ContentAsset(
            campaign_id=campaign.id,
            channel=ContentChannel.ADVERTISEMENT,
            variation_number=ad_var.variation_number or idx,
            platform=ad_var.platform,
            title=ad_var.headline,
            body=ad_var.primary_text,
            cta=ad_var.cta,
            status=ContentStatus.DRAFT,
            is_selected=(idx == 1),
            raw_response=result.raw_response,
            model_used=result.model,
        )
        db.add(asset)
        new_assets.append(asset)

    # Advance campaign status
    if campaign.status in [CampaignStatus.DRAFT, CampaignStatus.STRATEGY_GENERATED]:
        campaign.status = CampaignStatus.CONTENT_GENERATED

    db.commit()
    for a in new_assets:
        db.refresh(a)

    return new_assets


# 2. Global content assets library endpoints
@router.get("/content-assets", response_model=List[ContentAssetResponse])
def list_all_content_assets(
    workspace_id: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    query = db.query(ContentAsset).join(Campaign)
    if workspace_id:
        query = query.filter(Campaign.workspace_id == workspace_id)
    if channel:
        query = query.filter(ContentAsset.channel == channel)
    if status_filter:
        query = query.filter(ContentAsset.status == status_filter)
    return query.order_by(ContentAsset.created_at.desc()).all()


@router.get("/content-assets/{id}", response_model=ContentAssetResponse)
def get_content_asset(id: str, db: Session = Depends(get_db)):
    asset = db.query(ContentAsset).filter(ContentAsset.id == id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content asset not found")
    return asset


@router.patch("/content-assets/{id}", response_model=ContentAssetResponse)
def edit_content_asset(id: str, payload: ContentAssetUpdate, db: Session = Depends(get_db)):
    asset = db.query(ContentAsset).filter(ContentAsset.id == id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content asset not found")

    update_data = payload.model_dump(exclude_unset=True)
    edit_summary = update_data.pop("edit_summary", None)

    # Record edit history if content changed
    if any(k in update_data for k in ["body", "title", "preview_text", "hook", "cta"]):
        history_entry = {
            "edited_at": datetime.now(timezone.utc).isoformat(),
            "previous_title": asset.title,
            "previous_body": asset.body,
            "previous_cta": asset.cta,
            "summary": edit_summary or "Manual content edit",
        }
        current_history = list(asset.edit_history or [])
        current_history.append(history_entry)
        asset.edit_history = current_history

    for key, value in update_data.items():
        setattr(asset, key, value)

    db.commit()
    db.refresh(asset)
    return asset


@router.post("/content-assets/{id}/select", response_model=ContentAssetResponse)
def toggle_content_selection(id: str, db: Session = Depends(get_db)):
    asset = db.query(ContentAsset).filter(ContentAsset.id == id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content asset not found")

    asset.is_selected = not asset.is_selected
    db.commit()
    db.refresh(asset)
    return asset


@router.post("/content-assets/{id}/regenerate", response_model=ContentAssetResponse)
async def regenerate_content_variation(
    id: str,
    payload: ContentRegenerateRequest,
    db: Session = Depends(get_db),
):
    asset = db.query(ContentAsset).filter(ContentAsset.id == id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content asset not found")

    campaign = asset.campaign
    workspace = campaign.workspace
    agent = ContentAgent()

    try:
        result = await agent.regenerate_variation(
            db=db,
            asset=asset,
            campaign=campaign,
            workspace=workspace,
            instructions=payload.instructions,
            product=campaign.product,
            audience=campaign.audience,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to regenerate variation: {str(e)}"
        )

    # Record history
    history_entry = {
        "edited_at": datetime.now(timezone.utc).isoformat(),
        "previous_title": asset.title,
        "previous_body": asset.body,
        "previous_cta": asset.cta,
        "summary": f"AI Regeneration ({payload.instructions or 'No prompt instructions'})",
    }
    current_history = list(asset.edit_history or [])
    current_history.append(history_entry)
    asset.edit_history = current_history

    data = result.parsed
    if asset.channel == ContentChannel.EMAIL:
        asset.title = data.subject
        asset.preview_text = data.preview_text
        asset.body = data.body
        asset.cta = data.cta
    elif asset.channel == ContentChannel.SOCIAL:
        asset.platform = data.platform
        asset.hook = data.hook
        asset.body = data.caption
        asset.cta = data.cta
        asset.hashtags = data.hashtags
    elif asset.channel == ContentChannel.ADVERTISEMENT:
        asset.title = data.headline
        asset.body = data.primary_text
        asset.cta = data.cta

    asset.raw_response = result.raw_response
    asset.model_used = result.model
    # If it was rejected or approved, reset back to DRAFT for review
    asset.status = ContentStatus.DRAFT

    db.commit()
    db.refresh(asset)
    return asset


@router.post("/content-assets/{id}/approve", response_model=ApprovalResponse)
def submit_content_approval(
    id: str,
    payload: ApprovalCreate,
    db: Session = Depends(get_db),
):
    asset = db.query(ContentAsset).filter(ContentAsset.id == id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content asset not found")

    campaign = asset.campaign
    workspace = campaign.workspace

    if payload.action not in ApprovalAction.ALL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action '{payload.action}'. Must be one of {ApprovalAction.ALL}"
        )

    # Update asset status
    if payload.action == ApprovalAction.APPROVE:
        asset.status = ContentStatus.APPROVED
    elif payload.action == ApprovalAction.REJECT:
        asset.status = ContentStatus.REJECTED
    elif payload.action == ApprovalAction.REQUEST_CHANGES:
        asset.status = ContentStatus.IN_REVIEW

    # Check if all selected assets for campaign are approved, advance campaign status to APPROVED
    selected_assets = db.query(ContentAsset).filter(
        ContentAsset.campaign_id == campaign.id,
        ContentAsset.is_selected == True,
    ).all()
    if selected_assets and all(a.status == ContentStatus.APPROVED for a in selected_assets):
        campaign.status = CampaignStatus.APPROVED
    elif campaign.status == CampaignStatus.CONTENT_GENERATED and payload.action in [ApprovalAction.REQUEST_CHANGES, ApprovalAction.APPROVE]:
        campaign.status = CampaignStatus.IN_REVIEW

    approval = Approval(
        workspace_id=workspace.id,
        campaign_id=campaign.id,
        content_asset_id=asset.id,
        user_id=payload.user_id,
        action=payload.action,
        feedback=payload.feedback,
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval
