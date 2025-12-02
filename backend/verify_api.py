#!/usr/bin/env python3
"""
Verify API Script
Tests the running server to ensure all endpoints work correctly.
Run this while the server is running: uv run python verify_api.py
"""

import httpx
import sys
from typing import Dict, Any

# Base URL of the running server
BASE_URL = "http://localhost:8000"

# Test credentials
TEST_EMAIL = "snake@example.com"
TEST_PASSWORD = "password123"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(name: str, passed: bool, details: str = ""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details:
        print(f"      {details}")

def test_root():
    """Test root endpoint"""
    try:
        response = httpx.get(f"{BASE_URL}/")
        passed = response.status_code == 200 and "message" in response.json()
        print_test("GET /", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("GET /", False, f"Error: {str(e)}")
        return False

def test_signup():
    """Test user signup"""
    try:
        import random
        random_suffix = random.randint(1000, 9999)
        response = httpx.post(f"{BASE_URL}/auth/signup", json={
            "username": f"testuser{random_suffix}",
            "email": f"test{random_suffix}@example.com",
            "password": "testpass123"
        })
        passed = response.status_code == 200 and "token" in response.json()
        print_test("POST /auth/signup", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("POST /auth/signup", False, f"Error: {str(e)}")
        return False

def test_login():
    """Test user login and return token"""
    try:
        response = httpx.post(f"{BASE_URL}/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        passed = response.status_code == 200 and "token" in response.json()
        token = response.json().get("token") if passed else None
        print_test("POST /auth/login", passed, f"Status: {response.status_code}")
        return passed, token
    except Exception as e:
        print_test("POST /auth/login", False, f"Error: {str(e)}")
        return False, None

def test_get_me(token: str):
    """Test get current user"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get(f"{BASE_URL}/auth/me", headers=headers)
        passed = response.status_code == 200 and "username" in response.json()
        print_test("GET /auth/me", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("GET /auth/me", False, f"Error: {str(e)}")
        return False

def test_logout(token: str):
    """Test logout"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.post(f"{BASE_URL}/auth/logout", headers=headers)
        passed = response.status_code == 200
        print_test("POST /auth/logout", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("POST /auth/logout", False, f"Error: {str(e)}")
        return False

def test_get_leaderboard():
    """Test get leaderboard"""
    try:
        response = httpx.get(f"{BASE_URL}/leaderboard/")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        print_test("GET /leaderboard/", passed, f"Status: {response.status_code}, Entries: {len(response.json())}")
        return passed
    except Exception as e:
        print_test("GET /leaderboard/", False, f"Error: {str(e)}")
        return False

def test_get_leaderboard_filtered():
    """Test get leaderboard with filters"""
    try:
        response = httpx.get(f"{BASE_URL}/leaderboard/?mode=walls&limit=5")
        data = response.json()
        passed = response.status_code == 200 and isinstance(data, list) and len(data) <= 5
        print_test("GET /leaderboard/?mode=walls&limit=5", passed, f"Status: {response.status_code}, Entries: {len(data)}")
        return passed
    except Exception as e:
        print_test("GET /leaderboard/?mode=walls&limit=5", False, f"Error: {str(e)}")
        return False

def test_submit_score(token: str):
    """Test submit score"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.post(f"{BASE_URL}/leaderboard/", 
                             json={"score": 1234, "mode": "walls"},
                             headers=headers)
        passed = response.status_code == 200
        print_test("POST /leaderboard/", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("POST /leaderboard/", False, f"Error: {str(e)}")
        return False

def test_get_sessions():
    """Test get active sessions"""
    try:
        response = httpx.get(f"{BASE_URL}/sessions/")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        print_test("GET /sessions/", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("GET /sessions/", False, f"Error: {str(e)}")
        return False

def test_create_session(token: str):
    """Test create session and return session ID"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.post(f"{BASE_URL}/sessions/",
                             json={"mode": "pass-through"},
                             headers=headers)
        passed = response.status_code == 200 and "id" in response.json()
        session_id = response.json().get("id") if passed else None
        print_test("POST /sessions/", passed, f"Status: {response.status_code}")
        return passed, session_id
    except Exception as e:
        print_test("POST /sessions/", False, f"Error: {str(e)}")
        return False, None

def test_get_session(session_id: str):
    """Test get session by ID"""
    try:
        response = httpx.get(f"{BASE_URL}/sessions/{session_id}")
        passed = response.status_code == 200 and response.json().get("id") == session_id
        print_test(f"GET /sessions/{session_id}", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test(f"GET /sessions/{{id}}", False, f"Error: {str(e)}")
        return False

def test_update_session(session_id: str, token: str):
    """Test update session score"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.put(f"{BASE_URL}/sessions/{session_id}",
                            json={"score": 500},
                            headers=headers)
        passed = response.status_code == 200
        print_test(f"PUT /sessions/{session_id}", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test(f"PUT /sessions/{{id}}", False, f"Error: {str(e)}")
        return False

def test_end_session(session_id: str, token: str):
    """Test end session"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.delete(f"{BASE_URL}/sessions/{session_id}",
                               headers=headers)
        passed = response.status_code == 200
        print_test(f"DELETE /sessions/{session_id}", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test(f"DELETE /sessions/{{id}}", False, f"Error: {str(e)}")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}Snake Arena API Verification{Colors.RESET}")
    print(f"{Colors.BLUE}Testing server at: {BASE_URL}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    results = []
    
    # Test basic endpoints
    print(f"{Colors.YELLOW}Testing Basic Endpoints{Colors.RESET}")
    results.append(test_root())
    print()

    # Test authentication
    print(f"{Colors.YELLOW}Testing Authentication{Colors.RESET}")
    results.append(test_signup())
    login_passed, token = test_login()
    results.append(login_passed)
    
    if token:
        results.append(test_get_me(token))
        results.append(test_logout(token))
        # Get a fresh token for other tests
        _, token = test_login()
    print()

    # Test leaderboard
    print(f"{Colors.YELLOW}Testing Leaderboard{Colors.RESET}")
    results.append(test_get_leaderboard())
    results.append(test_get_leaderboard_filtered())
    if token:
        results.append(test_submit_score(token))
    print()

    # Test sessions
    print(f"{Colors.YELLOW}Testing Sessions{Colors.RESET}")
    results.append(test_get_sessions())
    if token:
        session_passed, session_id = test_create_session(token)
        results.append(session_passed)
        if session_id:
            results.append(test_get_session(session_id))
            results.append(test_update_session(session_id, token))
            results.append(test_end_session(session_id, token))
    print()

    # Summary
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}Summary{Colors.RESET}")
    print(f"{Colors.GREEN}Passed: {passed}/{total}{Colors.RESET}")
    if failed > 0:
        print(f"{Colors.RED}Failed: {failed}/{total}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)
