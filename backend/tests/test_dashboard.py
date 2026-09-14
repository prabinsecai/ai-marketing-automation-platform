def test_dashboard_stats(client, seeded_db):
    workspace = seeded_db["workspace"]
    response = client.get(f"/api/v1/dashboard/stats?workspace_id={workspace.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["workspace_name"] == workspace.name
    assert data["total_campaigns"] >= 1
    assert data["total_products"] >= 1
    assert data["total_audiences"] >= 1
    assert "campaign_status_counts" in data
    assert "content_status_counts" in data
    assert len(data["recent_campaigns"]) >= 1
    assert len(data["recent_ai_activity"]) >= 1
