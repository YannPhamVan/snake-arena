"""
Integration tests for authentication flow.

Tests the complete authentication lifecycle including signup, login,
token management, and user profile retrieval using a real database.
"""

from fastapi.testclient import TestClient


def test_complete_auth_flow(client: TestClient):
    """Test complete authentication flow from signup to profile retrieval"""
    
    # Step 1: Sign up a new user
    signup_data = {
        "username": "integrationuser",
        "email": "integration@example.com",
        "password": "securepassword123"
    }
    signup_response = client.post("/api/auth/signup", json=signup_data)
    assert signup_response.status_code == 200
    
    signup_result = signup_response.json()
    assert "user" in signup_result
    assert "token" in signup_result
    assert signup_result["user"]["username"] == "integrationuser"
    assert signup_result["user"]["email"] == "integration@example.com"
    assert signup_result["user"]["highScore"] == 0
    
    first_token = signup_result["token"]
    user_id = signup_result["user"]["id"]
    
    # Step 2: Verify we can access profile with the token
    headers = {"Authorization": f"Bearer {first_token}"}
    profile_response = client.get("/api/auth/me", headers=headers)
    assert profile_response.status_code == 200
    
    profile = profile_response.json()
    assert profile["id"] == user_id
    assert profile["username"] == "integrationuser"
    
    # Step 3: Logout (client-side operation, token still valid on server)
    logout_response = client.post("/api/auth/logout", headers=headers)
    assert logout_response.status_code == 200
    
    # Step 4: Login with same credentials
    login_data = {
        "email": "integration@example.com",
        "password": "securepassword123"
    }
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    login_result = login_response.json()
    assert login_result["user"]["id"] == user_id
    assert login_result["user"]["username"] == "integrationuser"
    
    second_token = login_result["token"]
    
    # Step 5: Verify new token works
    new_headers = {"Authorization": f"Bearer {second_token}"}
    new_profile_response = client.get("/api/auth/me", headers=new_headers)
    assert new_profile_response.status_code == 200
    assert new_profile_response.json()["id"] == user_id


def test_duplicate_signup_prevention(client: TestClient):
    """Test that duplicate signups are properly prevented"""
    
    signup_data = {
        "username": "uniqueuser",
        "email": "unique@example.com",
        "password": "password123"
    }
    
    # First signup should succeed
    first_response = client.post("/api/auth/signup", json=signup_data)
    assert first_response.status_code == 200
    
    # Duplicate email should fail
    duplicate_email = {
        "username": "differentuser",
        "email": "unique@example.com",
        "password": "password123"
    }
    response = client.post("/api/auth/signup", json=duplicate_email)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()
    
    # Duplicate username should fail
    duplicate_username = {
        "username": "uniqueuser",
        "email": "different@example.com",
        "password": "password123"
    }
    response = client.post("/api/auth/signup", json=duplicate_username)
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"].lower()


def test_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    
    # Create a user first
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "correctpassword"
    }
    client.post("/api/auth/signup", json=signup_data)
    
    # Try to login with wrong password
    wrong_password = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", json=wrong_password)
    assert response.status_code == 401
    
    # Try to login with non-existent email
    wrong_email = {
        "email": "nonexistent@example.com",
        "password": "anypassword"
    }
    response = client.post("/api/auth/login", json=wrong_email)
    assert response.status_code == 401


def test_token_validation(client: TestClient):
    """Test JWT token validation"""
    
    # Invalid token format
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 401
    
    # Missing token
    response = client.get("/api/auth/me")
    assert response.status_code == 401  # FastAPI/HTTPBearer returns 401 for missing auth

