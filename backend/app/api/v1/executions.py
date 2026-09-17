import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.campaign import Campaign, CampaignStatus
from app.models.content import ContentStatus
from app.models.execution import CampaignExecution, ExecutionStatus
from app.schemas.execution import (
    ExecutionCreateRequest,
    CampaignExecutionResponse,
)
from app.ai.agents.execution_agent import CampaignExecutionAgent

router = APIRouter(tags=["Campaign Executions"])


@router.get("/executions", response_model=List[CampaignExecutionResponse])
def list_executions(
    workspace_id: Optional[str] = Query(None),
    campaign_id: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    query = db.query(CampaignExecution).options(joinedload(CampaignExecution.steps))
    if workspace_id:
        query = query.filter(CampaignExecution.workspace_id == workspace_id)
    if campaign_id:
        query = query.filter(CampaignExecution.campaign_id == campaign_id)
    if status_filter:
        query = query.filter(CampaignExecution.status == status_filter)
    return query.order_by(CampaignExecution.created_at.desc()).all()


@router.get("/executions/{id}", response_model=CampaignExecutionResponse)
def get_execution_detail(id: str, db: Session = Depends(get_db)):
    execution = (
        db.query(CampaignExecution)
        .options(joinedload(CampaignExecution.steps))
        .filter(CampaignExecution.id == id)
        .first()
    )
    if not execution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution record not found")
    return execution


@router.post("/campaigns/{campaign_id}/execute", response_model=CampaignExecutionResponse, status_code=status.HTTP_200_OK)
async def execute_campaign(
    campaign_id: str,
    payload: Optional[ExecutionCreateRequest] = None,
    db: Session = Depends(get_db),
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    # Strict approval gate check at API level
    is_campaign_approved = campaign.status == CampaignStatus.APPROVED
    has_approved_assets = any(
        a.is_selected and a.status == ContentStatus.APPROVED for a in (campaign.content_assets or [])
    )
    if not (is_campaign_approved or has_approved_assets):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"UNAPPROVED_CAMPAIGN_BLOCKED: Campaign '{campaign.name}' has status '{campaign.status}'. "
                "Only approved campaigns or campaigns with approved selected content assets can be executed."
            ),
        )

    # Idempotency Check: if idempotency key already exists, return existing execution
    if payload and payload.idempotency_key:
        existing = db.query(CampaignExecution).filter(CampaignExecution.idempotency_key == payload.idempotency_key).first()
        if existing:
            return existing

    # Prevent concurrent active executions for the same campaign
    active_execution = (
        db.query(CampaignExecution)
        .filter(
            CampaignExecution.campaign_id == campaign_id,
            CampaignExecution.status.in_([ExecutionStatus.PENDING, ExecutionStatus.RUNNING, ExecutionStatus.RETRYING]),
        )
        .first()
    )
    if active_execution:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An active execution run ({active_execution.id}) is already in progress for this campaign.",
        )

    idempotency_key = (payload and payload.idempotency_key) or f"exec-{campaign_id}-{uuid.uuid4().hex[:8]}"

    execution = CampaignExecution(
        campaign_id=campaign.id,
        workspace_id=campaign.workspace_id,
        status=ExecutionStatus.PENDING,
        idempotency_key=idempotency_key,
        trigger_source=(payload and payload.trigger_source) or "manual_ui",
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    # Run LangGraph Execution Agent
    agent = CampaignExecutionAgent(db=db)
    updated_execution = await agent.execute_campaign(execution, campaign)

    return updated_execution


@router.post("/executions/{id}/retry", response_model=CampaignExecutionResponse)
async def retry_execution(id: str, db: Session = Depends(get_db)):
    execution = db.query(CampaignExecution).filter(CampaignExecution.id == id).first()
    if not execution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution record not found")

    if execution.status not in [ExecutionStatus.FAILED, ExecutionStatus.ESCALATED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot retry an execution with status '{execution.status}'. Must be FAILED or ESCALATED.",
        )

    if execution.retry_count >= execution.max_retries:
        # Max retries exhausted -> Escalate to human operator
        agent = CampaignExecutionAgent(db=db)
        state = {
            "campaign_id": execution.campaign_id,
            "execution_id": execution.id,
            "workspace_id": execution.workspace_id,
            "campaign_name": execution.campaign.name if execution.campaign else "Campaign",
            "campaign_status": execution.campaign.status if execution.campaign else "APPROVED",
            "objective": execution.campaign.objective if execution.campaign else "",
            "budget": None,
            "timeline": None,
            "selected_assets": [],
            "strategy_summary": None,
            "planned_channels": [],
            "n8n_execution_id": execution.n8n_execution_id,
            "n8n_workflow_id": execution.n8n_workflow_id,
            "status": ExecutionStatus.FAILED,
            "retry_count": execution.retry_count,
            "max_retries": execution.max_retries,
            "error_message": execution.error_message or "Max retries exceeded",
            "agent_trace": list(execution.agent_trace or []),
            "is_escalated": False,
        }
        res = agent._escalate_node(state)
        execution.status = ExecutionStatus.ESCALATED
        execution.error_message = res["error_message"]
        execution.agent_trace = state["agent_trace"]
        db.commit()
        db.refresh(execution)
        return execution

    campaign = execution.campaign
    agent = CampaignExecutionAgent(db=db)
    updated_execution = await agent.execute_campaign(execution, campaign)

    return updated_execution
