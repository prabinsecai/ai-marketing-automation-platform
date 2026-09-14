from app.models.campaign import Campaign, CampaignStatus
from app.models.product import Product
from app.models.audience import Audience


def test_full_campaign_ai_lifecycle(client, seeded_db):
    workspace = seeded_db["workspace"]
    db = seeded_db["db"]

    product = db.query(Product).filter(Product.workspace_id == workspace.id).first()
    audience = db.query(Audience).filter(Audience.workspace_id == workspace.id).first()

    # Step 1: Create Campaign (DRAFT)
    create_resp = client.post("/api/v1/campaigns", json={
        "workspace_id": workspace.id,
        "product_id": product.id,
        "audience_id": audience.id,
        "name": "Integration Test Automated Sprint",
        "objective": "Lead Generation & Demo Bookings",
        "budget": "$12,000",
        "target_timeline": "4-week sprint",
    })
    assert create_resp.status_code == 201
    campaign_id = create_resp.json()["id"]
    assert create_resp.json()["status"] == CampaignStatus.DRAFT

    # Step 2: Generate Strategy (DRAFT -> STRATEGY_GENERATED)
    strat_resp = client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")
    assert strat_resp.status_code == 200
    strat_data = strat_resp.json()
    assert strat_data["campaign_id"] == campaign_id
    assert len(strat_data["summary"]) > 20
    assert len(strat_data["channel_strategy"]) >= 2
    assert len(strat_data["campaign_themes"]) >= 2

    # Verify campaign status advanced
    camp_detail = client.get(f"/api/v1/campaigns/{campaign_id}").json()
    assert camp_detail["status"] == CampaignStatus.STRATEGY_GENERATED

    # Step 3: Generate Multi-Channel Content (STRATEGY_GENERATED -> CONTENT_GENERATED)
    content_resp = client.post(f"/api/v1/campaigns/{campaign_id}/content/generate")
    assert content_resp.status_code == 200
    assets = content_resp.json()
    assert len(assets) >= 6  # At least 2 email, 3 social, 1+ ad

    # Check channels exist
    channels = {a["channel"] for a in assets}
    assert "EMAIL" in channels
    assert "SOCIAL" in channels
    assert "ADVERTISEMENT" in channels

    # Verify campaign status advanced
    camp_detail_2 = client.get(f"/api/v1/campaigns/{campaign_id}").json()
    assert camp_detail_2["status"] == CampaignStatus.CONTENT_GENERATED

    # Step 4: Edit a Content Asset
    target_asset = assets[0]
    asset_id = target_asset["id"]
    edit_resp = client.patch(f"/api/v1/content-assets/{asset_id}", json={
        "body": "Updated customized body copy with additional customer quote.",
        "edit_summary": "Added customer quote",
    })
    assert edit_resp.status_code == 200
    updated_asset = edit_resp.json()
    assert "Updated customized body copy" in updated_asset["body"]
    assert len(updated_asset["edit_history"]) >= 1

    # Step 5: Regenerate Single Variation
    regen_resp = client.post(f"/api/v1/content-assets/{asset_id}/regenerate", json={
        "instructions": "Make it more urgent and emphasize the 70% time savings metric."
    })
    assert regen_resp.status_code == 200
    regenerated_asset = regen_resp.json()
    assert len(regenerated_asset["body"]) > 10

    # Step 6: Toggle Selection
    toggle_resp = client.post(f"/api/v1/content-assets/{asset_id}/select")
    assert toggle_resp.status_code == 200

    # Step 7: Submit Approval Action
    approval_resp = client.post(f"/api/v1/content-assets/{asset_id}/approve", json={
        "action": "APPROVE",
        "feedback": "Approved for live launch.",
    })
    assert approval_resp.status_code == 200
    assert approval_resp.json()["action"] == "APPROVE"

    # Verify asset status is APPROVED
    asset_check = client.get(f"/api/v1/content-assets/{asset_id}").json()
    assert asset_check["status"] == "APPROVED"
