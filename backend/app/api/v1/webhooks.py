import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.execution import CampaignExecution, ExecutionStatus
from app.models.execution_step import ExecutionStep, StepStatus
from app.schemas.execution import N8NWebhookResultPayload

logger = logging.getLogger("app.api.webhooks")
router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/n8n/result")
def receive_n8n_result_callback(
    payload: N8NWebhookResultPayload,
    x_n8n_webhook_secret: str = Header(None, alias="X-N8N-Webhook-Secret"),
    db: Session = Depends(get_db),
):
    """
    Receives webhook callbacks from local n8n workflows upon execution completion.
    """
    # Validate secret if configured
    if settings.N8N_WEBHOOK_SECRET and x_n8n_webhook_secret != settings.N8N_WEBHOOK_SECRET:
        logger.warning("Unauthorized n8n webhook callback attempted with invalid secret.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook secret")

    execution = db.query(CampaignExecution).filter(CampaignExecution.id == payload.execution_id).first()
    if not execution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution ID not found")

    # Record callback step
    step = ExecutionStep(
        execution_id=execution.id,
        step_name="n8n_callback_received",
        step_type="callback_receipt",
        status=StepStatus.SUCCESS if payload.status == "SUCCESS" else StepStatus.FAILED,
        input_data={"n8n_execution_id": payload.n8n_execution_id, "workflow_id": payload.workflow_id},
        output_data=payload.data or {},
        error_message=payload.error,
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
    )
    db.add(step)

    # Append to agent trace
    trace_entry = {
        "node": "n8n_webhook_callback",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": f"Received n8n asynchronous callback with status: {payload.status}",
        "details": payload.data or {},
    }
    current_trace = list(execution.agent_trace or [])
    current_trace.append(trace_entry)
    execution.agent_trace = current_trace

    if payload.status == "SUCCESS":
        execution.status = ExecutionStatus.SUCCESS
        execution.error_message = None
    else:
        execution.status = ExecutionStatus.FAILED
        execution.error_message = payload.error or "n8n workflow callback reported failure"

    if payload.n8n_execution_id:
        execution.n8n_execution_id = payload.n8n_execution_id

    execution.completed_at = datetime.now(timezone.utc)
    db.commit()

    return {"status": "ACKNOWLEDGED", "execution_id": execution.id, "new_status": execution.status}
