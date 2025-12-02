from fastapi.testclient import TestClient

def test_get_leaderboard(client: TestClient):
    response = client.get("/leaderboard/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_leaderboard_with_mode_filter(client: TestClient):
    response = client.get("/leaderboard/?mode=walls")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # All entries should be walls mode
    for entry in data:
        assert entry["mode"] == "walls"

def test_get_leaderboard_with_limit(client: TestClient):
    response = client.get("/leaderboard/?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 3

def test_submit_score(client: TestClient):
    headers = {"Authorization": "Bearer mock-jwt-token"}
    response = client.post("/leaderboard/", json={
        "score": 1000,
        "mode": "walls"
    }, headers=headers)
    assert response.status_code == 200
