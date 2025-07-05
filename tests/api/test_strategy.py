import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from backend.database.database import Base, get_db
from backend.models import user_model, strategy_model
from backend.models import schemas  # Import Pydantic schemas

# Create a separate test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_quant_platform.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db for dependency injection
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create all tables for test DB
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

# Helper to register user with a unique username and email
def create_test_user(client, username_suffix=""):
    user_data = {
        "username": f"testuser{username_suffix}",
        "email": f"test{username_suffix}@example.com",
        "password": "testpassword"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    return response.json()

# Helper to login and get token for a specific user
def get_access_token(client, username_suffix=""):
    login_data = {
        "username": f"testuser{username_suffix}",
        "password": "testpassword"
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]

# Test for creating a strategy (successful case - public)
def test_create_strategy_public(client):
    user_data = create_test_user(client, "public")
    token = get_access_token(client, "public")

    strategy_data = {
        "name": "Public Test Strategy",
        "description": "A public test strategy",
        "parameters": {"sma_length": 20},
        "sharing_status": "public",
        "rental_fee": 5.0,
        "profit_sharing_percentage": 0.02,
        "category": "Momentum",
        "asset_types": ["crypto"]
    }

    response = client.post("/strategies/", json=strategy_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["sharing_status"] == "public"

# Test for creating a strategy (successful case - private)
def test_create_strategy_private(client):
    user_data = create_test_user(client, "private")
    token = get_access_token(client, "private")

    strategy_data = {
        "name": "Private Test Strategy",
        "description": "A private test strategy",
        "parameters": {"rsi_period": 14},
        "sharing_status": "private"
    }

    response = client.post("/strategies/", json=strategy_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["sharing_status"] == "private"

# Test for creating a strategy (successful case - rentable)
def test_create_strategy_rentable(client):
    user_data = create_test_user(client, "rentable")
    token = get_access_token(client, "rentable")

    strategy_data = {
        "name": "Rentable Test Strategy",
        "description": "A rentable test strategy",
        "parameters": {"bollinger_length": 20, "std_dev": 2},
        "sharing_status": "rentable",
        "rental_fee": 15.0
    }

    response = client.post("/strategies/", json=strategy_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["sharing_status"] == "rentable"
    assert pytest.approx(response.json()["rental_fee"]) == 15.0

# Test for creating a strategy without authentication
def test_create_strategy_unauthenticated(client):
    strategy_data = {
        "name": "Unauthorized Strategy",
        "parameters": {"some_param": "some_value"},
        "sharing_status": "private"
    }
    response = client.post("/strategies/", json=strategy_data)
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Not authenticated"

# Test for creating a strategy with invalid input (missing required fields)
def test_create_strategy_invalid_input(client):
    user_data = create_test_user(client, "invalid")
    token = get_access_token(client, "invalid")

    invalid_strategy_data = {
        "parameters": {"sma_length": 20},
        "sharing_status": "private"
        # Missing the 'name' field which is likely required
    }

    response = client.post("/strategies/", json=invalid_strategy_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422  # Expect Unprocessable Entity
    assert "detail" in response.json()
    # You might want to add more specific assertions about the error details
    # depending on how your FastAPI application handles validation.
    # For example, checking if the "name" field is mentioned in the errors.
    errors = response.json()["detail"]
    assert isinstance(errors, list)
    assert any(error["loc"] == ["body", "name"] for error in errors)
    assert any(error["msg"] == "field required" for error in errors)