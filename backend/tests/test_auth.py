from fastapi.testclient import TestClient
from src.main import app
from src.services.auth_service import AuthService
from src.models.user import User
from src.schemas.user import UserCreate
from sqlalchemy.orm import Session
from src.database import get_db

client = TestClient(app)

def test_register_user():
    response = client.post("/api/v1/auth/register", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@example.com"

def test_login_user():
    response = client.post("/api/v1/auth/login", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user():
    response = client.post("/api/v1/auth/login", json={
        "email": "invaliduser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_register_existing_user():
    response = client.post("/api/v1/auth/register", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"