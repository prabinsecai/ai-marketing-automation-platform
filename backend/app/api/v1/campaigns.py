from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.campaign import Campaign, CampaignStatus
from app.models.workspace import Workspace
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignStatusUpdate,
    CampaignResponse,
    CampaignDetailResponse,
)

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.get("", response_model=List[CampaignResponse])
def list_campaigns(
    workspace_id: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    query = db.query(Campaign)
    if workspace_id:
        query = query.filter(Campaign.workspace_id == workspace_id)
    if status_filter:
        query = query.filter(Campaign.status == status_filter)
    return query.order_by(Campaign.created_at.desc()).all()


@router.post("", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == payload.workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    campaign = Campaign(**payload.model_dump(), status=CampaignStatus.DRAFT)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("/{id}", response_model=CampaignDetailResponse)
def get_campaign_detail(id: str, db: Session = Depends(get_db)):
    campaign = (
        db.query(Campaign)
        .options(
            joinedload(Campaign.product),
            joinedload(Campaign.audience),
            joinedload(Campaign.strategy),
            joinedload(Campaign.content_assets),
        )
        .filter(Campaign.id == id)
        .first()
    )
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign


@router.put("/{id}", response_model=CampaignResponse)
def update_campaign(id: str, payload: CampaignUpdate, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in CampaignStatus.ALL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{update_data['status']}'. Must be one of {CampaignStatus.ALL}"
        )

    for key, value in update_data.items():
        setattr(campaign, key, value)

    db.commit()
    db.refresh(campaign)
    return campaign


@router.patch("/{id}/status", response_model=CampaignResponse)
def update_campaign_status(id: str, payload: CampaignStatusUpdate, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    if payload.status not in CampaignStatus.ALL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{payload.status}'. Must be one of {CampaignStatus.ALL}"
        )

    campaign.status = payload.status
    db.commit()
    db.refresh(campaign)
    return campaign


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    db.delete(campaign)
    db.commit()
    return None
