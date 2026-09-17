import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class CampaignMetric(Base):
    __tablename__ = "campaign_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    channel = Column(String(50), nullable=False) # e.g., 'EMAIL', 'SOCIAL', 'ADVERTISEMENT'
    date = Column(Date, nullable=False, default=date.today)
    
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    spend = Column(Float, default=0.0)
    leads = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    campaign = relationship("Campaign", backref="metrics")


class CampaignEvent(Base):
    __tablename__ = "campaign_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False) # e.g., 'email_open', 'link_click', 'form_submit'
    metadata_payload = Column(JSON, default=dict)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    campaign = relationship("Campaign", backref="events")


class OptimizationRecommendation(Base):
    __tablename__ = "optimization_recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    
    type = Column(String(50), nullable=False) # e.g., 'BUDGET_SHIFT', 'AUDIENCE_TWEAK', 'CONTENT_REVISION', 'PAUSE_CHANNEL'
    description = Column(String, nullable=False)
    evidence = Column(JSON, default=dict)
    
    # PENDING, ACCEPTED, REJECTED, APPLIED
    status = Column(String(20), nullable=False, default="PENDING")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    applied_at = Column(DateTime, nullable=True)

    campaign = relationship("Campaign", backref="recommendations")
