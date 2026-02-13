from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate
import pytest

# Setup for testing
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    # Create the database and the database table
    from ..database import Base
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

def test_create_user(client, db):
    user_data = {"email": "test@example.com", "password": "password"}
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]

def test_read_user(client, db):
    response = client.get("/api/v1/users/test@example.com")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_update_user(client, db):
    update_data = {"email": "test@example.com", "password": "newpassword"}
    response = client.put("/api/v1/users/test@example.com", json=update_data)
    assert response.status_code == 200
    assert response.json()["email"] == update_data["email"]

def test_delete_user(client, db):
    response = client.delete("/api/v1/users/test@example.com")
    assert response.status_code == 204
    response = client.get("/api/v1/users/test@example.com")
    assert response.status_code == 404