"""
Integration tests for game session lifecycle.

Tests creating, updating, and ending game sessions with
real database persistence and multiple concurrent sessions.
"""

from fastapi.testclient import TestClient


def test_session_lifecycle(client: TestClient):
    """Test complete game session lifecycle"""
    
    # Create a user
    signup_response = client.post("/auth/signup", json={
        "username": "gamer",
        "email": "gamer@example.com",
        "password": "password123"
    })
    token = signup_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a session
    create_response = client.post("/sessions/", json={"mode": "walls"}, headers=headers)
    assert create_response.status_code == 200
    
    session_data = create_response.json()
    session_id = session_data["id"]
    assert session_data["mode"] == "walls"
    assert session_data["score"] == 0
    assert session_data["isActive"] is True
    assert session_data["username"] == "gamer"
    
    # Verify session appears in active sessions
    active_response = client.get("/sessions/")
    assert active_response.status_code == 200
    active_sessions = active_response.json()
    assert len(active_sessions) == 1
    assert active_sessions[0]["id"] == session_id
    
    # Update session score
    update_response = client.put(f"/sessions/{session_id}", json={"score": 500}, headers=headers)
    assert update_response.status_code == 200
    
    # Verify score was updated
    get_response = client.get(f"/sessions/{session_id}")
    assert get_response.status_code == 200
    assert get_response.json()["score"] == 500
    
    # Update score again
    client.put(f"/sessions/{session_id}", json={"score": 1000}, headers=headers)
    get_response = client.get(f"/sessions/{session_id}")
    assert get_response.json()["score"] == 1000
    
    # End the session
    end_response = client.delete(f"/sessions/{session_id}", headers=headers)
    assert end_response.status_code == 200
    
    # Verify session is no longer active
    get_response = client.get(f"/sessions/{session_id}")
    assert get_response.status_code == 200
    assert get_response.json()["isActive"] is False
    
    # Verify it doesn't appear in active sessions
    active_response = client.get("/sessions/")
    active_sessions = active_response.json()
    assert len(active_sessions) == 0


def test_multiple_concurrent_sessions(client: TestClient):
    """Test multiple users with concurrent sessions"""
    
    # Create three users
    users = []
    for i in range(3):
        signup_response = client.post("/auth/signup", json={
            "username": f"player{i}",
            "email": f"player{i}@example.com",
            "password": "password123"
        })
        users.append(signup_response.json())
    
    # Each user creates a session
    sessions = []
    for i, user in enumerate(users):
        headers = {"Authorization": f"Bearer {user['token']}"}
        mode = "walls" if i % 2 == 0 else "pass-through"
        create_response = client.post("/sessions/", json={"mode": mode}, headers=headers)
        session = create_response.json()
        sessions.append(session)
    
    # Verify all sessions are active
    active_response = client.get("/sessions/")
    active_sessions = active_response.json()
    assert len(active_sessions) == 3
    
    # Update scores for all sessions
    for i, session in enumerate(sessions):
        headers = {"Authorization": f"Bearer {users[i]['token']}"}
        score = (i + 1) * 100
        client.put(f"/sessions/{session['id']}", json={"score": score}, headers=headers)
    
    # Verify all scores updated
    for i, session in enumerate(sessions):
        get_response = client.get(f"/sessions/{session['id']}")
        assert get_response.json()["score"] == (i + 1) * 100
    
    # End first session
    headers = {"Authorization": f"Bearer {users[0]['token']}"}
    client.delete(f"/sessions/{sessions[0]['id']}", headers=headers)
    
    # Verify only 2 are still active
    active_response = client.get("/sessions/")
    active_sessions = active_response.json()
    assert len(active_sessions) == 2


def test_session_operations_require_auth(client: TestClient):
    """Test that session operations require authentication"""
    
    # Try to create session without auth
    response = client.post("/sessions/", json={"mode": "walls"})
    assert response.status_code == 401  # HTTPBearer returns 401
    
    # Create a user and session
    signup_response = client.post("/auth/signup", json={
        "username": "sessionuser",
        "email": "sessionuser@example.com",
        "password": "password123"
    })
    token = signup_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    create_response = client.post("/sessions/", json={"mode": "walls"}, headers=headers)
    session_id = create_response.json()["id"]
    
    # Try to update without auth
    response = client.put(f"/sessions/{session_id}", json={"score": 100})
    assert response.status_code == 401
    
    # Try to delete without auth
    response = client.delete(f"/sessions/{session_id}")
    assert response.status_code == 401
    
    # Verify operations work with auth
    assert client.put(f"/sessions/{session_id}", json={"score": 100}, headers=headers).status_code == 200
    assert client.delete(f"/sessions/{session_id}", headers=headers).status_code == 200


def test_nonexistent_session(client: TestClient):
    """Test operations on non-existent session"""
    
    # Try to get non-existent session
    response = client.get("/sessions/nonexistent-id")
    assert response.status_code == 404
    
    # Create a user for auth
    signup_response = client.post("/auth/signup", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    token = signup_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try to update non-existent session
    response = client.put("/sessions/nonexistent-id", json={"score": 100}, headers=headers)
    assert response.status_code == 404
    
    # Try to delete non-existent session
    response = client.delete("/sessions/nonexistent-id", headers=headers)
    assert response.status_code == 404


def test_session_data_persistence(client: TestClient):
    """Test that session data persists correctly"""
    
    # Create user and session
    signup_response = client.post("/auth/signup", json={
        "username": "persistent",
        "email": "persistent@example.com",
        "password": "password123"
    })
    token = signup_response.json()["token"]
    user_id = signup_response.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create session
    create_response = client.post("/sessions/", json={"mode": "pass-through"}, headers=headers)
    session_id = create_response.json()["id"]
    
    # Update score multiple times
    for score in [100, 250, 500, 750, 1000]:
        client.put(f"/sessions/{session_id}", json={"score": score}, headers=headers)
    
    # Retrieve session and verify final score
    get_response = client.get(f"/sessions/{session_id}")
    session = get_response.json()
    assert session["score"] == 1000
    assert session["userId"] == user_id
    assert session["mode"] == "pass-through"
    assert session["isActive"] is True
