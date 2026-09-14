import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ContentChannel:
    EMAIL = "EMAIL"
    SOCIAL = "SOCIAL"
    ADVERTISEMENT = "ADVERTISEMENT"

    ALL = [EMAIL, SOCIAL, ADVERTISEMENT]


class ContentStatus:
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

    ALL = [DRAFT, IN_REVIEW, APPROVED, REJECTED]


class ContentAsset(Base):
    __tablename__ = "content_assets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)

    channel = Column(String(50), nullable=False, index=True)  # EMAIL, SOCIAL, ADVERTISEMENT
    variation_number = Column(Integer, default=1, nullable=False)

    # Common / Channel specific fields
    title = Column(String(255), nullable=True)  # For email: subject; for ad: headline; for social: title/topic
    preview_text = Column(Text, nullable=True)  # Email preview / preheader
    body = Column(Text, nullable=False)  # Email body / Social caption / Ad primary text
    hook = Column(Text, nullable=True)  # Social hook / Opening hook
    cta = Column(String(255), nullable=True)  # Call To Action
    hashtags = Column(JSON, default=list, nullable=False)  # List[str] for social
    platform = Column(String(50), nullable=True)  # For social: LinkedIn, X/Twitter, Instagram; for ad: Google Ads, Meta Ads

    status = Column(String(50), default=ContentStatus.DRAFT, nullable=False, index=True)
    is_selected = Column(Boolean, default=False, nullable=False)

    edit_history = Column(JSON, default=list, nullable=False)  # List of {edited_at, previous_body, changes_summary, editor}
    raw_prompt = Column(Text, nullable=True)
    raw_response = Column(Text, nullable=True)
    model_used = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    campaign = relationship("Campaign", back_populates="content_assets")
    approvals = relationship("Approval", back_populates="content_asset", cascade="all, delete-orphan")
