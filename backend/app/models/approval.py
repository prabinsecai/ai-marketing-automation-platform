import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ApprovalAction:
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_CHANGES = "REQUEST_CHANGES"

    ALL = [APPROVE, REJECT, REQUEST_CHANGES]


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    campaign_id = Column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    content_asset_id = Column(String(36), ForeignKey("content_assets.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    action = Column(String(50), nullable=False)  # APPROVE, REJECT, REQUEST_CHANGES
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    workspace = relationship("Workspace", back_populates="approvals")
    campaign = relationship("Campaign", back_populates="approvals")
    content_asset = relationship("ContentAsset", back_populates="approvals")
    user = relationship("User", back_populates="approvals")
