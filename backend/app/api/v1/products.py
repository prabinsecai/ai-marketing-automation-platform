from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.models.workspace import Workspace
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def list_products(
    workspace_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Product)
    if workspace_id:
        query = query.filter(Product.workspace_id == workspace_id)
    return query.order_by(Product.created_at.desc()).all()


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == payload.workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{id}", response_model=ProductResponse)
def get_product(id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.put("/{id}", response_model=ProductResponse)
def update_product(id: str, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product)
    db.commit()
    return None
