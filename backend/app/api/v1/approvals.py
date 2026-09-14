from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.approval import Approval
from app.schemas.approval import ApprovalResponse

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.get("", response_model=List[ApprovalResponse])
def list_approvals(
    workspace_id: Optional[str] = Query(None),
    campaign_id: Optional[str] = Query(None),
    content_asset_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Approval)
    if workspace_id:
        query = query.filter(Approval.workspace_id == workspace_id)
    if campaign_id:
        query = query.filter(Approval.campaign_id == campaign_id)
    if content_asset_id:
        query = query.filter(Approval.content_asset_id == content_asset_id)
    return query.order_by(Approval.created_at.desc()).all()
