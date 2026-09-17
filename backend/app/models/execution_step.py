import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class StepStatus:
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

    ALL = [RUNNING, SUCCESS, FAILED, SKIPPED]


class ExecutionStep(Base):
    __tablename__ = "execution_steps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id = Column(String(36), ForeignKey("campaign_executions.id", ondelete="CASCADE"), nullable=False, index=True)

    step_name = Column(String(100), nullable=False)  # validate_approval, plan_execution, dispatch_n8n_webhook, evaluate_result, handle_retry, escalate
    step_type = Column(String(50), nullable=False)  # agent_node, tool_call, webhook_dispatch, escalation
    status = Column(String(50), default=StepStatus.RUNNING, nullable=False)

    input_data = Column(JSON, default=dict, nullable=False)
    output_data = Column(JSON, default=dict, nullable=False)
    error_message = Column(Text, nullable=True)

    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    execution = relationship("CampaignExecution", back_populates="steps")
