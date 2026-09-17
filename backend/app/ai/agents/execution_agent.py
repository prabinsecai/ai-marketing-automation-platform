import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TypedDict
from sqlalchemy.orm import Session
from langgraph.graph import StateGraph, END

from app.config import settings
from app.models.campaign import Campaign, CampaignStatus
from app.models.content import ContentAsset, ContentStatus
from app.models.execution import CampaignExecution, ExecutionStatus
from app.models.execution_step import ExecutionStep, StepStatus
from app.ai.n8n_client import N8NClient

logger = logging.getLogger("app.ai.execution_agent")


class CampaignExecutionState(TypedDict):
    campaign_id: str
    execution_id: str
    workspace_id: str
    campaign_name: str
    campaign_status: str
    objective: str
    budget: Optional[str]
    timeline: Optional[str]
    selected_assets: List[Dict[str, Any]]
    strategy_summary: Optional[str]
    planned_channels: List[str]
    n8n_execution_id: Optional[str]
    n8n_workflow_id: Optional[str]
    status: str
    retry_count: int
    max_retries: int
    error_message: Optional[str]
    agent_trace: List[Dict[str, Any]]
    is_escalated: bool


class CampaignExecutionAgent:
    """
    LangGraph-powered Campaign Execution Agent.
    Strictly validates approval, orchestrates local n8n workflows, manages retries, and escalates failures.
    """

    def __init__(self, db: Session):
        self.db = db
        self.n8n_client = N8NClient()
        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(CampaignExecutionState)

        # Add Nodes
        builder.add_node("validate_approval", self._validate_approval_node)
        builder.add_node("plan_execution", self._plan_execution_node)
        builder.add_node("dispatch_workflows", self._dispatch_workflows_node)
        builder.add_node("evaluate_result", self._evaluate_result_node)
        builder.add_node("handle_retry", self._handle_retry_node)
        builder.add_node("escalate", self._escalate_node)

        # Set Entry Point
        builder.set_entry_point("validate_approval")

        # Conditional Edges
        builder.add_conditional_edges(
            "validate_approval",
            self._route_after_validation,
            {
                "proceed": "plan_execution",
                "blocked": END,
            },
        )

        builder.add_edge("plan_execution", "dispatch_workflows")
        builder.add_edge("dispatch_workflows", "evaluate_result")

        builder.add_conditional_edges(
            "evaluate_result",
            self._route_after_evaluation,
            {
                "success": END,
                "retry": "handle_retry",
                "escalate": "escalate",
            },
        )

        builder.add_edge("handle_retry", "dispatch_workflows")
        builder.add_edge("escalate", END)

        return builder.compile()

    # --- Node Implementations ---

    def _record_step(
        self,
        execution_id: str,
        step_name: str,
        step_type: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        status: str,
        error_message: Optional[str] = None,
    ) -> None:
        step = ExecutionStep(
            execution_id=execution_id,
            step_name=step_name,
            step_type=step_type,
            status=status,
            input_data=input_data,
            output_data=output_data,
            error_message=error_message,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        self.db.add(step)
        self.db.commit()

    def _append_trace(self, state: CampaignExecutionState, node: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        trace_entry = {
            "node": node,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "details": details or {},
        }
        state["agent_trace"].append(trace_entry)

    def _validate_approval_node(self, state: CampaignExecutionState) -> Dict[str, Any]:
        """
        Guards against unapproved execution. Campaign must be APPROVED or have approved selected assets.
        """
        campaign = self.db.query(Campaign).filter(Campaign.id == state["campaign_id"]).first()
        if not campaign:
            err = f"Campaign '{state['campaign_id']}' does not exist."
            self._append_trace(state, "validate_approval", f"Validation Failed: {err}")
            state["status"] = ExecutionStatus.FAILED
            state["error_message"] = err
            self._record_step(state["execution_id"], "validate_approval", "agent_node", {"campaign_id": state["campaign_id"]}, {}, StepStatus.FAILED, err)
            return {"status": ExecutionStatus.FAILED, "error_message": err}

        # Strict approval check
        is_campaign_approved = campaign.status == CampaignStatus.APPROVED
        has_approved_assets = any(
            a.is_selected and a.status == ContentStatus.APPROVED for a in campaign.content_assets
        )

        if not (is_campaign_approved or has_approved_assets):
            err = (
                f"UNAPPROVED_CAMPAIGN_BLOCKED: Campaign '{campaign.name}' has status '{campaign.status}'. "
                "Only campaigns in 'APPROVED' status or with approved selected content assets may be executed."
            )
            self._append_trace(state, "validate_approval", f"Blocked: {err}")
            state["status"] = ExecutionStatus.FAILED
            state["error_message"] = err
            self._record_step(state["execution_id"], "validate_approval", "agent_node", {"campaign_status": campaign.status}, {}, StepStatus.FAILED, err)
            return {"status": ExecutionStatus.FAILED, "error_message": err}

        self._append_trace(state, "validate_approval", f"Campaign '{campaign.name}' verified as APPROVED for execution.")
        self._record_step(
            state["execution_id"],
            "validate_approval",
            "agent_node",
            {"campaign_id": campaign.id, "status": campaign.status},
            {"approval_confirmed": True, "approved_assets_count": len(state["selected_assets"])},
            StepStatus.SUCCESS,
        )
        return {"status": ExecutionStatus.RUNNING, "error_message": None}

    def _plan_execution_node(self, state: CampaignExecutionState) -> Dict[str, Any]:
        """
        Determines targeted channels, maps tools, and prepares n8n payload packages.
        """
        channels = list({a.get("channel") for a in state["selected_assets"] if isinstance(a, dict)})
        if not channels:
            channels = ["EMAIL", "SOCIAL", "ADVERTISEMENT"]

        plan_details = {
            "target_channels": channels,
            "assets_count": len(state["selected_assets"]),
            "n8n_target_endpoint": settings.N8N_WEBHOOK_CAMPAIGN_EXECUTE,
            "execution_mode": "n8n_webhook_dispatch",
        }

        self._append_trace(state, "plan_execution", f"Execution plan formulated for channels: {', '.join(channels)}", plan_details)
        self._record_step(state["execution_id"], "plan_execution", "agent_node", {"selected_assets": len(state["selected_assets"])}, plan_details, StepStatus.SUCCESS)

        return {"planned_channels": channels}

    async def _dispatch_workflows_node(self, state: CampaignExecutionState) -> Dict[str, Any]:
        """
        Calls the local n8n campaign webhook.
        """
        self._append_trace(state, "dispatch_workflows", f"Dispatching campaign payload to local n8n (Attempt #{state['retry_count'] + 1})")

        campaign_payload = {
            "id": state["campaign_id"],
            "name": state["campaign_name"],
            "objective": state["objective"],
            "budget": state["budget"],
            "timeline": state["timeline"],
        }

        result = await self.n8n_client.dispatch_campaign_execution(
            execution_id=state["execution_id"],
            campaign_data=campaign_payload,
            content_assets=state["selected_assets"],
            strategy_data={"summary": state["strategy_summary"]},
        )

        if result.get("status") == "FAILED":
            err = result.get("error", "n8n webhook dispatch error")
            self._append_trace(state, "dispatch_workflows", f"Dispatch Failed: {err}")
            self._record_step(state["execution_id"], "dispatch_n8n_webhook", "webhook_dispatch", campaign_payload, result, StepStatus.FAILED, err)
            return {"status": ExecutionStatus.FAILED, "error_message": err}

        n8n_exec_id = result.get("n8n_execution_id")
        n8n_wf_id = result.get("n8n_workflow_id")
        is_sim = result.get("is_simulated", False)

        msg = f"Successfully dispatched to n8n (Execution ID: {n8n_exec_id})" + (" [Simulated Offline Mode]" if is_sim else "")
        self._append_trace(state, "dispatch_workflows", msg, result)
        self._record_step(state["execution_id"], "dispatch_n8n_webhook", "webhook_dispatch", campaign_payload, result, StepStatus.SUCCESS)

        return {
            "status": ExecutionStatus.SUCCESS,
            "n8n_execution_id": n8n_exec_id,
            "n8n_workflow_id": n8n_wf_id,
            "error_message": None,
        }

    def _evaluate_result_node(self, state: CampaignExecutionState) -> Dict[str, Any]:
        """
        Evaluates the outcome of the dispatch.
        """
        if state["status"] == ExecutionStatus.SUCCESS:
            self._append_trace(state, "evaluate_result", "Campaign execution completed successfully.")
            self._record_step(state["execution_id"], "evaluate_result", "agent_node", {"n8n_execution_id": state["n8n_execution_id"]}, {"status": "SUCCESS"}, StepStatus.SUCCESS)
            return {"status": ExecutionStatus.SUCCESS}

        # Error evaluation
        self._append_trace(state, "evaluate_result", f"Execution error evaluated: {state.get('error_message')}")
        return {"status": state["status"]}

    def _handle_retry_node(self, state: CampaignExecutionState) -> Dict[str, Any]:
        """
        Retries failed step if retry count is under max_retries.
        """
        new_retry_count = state["retry_count"] + 1
        self._append_trace(
            state,
            "handle_retry",
            f"Scheduling retry attempt {new_retry_count} of {state['max_retries']}.",
            {"previous_error": state["error_message"]},
        )
        self._record_step(
            state["execution_id"],
            "handle_retry",
            "agent_node",
            {"retry_count": state["retry_count"]},
            {"new_retry_count": new_retry_count},
            StepStatus.SUCCESS,
        )
        return {"retry_count": new_retry_count, "status": ExecutionStatus.RETRYING}

    def _escalate_node(self, state: CampaignExecutionState) -> Dict[str, Any]:
        """
        Escalates execution to human operator when retries are exhausted.
        """
        escalation_reason = (
            f"ESCALATION REQUIRED: Execution failed after {state['retry_count']} retry attempts. "
            f"Last Error: {state.get('error_message') or 'Unknown automation failure'}. "
            "Action Required: Check local n8n server connectivity (http://localhost:5678) and review webhook logs."
        )
        self._append_trace(state, "escalate", f"ESCALATION TRIGGERED: {escalation_reason}", {"action_required": True})
        self._record_step(
            state["execution_id"],
            "escalate",
            "escalation",
            {"retry_count": state["retry_count"], "error": state["error_message"]},
            {"escalation_reason": escalation_reason},
            StepStatus.FAILED,
            escalation_reason,
        )
        return {"status": ExecutionStatus.ESCALATED, "is_escalated": True, "error_message": escalation_reason}

    # --- Routing Conditions ---

    def _route_after_validation(self, state: CampaignExecutionState) -> str:
        if state["status"] == ExecutionStatus.FAILED:
            return "blocked"
        return "proceed"

    def _route_after_evaluation(self, state: CampaignExecutionState) -> str:
        if state["status"] == ExecutionStatus.SUCCESS:
            return "success"
        if state["retry_count"] < state["max_retries"]:
            return "retry"
        return "escalate"

    # --- Execution Driver ---

    async def execute_campaign(
        self,
        execution: CampaignExecution,
        campaign: Campaign,
        force_fail_for_test: bool = False,
    ) -> CampaignExecution:
        """
        Runs the full LangGraph execution graph for the given campaign.
        """
        execution.status = ExecutionStatus.RUNNING
        execution.started_at = datetime.now(timezone.utc)
        self.db.commit()

        # Extract selected content assets
        selected_assets = [
            {
                "id": a.id,
                "channel": a.channel,
                "title": a.title,
                "body": a.body,
                "cta": a.cta,
                "platform": a.platform,
                "status": a.status,
            }
            for a in (campaign.content_assets or [])
            if a.is_selected or a.status == ContentStatus.APPROVED
        ]

        initial_state: CampaignExecutionState = {
            "campaign_id": campaign.id,
            "execution_id": execution.id,
            "workspace_id": campaign.workspace_id,
            "campaign_name": campaign.name,
            "campaign_status": campaign.status,
            "objective": campaign.objective,
            "budget": campaign.budget,
            "timeline": campaign.target_timeline,
            "selected_assets": selected_assets,
            "strategy_summary": campaign.strategy.summary if campaign.strategy else None,
            "planned_channels": [],
            "n8n_execution_id": execution.n8n_execution_id,
            "n8n_workflow_id": execution.n8n_workflow_id,
            "status": execution.status,
            "retry_count": execution.retry_count,
            "max_retries": execution.max_retries,
            "error_message": None,
            "agent_trace": list(execution.agent_trace or []),
            "is_escalated": False,
        }

        # Run StateGraph
        final_state = await self.graph.ainvoke(initial_state)

        # Update Execution Model
        execution.status = final_state["status"]
        execution.retry_count = final_state["retry_count"]
        execution.n8n_execution_id = final_state.get("n8n_execution_id")
        execution.n8n_workflow_id = final_state.get("n8n_workflow_id")
        execution.error_message = final_state.get("error_message")
        execution.agent_trace = final_state.get("agent_trace", [])
        execution.completed_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(execution)
        return execution
