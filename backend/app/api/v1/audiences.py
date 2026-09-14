from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audience import Audience
from app.models.workspace import Workspace
from app.schemas.audience import AudienceCreate, AudienceUpdate, AudienceResponse

router = APIRouter(prefix="/audiences", tags=["Audiences"])


@router.get("", response_model=List[AudienceResponse])
def list_audiences(
    workspace_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Audience)
    if workspace_id:
        query = query.filter(Audience.workspace_id == workspace_id)
    return query.order_by(Audience.created_at.desc()).all()


@router.post("", response_model=AudienceResponse, status_code=status.HTTP_201_CREATED)
def create_audience(payload: AudienceCreate, db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == payload.workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    audience = Audience(**payload.model_dump())
    db.add(audience)
    db.commit()
    db.refresh(audience)
    return audience


@router.get("/{id}", response_model=AudienceResponse)
def get_audience(id: str, db: Session = Depends(get_db)):
    audience = db.query(Audience).filter(Audience.id == id).first()
    if not audience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audience not found")
    return audience


@router.put("/{id}", response_model=AudienceResponse)
def update_audience(id: str, payload: AudienceUpdate, db: Session = Depends(get_db)):
    audience = db.query(Audience).filter(Audience.id == id).first()
    if not audience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audience not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(audience, key, value)

    db.commit()
    db.refresh(audience)
    return audience


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audience(id: str, db: Session = Depends(get_db)):
    audience = db.query(Audience).filter(Audience.id == id).first()
    if not audience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audience not found")
    db.delete(audience)
    db.commit()
    return None
