"""
Integration tests for leaderboard functionality.

Tests leaderboard queries, score submission, and filtering
with a real database including multiple users and entries.
"""

from fastapi.testclient import TestClient
from app.services.database import db_service
from app.models import GameMode


def test_leaderboard_with_multiple_users(client: TestClient, db_session):
    """Test leaderboard with multiple users and scores"""
    
    # Create multiple users and submit scores
    users = []
    for i in range(5):
        signup_data = {
            "username": f"player{i}",
            "email": f"player{i}@example.com",
            "password": "password123"
        }
        response = client.post("/api/auth/signup", json=signup_data)
        assert response.status_code == 200
        users.append(response.json())
    
    # Submit various scores
    scores = [
        (users[0]["token"], 1000, "walls"),
        (users[1]["token"], 1500, "walls"),
        (users[2]["token"], 800, "walls"),
        (users[0]["token"], 2000, "pass-through"),
        (users[3]["token"], 1200, "pass-through"),
    ]
    
    for token, score, mode in scores:
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/api/leaderboard/", json={"score": score, "mode": mode}, headers=headers)
        assert response.status_code == 200
    
    # Get all leaderboard entries
    response = client.get("/api/leaderboard/")
    assert response.status_code == 200
    entries = response.json()
    assert len(entries) == 5
    
    # Verify sorting (highest score first)
    assert entries[0]["score"] == 2000
    assert entries[1]["score"] == 1500
    
    # Test mode filtering
    walls_response = client.get("/api/leaderboard/?mode=walls")
    assert walls_response.status_code == 200
    walls_entries = walls_response.json()
    assert len(walls_entries) == 3
    for entry in walls_entries:
        assert entry["mode"] == "walls"
    
    passthrough_response = client.get("/api/leaderboard/?mode=pass-through")
    assert passthrough_response.status_code == 200
    passthrough_entries = passthrough_response.json()
    assert len(passthrough_entries) == 2
    for entry in passthrough_entries:
        assert entry["mode"] == "pass-through"


def test_score_submission_updates_high_score(client: TestClient, db_session):
    """Test that submitting scores updates user's high score"""
    
    # Create user
    signup_data = {
        "username": "scoretracker",
        "email": "scoretracker@example.com",
        "password": "password123"
    }
    response = client.post("/api/auth/signup", json=signup_data)
    token = response.json()["token"]
    user_id = response.json()["user"]["id"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Initial high score should be 0
    profile = client.get("/api/auth/me", headers=headers).json()
    assert profile["highScore"] == 0
    
    # Submit first score
    client.post("/api/leaderboard/", json={"score": 500, "mode": "walls"}, headers=headers)
    
    # Check high score updated
    user = db_service.get_user_by_id(db_session, user_id)
    assert user.high_score == 500
    
    # Submit higher score
    client.post("/api/leaderboard/", json={"score": 1000, "mode": "walls"}, headers=headers)
    
    # High score should be updated
    user = db_service.get_user_by_id(db_session, user_id)
    assert user.high_score == 1000
    
    # Submit lower score
    client.post("/api/leaderboard/", json={"score": 300, "mode": "walls"}, headers=headers)
    
    # High score should remain 1000
    user = db_service.get_user_by_id(db_session, user_id)
    assert user.high_score == 1000


def test_leaderboard_limit(client: TestClient):
    """Test leaderboard limit parameter"""
    
    # Create users and submit 15 scores
    for i in range(15):
        signup_data = {
            "username": f"limituser{i}",
            "email": f"limituser{i}@example.com",
            "password": "password123"
        }
        response = client.post("/api/auth/signup", json=signup_data)
        token = response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        client.post("/api/leaderboard/", json={"score": 100 * i, "mode": "walls"}, headers=headers)
    
    # Note: In integration tests, data persists between tests,
    # so we just verify the limit parameter works, not exact counts
    
    # Request with limit=5
    response = client.get("/api/leaderboard/?limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5
    
    # Request with limit=10  
    response = client.get("/api/leaderboard/?limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_leaderboard_requires_auth_for_submission(client: TestClient):
    """Test that submitting scores requires authentication"""
    
    # Try to submit without token
    response = client.post("/api/leaderboard/", json={"score": 1000, "mode": "walls"})
    assert response.status_code == 401  # HTTPBearer returns 401 for missing auth
    
    # Try with invalid token
    headers = {"Authorization": "Bearer invalid.token"}
    response = client.post("/api/leaderboard/", json={"score": 1000, "mode": "walls"}, headers=headers)
    assert response.status_code == 401
