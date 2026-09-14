import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CampaignStrategy(Base):
    __tablename__ = "campaign_strategies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    summary = Column(Text, nullable=False)
    audience_reasoning = Column(Text, nullable=False)
    positioning = Column(Text, nullable=False)
    key_message = Column(Text, nullable=False)

    # Structured recommendations
    channel_strategy = Column(JSON, default=list, nullable=False)  # List of {channel, priority, rationale, tactics}
    campaign_themes = Column(JSON, default=list, nullable=False)  # List of {theme, hook, description}
    content_recommendations = Column(JSON, default=list, nullable=False)  # List of {channel, asset_type, objective, best_practices}

    cta_strategy = Column(Text, nullable=False)
    timeline_suggestion = Column(Text, nullable=False)
    future_success_metrics = Column(JSON, default=list, nullable=False)  # List of {metric, rationale, target_benchmark}
    risks_assumptions = Column(JSON, default=list, nullable=False)  # List of {risk, mitigation}

    raw_prompt = Column(Text, nullable=True)
    raw_response = Column(Text, nullable=True)
    model_used = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    campaign = relationship("Campaign", back_populates="strategy")
