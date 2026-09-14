import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Audience(Base):
    __tablename__ = "audiences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    demographics = Column(JSON, default=dict, nullable=False)  # dict with role, industry, company_size, location, etc.
    pain_points = Column(JSON, default=list, nullable=False)  # List[str]
    interests = Column(JSON, default=list, nullable=False)  # List[str]
    goals = Column(JSON, default=list, nullable=False)  # List[str]
    preferred_channels = Column(JSON, default=list, nullable=False)  # List[str] e.g. ["EMAIL", "LINKEDIN", "GOOGLE_ADS"]
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    workspace = relationship("Workspace", back_populates="audiences")
    campaigns = relationship("Campaign", back_populates="audience")
