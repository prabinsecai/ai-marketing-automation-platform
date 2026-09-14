from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ai_log import AILog
from app.schemas.ai_log import AILogResponse

router = APIRouter(prefix="/ai-logs", tags=["AI Logs"])


@router.get("", response_model=List[AILogResponse])
def list_ai_logs(
    workspace_id: Optional[str] = Query(None),
    campaign_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(AILog)
    if workspace_id:
        query = query.filter(AILog.workspace_id == workspace_id)
    if campaign_id:
        query = query.filter(AILog.campaign_id == campaign_id)
    return query.order_by(AILog.created_at.desc()).limit(limit).all()
