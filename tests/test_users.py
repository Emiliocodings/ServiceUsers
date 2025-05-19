import pytest
from httpx import AsyncClient
from app.main import app

pytestmark = pytest.mark.asyncio

async def test_create_user(client):
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "User",
        "role": "user",
        "active": True
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data

async def test_create_user_duplicate_email(client, test_user):
    user_data = {
        "username": "anotheruser",
        "email": test_user.email,  # Using existing email
        "first_name": "Another",
        "last_name": "User",
        "role": "user",
        "active": True
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

async def test_read_users(client, test_user):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["username"] == test_user.username

async def test_read_user(client, test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email

async def test_read_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

async def test_update_user(client, test_user):
    update_data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    response = client.put(f"/users/{test_user.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["username"] == test_user.username  # Unchanged field

async def test_update_user_not_found(client):
    update_data = {"first_name": "Updated"}
    response = client.put("/users/999", json=update_data)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

async def test_delete_user(client, test_user):
    response = client.delete(f"/users/{test_user.id}")
    assert response.status_code == 204

    # Verify user is deleted
    get_response = client.get(f"/users/{test_user.id}")
    assert get_response.status_code == 404

async def test_delete_user_not_found(client):
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

async def test_create_user_validation(client):
    # Test invalid email
    invalid_user = {
        "username": "testuser",
        "email": "invalid-email",
        "first_name": "Test",
        "last_name": "User",
        "role": "user"
    }
    response = client.post("/users/", json=invalid_user)
    assert response.status_code == 422

    # Test invalid role
    invalid_user = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "invalid_role"
    }
    response = client.post("/users/", json=invalid_user)
    assert response.status_code == 422

    # Test username too short
    invalid_user = {
        "username": "te",  # Too short
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "user"
    }
    response = client.post("/users/", json=invalid_user)
    assert response.status_code == 422 