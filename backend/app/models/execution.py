import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ExecutionStatus:
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    ESCALATED = "ESCALATED"

    ALL = [PENDING, RUNNING, SUCCESS, FAILED, RETRYING, ESCALATED]


class CampaignExecution(Base):
    __tablename__ = "campaign_executions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)

    status = Column(String(50), default=ExecutionStatus.PENDING, nullable=False, index=True)
    idempotency_key = Column(String(100), unique=True, nullable=False, index=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)

    n8n_execution_id = Column(String(100), nullable=True, index=True)
    n8n_workflow_id = Column(String(100), nullable=True)

    error_message = Column(Text, nullable=True)
    agent_trace = Column(JSON, default=list, nullable=False)  # List of LangGraph node execution events
    trigger_source = Column(String(50), default="manual_ui", nullable=False)  # manual_ui, api, retry

    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    campaign = relationship("Campaign", back_populates="executions")
    workspace = relationship("Workspace", back_populates="executions")
    steps = relationship("ExecutionStep", back_populates="execution", cascade="all, delete-orphan", order_by="ExecutionStep.created_at")
