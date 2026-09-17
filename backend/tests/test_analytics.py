import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.campaign import Campaign
from app.models.analytics import CampaignMetric
from datetime import date

def test_add_metrics(db_session, client):
    from app.seed.demo_data import seed_demo_data
    seed_demo_data(db_session)
    campaign = db_session.query(Campaign).first()
    assert campaign is not None
    
    response = client.post(
        f"/api/v1/campaigns/{campaign.id}/metrics",
        json={
            "campaign_id": campaign.id,
            "channel": "EMAIL",
            "date": date.today().isoformat(),
            "impressions": 1000,
            "clicks": 50,
            "spend": 10.0,
            "leads": 5,
            "conversions": 1,
            "revenue": 100.0
        }
    )
    assert response.status_code == 201
    
    # Test performance endpoint
    resp2 = client.get(f"/api/v1/campaigns/{campaign.id}/analytics")
    assert resp2.status_code == 200
    data = resp2.json()
    assert "performance" in data
    assert data["performance"]["ctr"] > 0
    assert "diagnostics" in data
