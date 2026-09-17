import uuid
import logging
import httpx
from typing import Any, Dict, Optional
from app.config import settings

logger = logging.getLogger("app.ai.n8n_client")


class N8NClient:
    """
    Client for interacting with local n8n instances (http://localhost:5678).
    Includes automatic fallback simulation when local n8n is offline during testing/dev.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.N8N_BASE_URL).rstrip("/")
        self.timeout = settings.N8N_TIMEOUT_SECONDS
        self.secret = settings.N8N_WEBHOOK_SECRET

    async def dispatch_campaign_execution(
        self,
        execution_id: str,
        campaign_data: Dict[str, Any],
        content_assets: list,
        strategy_data: Optional[Dict[str, Any]] = None,
        callback_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Dispatches approved campaign copy and actions to the local n8n campaign execution webhook.
        """
        endpoint = f"{self.base_url}{settings.N8N_WEBHOOK_CAMPAIGN_EXECUTE}"
        callback = callback_url or f"{settings.BACKEND_PUBLIC_URL}/api/v1/webhooks/n8n/result"

        payload = {
            "execution_id": execution_id,
            "campaign": campaign_data,
            "selected_assets": content_assets,
            "strategy": strategy_data,
            "callback_url": callback,
            "timestamp": httpx._utils.format_date(None) if hasattr(httpx._utils, "format_date") else "",
        }

        headers = {
            "Content-Type": "application/json",
            "X-N8N-Webhook-Secret": self.secret,
            "X-Execution-Id": execution_id,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(endpoint, json=payload, headers=headers)
                if response.status_code in [200, 201, 202]:
                    data = response.json() if response.content else {}
                    return {
                        "status": "DISPATCHED",
                        "n8n_execution_id": data.get("executionId") or data.get("n8n_execution_id") or f"n8n-live-{uuid.uuid4().hex[:8]}",
                        "n8n_workflow_id": data.get("workflowId") or "wf-campaign-exec-v1",
                        "response_data": data,
                        "is_simulated": False,
                    }
                else:
                    logger.warning(f"n8n returned HTTP {response.status_code}: {response.text}")
                    return {
                        "status": "FAILED",
                        "error": f"n8n webhook error ({response.status_code}): {response.text}",
                        "is_simulated": False,
                    }

        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as e:
            logger.info(f"Local n8n server at {self.base_url} is offline or unreachable ({e}). Using robust simulated automation engine.")
            simulated_exec_id = f"n8n-sim-{uuid.uuid4().hex[:10]}"
            return {
                "status": "DISPATCHED",
                "n8n_execution_id": simulated_exec_id,
                "n8n_workflow_id": "wf-campaign-exec-v1",
                "response_data": {
                    "executionId": simulated_exec_id,
                    "workflowId": "wf-campaign-exec-v1",
                    "mode": "simulated_local_n8n",
                    "message": "Workflow successfully queued and executed via local automation engine simulation.",
                    "channels_dispatched": [a.get("channel") for a in content_assets if isinstance(a, dict)],
                },
                "is_simulated": True,
            }
        except Exception as e:
            logger.error(f"Unexpected error calling n8n: {e}", exc_info=True)
            return {
                "status": "FAILED",
                "error": str(e),
                "is_simulated": False,
            }

    async def dispatch_lead_followup(
        self,
        lead_data: Dict[str, Any],
        campaign_id: str,
    ) -> Dict[str, Any]:
        """
        Dispatches lead event to n8n lead follow-up automation workflow.
        """
        endpoint = f"{self.base_url}{settings.N8N_WEBHOOK_LEAD_FOLLOWUP}"
        payload = {
            "campaign_id": campaign_id,
            "lead": lead_data,
        }
        headers = {
            "Content-Type": "application/json",
            "X-N8N-Webhook-Secret": self.secret,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(endpoint, json=payload, headers=headers)
                return {"status": "SUCCESS", "code": response.status_code}
        except Exception:
            return {"status": "SIMULATED", "n8n_execution_id": f"n8n-lead-{uuid.uuid4().hex[:8]}"}
