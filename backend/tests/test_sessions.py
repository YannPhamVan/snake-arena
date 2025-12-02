from fastapi.testclient import TestClient

def test_get_active_sessions(client: TestClient):
    response = client.get("/sessions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_session(client: TestClient):
    headers = {"Authorization": "Bearer mock-jwt-token"}
    response = client.post("/sessions/", json={"mode": "walls"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "walls"
    assert data["isActive"] is True
    assert data["score"] == 0

def test_get_session(client: TestClient):
    headers = {"Authorization": "Bearer mock-jwt-token"}
    # Create session first
    create_res = client.post("/sessions/", json={"mode": "walls"}, headers=headers)
    session_id = create_res.json()["id"]
    
    # Get session
    response = client.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    assert response.json()["id"] == session_id

def test_update_session(client: TestClient):
    headers = {"Authorization": "Bearer mock-jwt-token"}
    # Create session first
    create_res = client.post("/sessions/", json={"mode": "walls"}, headers=headers)
    session_id = create_res.json()["id"]
    
    # Update
    response = client.put(f"/sessions/{session_id}", json={"score": 100}, headers=headers)
    assert response.status_code == 200
    
    # Verify
    get_res = client.get(f"/sessions/{session_id}")
    assert get_res.json()["score"] == 100

def test_end_session(client: TestClient):
    headers = {"Authorization": "Bearer mock-jwt-token"}
    # Create session first
    create_res = client.post("/sessions/", json={"mode": "pass-through"}, headers=headers)
    session_id = create_res.json()["id"]
    
    # End session
    response = client.delete(f"/sessions/{session_id}", headers=headers)
    assert response.status_code == 200
    
    # Verify it's no longer active
    get_res = client.get(f"/sessions/{session_id}")
    assert get_res.json()["isActive"] is False

def test_get_nonexistent_session(client: TestClient):
    response = client.get("/sessions/nonexistent-id")
    assert response.status_code == 404
