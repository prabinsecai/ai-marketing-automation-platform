from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


@router.get("", response_model=List[WorkspaceResponse])
def list_workspaces(db: Session = Depends(get_db)):
    return db.query(Workspace).order_by(Workspace.created_at.desc()).all()


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def create_workspace(payload: WorkspaceCreate, db: Session = Depends(get_db)):
    existing = db.query(Workspace).filter(Workspace.slug == payload.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Workspace with slug '{payload.slug}' already exists."
        )
    workspace = Workspace(**payload.model_dump())
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


@router.get("/{id}", response_model=WorkspaceResponse)
def get_workspace(id: str, db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    return workspace


@router.put("/{id}", response_model=WorkspaceResponse)
def update_workspace(id: str, payload: WorkspaceUpdate, db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(workspace, key, value)

    db.commit()
    db.refresh(workspace)
    return workspace


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workspace(id: str, db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    db.delete(workspace)
    db.commit()
    return None
