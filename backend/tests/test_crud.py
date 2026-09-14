def test_workspace_crud(client):
    # Create workspace
    payload = {
        "name": "Test Growth Org",
        "slug": "test-growth-org",
        "industry": "FinTech",
        "website": "https://testfintech.com",
        "description": "Next gen fintech",
        "brand_guidelines": "Bold and secure",
    }
    create_resp = client.post("/api/v1/workspaces", json=payload)
    assert create_resp.status_code == 201
    workspace_data = create_resp.json()
    assert workspace_data["slug"] == "test-growth-org"
    workspace_id = workspace_data["id"]

    # List workspaces
    list_resp = client.get("/api/v1/workspaces")
    assert list_resp.status_code == 200
    assert any(w["id"] == workspace_id for w in list_resp.json())

    # Get single workspace
    get_resp = client.get(f"/api/v1/workspaces/{workspace_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Test Growth Org"

    # Update workspace
    update_resp = client.put(f"/api/v1/workspaces/{workspace_id}", json={"name": "Updated Growth Org"})
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Updated Growth Org"


def test_product_crud(client, seeded_db):
    workspace = seeded_db["workspace"]
    payload = {
        "workspace_id": workspace.id,
        "name": "Test Analytics Pro",
        "category": "Analytics",
        "description": "Real-time analytics engine",
        "price": "$499/mo",
        "features": ["Feature A", "Feature B"],
        "target_benefits": ["Benefit X"],
        "usp": "Fastest query engine",
    }
    create_resp = client.post("/api/v1/products", json=payload)
    assert create_resp.status_code == 201
    prod = create_resp.json()
    assert prod["name"] == "Test Analytics Pro"

    # List products
    list_resp = client.get(f"/api/v1/products?workspace_id={workspace.id}")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1


def test_audience_crud(client, seeded_db):
    workspace = seeded_db["workspace"]
    payload = {
        "workspace_id": workspace.id,
        "name": "Enterprise Data Engineers",
        "description": "Engineers managing pipeline orchestration",
        "demographics": {"title": "Staff Engineer"},
        "pain_points": ["Pipeline latency"],
        "interests": ["Kafka", "Spark"],
        "goals": ["Sub-second queries"],
        "preferred_channels": ["LinkedIn", "GitHub"],
    }
    create_resp = client.post("/api/v1/audiences", json=payload)
    assert create_resp.status_code == 201
    aud = create_resp.json()
    assert aud["name"] == "Enterprise Data Engineers"


def test_campaign_crud(client, seeded_db):
    workspace = seeded_db["workspace"]
    payload = {
        "workspace_id": workspace.id,
        "name": "New Year Conversion Sprint",
        "objective": "Customer Acquisition",
        "budget": "$10,000",
        "target_timeline": "Jan 2027",
    }
    create_resp = client.post("/api/v1/campaigns", json=payload)
    assert create_resp.status_code == 201
    camp = create_resp.json()
    assert camp["status"] == "DRAFT"
    camp_id = camp["id"]

    # Status update
    status_resp = client.patch(f"/api/v1/campaigns/{camp_id}/status", json={"status": "IN_REVIEW"})
    assert status_resp.status_code == 200
    assert status_resp.json()["status"] == "IN_REVIEW"
