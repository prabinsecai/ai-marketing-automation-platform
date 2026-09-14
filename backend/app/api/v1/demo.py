from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.seed.demo_data import seed_demo_data
from app.schemas.workspace import WorkspaceResponse

router = APIRouter(prefix="/demo", tags=["Demo"])


@router.post("/seed", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def seed_demo_endpoint(db: Session = Depends(get_db)):
    workspace = seed_demo_data(db)
    return workspace
