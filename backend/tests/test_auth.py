from fastapi.testclient import TestClient
from app.services.database import db_service
from app.models import GameMode


def test_signup(client: TestClient, db):
    """Test user signup"""
    response = client.post("/api/auth/signup", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "new@example.com"
    assert "token" in data
    assert data["token"] != "mock-jwt-token"  # Should be a real JWT token


def test_signup_duplicate_email(client: TestClient, db):
    """Test signup with duplicate email"""
    # Create first user
    client.post("/api/auth/signup", json={
        "username": "user1",
        "email": "dup@example.com",
        "password": "password123"
    })
    # Try to create user with same email
    response = client.post("/api/auth/signup", json={
        "username": "user2",
        "email": "dup@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_signup_duplicate_username(client: TestClient, db):
    """Test signup with duplicate username"""
    # Create first user
    client.post("/api/auth/signup", json={
        "username": "duplicate",
        "email": "user1@example.com",
        "password": "password123"
    })
    # Try to create user with same username
    response = client.post("/api/auth/signup", json={
        "username": "duplicate",
        "email": "user2@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"].lower()


def test_login(client: TestClient, db):
    """Test user login"""
    # First signup
    signup_response = client.post("/api/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert signup_response.status_code == 200
    
    # Then login
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "test@example.com"
    assert "token" in data


def test_login_invalid_credentials(client: TestClient, db):
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_logout(client: TestClient, db):
    """Test logout endpoint"""
    # Signup to get a token
    signup_response = client.post("/api/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    token = signup_response.json()["token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 200


def test_get_me(client: TestClient, db):
    """Test getting current user profile"""
    # Signup to get a token
    signup_response = client.post("/api/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    token = signup_response.json()["token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_me_invalid_token(client: TestClient, db):
    """Test getting current user with invalid token"""
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 401

