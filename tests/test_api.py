import pytest

# Test 1: Happy Path - User Registration
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "hashed_password": "testpassword", "is_admin": False}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

# Test 2: Happy Path - Login & JWT Token
def test_login_and_token(client):
    # First, register
    client.post(
        "/auth/register",
        json={"username": "loginuser", "hashed_password": "password123", "is_admin": False}
    )
    # Then, login
    response = client.post(
        "/auth/token",
        data={"username": "loginuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test 3: Integration Test - AI Suggest Stub
def test_ai_suggest_stub(client):
    # Register and Login to get token
    client.post("/auth/register", json={"username": "aiuser", "hashed_password": "password", "is_admin": False})
    login_res = client.post("/auth/token", data={"username": "aiuser", "password": "password"})
    token = login_res.json()["access_token"]
    
    # Requirement: Test the /ai/suggest STUB specifically
    response = client.get(
        "/ai/suggest?title=Build%20Login&stub=true",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "STUB:" in response.json()["suggested_description"]
    assert response.json()["mode"] == "stub"