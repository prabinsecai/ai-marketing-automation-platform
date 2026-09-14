import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class AILog(Base):
    __tablename__ = "ai_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    campaign_id = Column(String(36), ForeignKey("campaigns.id", ondelete="SET NULL"), nullable=True, index=True)

    agent_name = Column(String(100), nullable=False)  # "MarketingStrategist", "ContentAgent", etc.
    provider = Column(String(50), nullable=False)  # "mock", "openai", "anthropic"
    model = Column(String(100), nullable=False)

    prompt_template = Column(String(100), nullable=True)
    prompt_preview = Column(Text, nullable=True)
    response_preview = Column(Text, nullable=True)

    prompt_tokens = Column(Integer, default=0, nullable=False)
    completion_tokens = Column(Integer, default=0, nullable=False)
    total_tokens = Column(Integer, default=0, nullable=False)
    latency_ms = Column(Integer, default=0, nullable=False)

    status = Column(String(50), default="SUCCESS", nullable=False)  # "SUCCESS", "FAILED"
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    workspace = relationship("Workspace", back_populates="ai_logs")
