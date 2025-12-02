from fastapi.testclient import TestClient

def test_signup(client: TestClient):
    response = client.post("/auth/signup", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "newuser"
    assert "token" in data

def test_signup_duplicate_user(client: TestClient):
    # Create first user
    client.post("/auth/signup", json={
        "username": "duplicate",
        "email": "dup@example.com",
        "password": "password123"
    })
    # Try to create duplicate
    response = client.post("/auth/signup", json={
        "username": "duplicate",
        "email": "dup2@example.com",
        "password": "password123"
    })
    assert response.status_code == 400

def test_login(client: TestClient):
    # Mock db initializes with some users
    response = client.post("/auth/login", json={
        "email": "snake@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "snake@example.com"
    assert "token" in data

def test_logout(client: TestClient):
    headers = {"Authorization": "Bearer mock-jwt-token"}
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200

def test_get_me(client: TestClient):
    headers = {"Authorization": "Bearer mock-jwt-token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert "username" in response.json()
