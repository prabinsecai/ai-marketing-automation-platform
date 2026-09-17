import pytest
from app.models.campaign import Campaign, CampaignStatus
from app.models.content import ContentAsset, ContentStatus
from app.models.execution import CampaignExecution, ExecutionStatus
from app.models.execution_step import ExecutionStep, StepStatus
from app.ai.agents.execution_agent import CampaignExecutionAgent


def test_unapproved_campaign_execution_blocked(client, seeded_db):
    """Execution must be strictly blocked if campaign is not APPROVED."""
    workspace = seeded_db["workspace"]
    db = seeded_db["db"]

    # Create a draft campaign
    draft_campaign = Campaign(
        workspace_id=workspace.id,
        name="Draft Unapproved Campaign",
        objective="Lead Generation",
        status=CampaignStatus.DRAFT,
    )
    db.add(draft_campaign)
    db.commit()

    resp = client.post(
        f"/api/v1/campaigns/{draft_campaign.id}/execute",
        json={"workspace_id": workspace.id},
    )
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert "UNAPPROVED_CAMPAIGN_BLOCKED" in detail or "must be in APPROVED status" in detail


def test_approved_campaign_execution_flow(client, seeded_db):
    """An approved campaign with approved content must execute smoothly through LangGraph & n8n client."""
    workspace = seeded_db["workspace"]
    db = seeded_db["db"]

    # 1. Create an approved campaign with approved assets
    campaign = Campaign(
        workspace_id=workspace.id,
        name="Cloud Migration Drive",
        objective="Enterprise Signups",
        status=CampaignStatus.APPROVED,
    )
    db.add(campaign)
    db.commit()

    asset1 = ContentAsset(
        campaign_id=campaign.id,
        channel="email",
        title="Email Subject",
        body="Join our cloud workshop",
        status=ContentStatus.APPROVED,
    )
    asset2 = ContentAsset(
        campaign_id=campaign.id,
        channel="linkedin",
        title="LinkedIn Ad",
        body="Cloud infrastructure made simple",
        status=ContentStatus.APPROVED,
    )
    db.add_all([asset1, asset2])
    db.commit()

    # 2. Trigger execution
    resp = client.post(
        f"/api/v1/campaigns/{campaign.id}/execute",
        json={"workspace_id": workspace.id, "trigger_source": "manual_ui"},
    )
    assert resp.status_code == 200
    data = resp.json()

    assert data["campaign_id"] == campaign.id
    assert data["workspace_id"] == workspace.id
    assert data["status"] in [ExecutionStatus.SUCCESS, ExecutionStatus.RUNNING]
    assert len(data["steps"]) >= 3
    assert len(data["agent_trace"]) >= 3

    step_names = [s["step_name"] for s in data["steps"]]
    assert "validate_approval" in step_names
    assert "plan_execution" in step_names
    assert "dispatch_n8n_webhook" in step_names


def test_execution_idempotency(client, seeded_db):
    """Executing twice with the same idempotency key should return the existing execution."""
    workspace = seeded_db["workspace"]
    db = seeded_db["db"]

    campaign = Campaign(
        workspace_id=workspace.id,
        name="Idempotency Test Campaign",
        objective="Test Objective",
        status=CampaignStatus.APPROVED,
    )
    db.add(campaign)
    db.commit()

    asset = ContentAsset(
        campaign_id=campaign.id,
        channel="email",
        title="Email",
        body="Content",
        status=ContentStatus.APPROVED,
    )
    db.add(asset)
    db.commit()

    key = "custom-idempotency-test-key-123"

    resp1 = client.post(
        f"/api/v1/campaigns/{campaign.id}/execute",
        json={"workspace_id": workspace.id, "idempotency_key": key},
    )
    assert resp1.status_code == 200
    exec_id_1 = resp1.json()["id"]

    resp2 = client.post(
        f"/api/v1/campaigns/{campaign.id}/execute",
        json={"workspace_id": workspace.id, "idempotency_key": key},
    )
    assert resp2.status_code == 200
    exec_id_2 = resp2.json()["id"]

    assert exec_id_1 == exec_id_2


