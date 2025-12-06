from fastapi.testclient import TestClient
from app.services.database import db_service
from app.models import GameMode


def test_get_leaderboard_empty(client: TestClient, db):
    """Test get leaderboard when empty"""
    response = client.get("/api/leaderboard/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_leaderboard_with_data(client: TestClient, db):
    """Test get leaderboard with data"""
    # Create a user and submit a score
    user = db_service.create_user(db, "testuser", "test@example.com", "password123")
    db_service.submit_score(db, user.id, user.username, 1000, GameMode.WALLS)
    
    response = client.get("/api/leaderboard/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["score"] == 1000


def test_get_leaderboard_with_mode_filter(client: TestClient, db):
    """Test get leaderboard with mode filter"""
    # Create user and submit scores for different modes
    user = db_service.create_user(db, "testuser", "test@example.com", "password123")
    db_service.submit_score(db, user.id, user.username, 1000, GameMode.WALLS)
    db_service.submit_score(db, user.id, user.username, 2000, GameMode.PASS_THROUGH)
    
    response = client.get("/api/leaderboard/?mode=walls")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # All entries should be walls mode
    for entry in data:
        assert entry["mode"] == "walls"


def test_get_leaderboard_with_limit(client: TestClient, db):
    """Test get leaderboard with limit"""
    # Create user and submit multiple scores
    user = db_service.create_user(db, "testuser", "test@example.com", "password123")
    for i in range(5):
        db_service.submit_score(db, user.id, user.username, 1000 + i * 100, GameMode.WALLS)
    
    response = client.get("/api/leaderboard/?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 3


def test_submit_score(client: TestClient, db):
    """Test submit score"""
    # Signup to get a token
    signup_response = client.post("/api/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    token = signup_response.json()["token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/leaderboard/", json={
        "score": 1000,
        "mode": "walls"
    }, headers=headers)
    assert response.status_code == 200
    
    # Verify score was added
    leaderboard_response = client.get("/api/leaderboard/")
    assert leaderboard_response.status_code == 200
    entries = leaderboard_response.json()
    assert any(entry["score"] == 1000 for entry in entries)

