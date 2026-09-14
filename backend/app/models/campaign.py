import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base


class CampaignStatus:
    DRAFT = "DRAFT"
    STRATEGY_GENERATED = "STRATEGY_GENERATED"
    CONTENT_GENERATED = "CONTENT_GENERATED"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"

    ALL = [DRAFT, STRATEGY_GENERATED, CONTENT_GENERATED, IN_REVIEW, APPROVED]


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True)
    audience_id = Column(String(36), ForeignKey("audiences.id", ondelete="SET NULL"), nullable=True, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    objective = Column(String(255), nullable=False)  # e.g., Lead Generation, Brand Awareness, Product Launch, Customer Retention
    status = Column(String(50), default=CampaignStatus.DRAFT, nullable=False, index=True)
    budget = Column(String(100), nullable=True)
    target_timeline = Column(String(255), nullable=True)  # e.g., "Q3 2026, 4-week ramp"

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    workspace = relationship("Workspace", back_populates="campaigns")
    product = relationship("Product", back_populates="campaigns")
    audience = relationship("Audience", back_populates="campaigns")

    strategy = relationship("CampaignStrategy", back_populates="campaign", uselist=False, cascade="all, delete-orphan")
    content_assets = relationship("ContentAsset", back_populates="campaign", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="campaign", cascade="all, delete-orphan")