def test_n8n_webhook_callback(client, seeded_db):
    """POST /api/v1/webhooks/n8n/result should update execution and record step."""
    workspace = seeded_db["workspace"]
    db = seeded_db["db"]

    campaign = Campaign(
        workspace_id=workspace.id,
        name="Callback Campaign",
        objective="Test Objective",
        status=CampaignStatus.APPROVED,
    )
    db.add(campaign)
    db.commit()

    execution = CampaignExecution(
        campaign_id=campaign.id,
        workspace_id=workspace.id,
        status=ExecutionStatus.RUNNING,
        idempotency_key="cb-test-key-001",
        trigger_source="manual_ui",
    )
    db.add(execution)
    db.commit()

    payload = {
        "execution_id": execution.id,
        "campaign_id": campaign.id,
        "status": "SUCCESS",
        "n8n_execution_id": "n8n-live-789",
        "channel_results": {"email": "sent_150"},
    }

    resp = client.post(
        "/api/v1/webhooks/n8n/result",
        json=payload,
        headers={"X-N8N-Webhook-Secret": "marketing-automation-n8n-secret"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] in ["ACKNOWLEDGED", "PROCESSED"]

    db.refresh(execution)
    assert execution.status == ExecutionStatus.SUCCESS
    assert execution.n8n_execution_id == "n8n-live-789"
    assert execution.completed_at is not None


def test_executions_listing_and_detail(client, seeded_db):
    """GET /api/v1/executions and GET /api/v1/executions/{id} endpoint validation."""
    workspace = seeded_db["workspace"]
    db = seeded_db["db"]

    campaign = Campaign(
        workspace_id=workspace.id,
        name="Listing Test Campaign",
        objective="Test Objective",
        status=CampaignStatus.APPROVED,
    )
    db.add(campaign)
    db.commit()

    asset = ContentAsset(
        campaign_id=campaign.id,
        channel="email",
        title="Email",
        body="Body",
        status=ContentStatus.APPROVED,
    )
    db.add(asset)
    db.commit()

    exec_resp = client.post(
        f"/api/v1/campaigns/{campaign.id}/execute",
        json={"workspace_id": workspace.id},
    )
    exec_id = exec_resp.json()["id"]

    # List
    list_resp = client.get(f"/api/v1/executions?workspace_id={workspace.id}")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert any(x["id"] == exec_id for x in items)

    # Detail
    detail_resp = client.get(f"/api/v1/executions/{exec_id}?workspace_id={workspace.id}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == exec_id


def test_retry_and_escalation_logic(client, seeded_db):
    """Retrying an execution advances retry_count; exceeding max_retries escalates to human."""
    workspace = seeded_db["workspace"]
    db = seeded_db["db"]

    campaign = Campaign(
        workspace_id=workspace.id,
        name="Failing Campaign",
        objective="Test Objective",
        status=CampaignStatus.APPROVED,
    )
    db.add(campaign)
    db.commit()

    asset = ContentAsset(
        campaign_id=campaign.id,
        channel="email",
        title="Email",
        body="Body",
        status=ContentStatus.APPROVED,
    )
    db.add(asset)
    db.commit()

    # Create a failed execution with max_retries=1 and retry_count=1
    execution = CampaignExecution(
        campaign_id=campaign.id,
        workspace_id=workspace.id,
        status=ExecutionStatus.FAILED,
        idempotency_key="fail-key-999",
        retry_count=1,
        max_retries=1,
        error_message="Downstream service timeout",
    )
    db.add(execution)
    db.commit()

    # Attempt retry when retry_count >= max_retries -> should escalate
    resp = client.post(f"/api/v1/executions/{execution.id}/retry", json={"workspace_id": workspace.id})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == ExecutionStatus.ESCALATED
    assert "escalat" in data["error_message"].lower()
