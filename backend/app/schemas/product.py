from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = None
    description: str = Field(..., min_length=1)
    price: Optional[str] = None
    features: List[str] = Field(default_factory=list)
    target_benefits: List[str] = Field(default_factory=list)
    usp: Optional[str] = None
    url: Optional[str] = None


class ProductCreate(ProductBase):
    workspace_id: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    features: Optional[List[str]] = None
    target_benefits: Optional[List[str]] = None
    usp: Optional[str] = None
    url: Optional[str] = None


class ProductResponse(ProductBase):
    id: str
    workspace_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
