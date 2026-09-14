import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
    price = Column(String(100), nullable=True)  # Formatted or numeric representation
    features = Column(JSON, default=list, nullable=False)  # List[str]
    target_benefits = Column(JSON, default=list, nullable=False)  # List[str]
    usp = Column(Text, nullable=True)  # Unique Selling Proposition
    url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    workspace = relationship("Workspace", back_populates="products")
    campaigns = relationship("Campaign", back_populates="product")
