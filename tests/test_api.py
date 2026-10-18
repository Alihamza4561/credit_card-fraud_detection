import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def get_auth_token(client):
    response = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={
            "username": settings.ADMIN_USERNAME,
            "password": settings.ADMIN_PASSWORD,
        },
    )
    return response.json()["access_token"]


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True


def test_auth_failure(client):
    response = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": "wrong", "password": "user"},
    )
    assert response.status_code == 401


def test_unauthorized_inference(client):
    payload = {"amount": 100.0, "v_features": [0.0] * 28}
    response = client.post(
        f"{settings.API_V1_STR}/transactions/evaluate", json=payload
    )
    assert response.status_code == 401


def test_successful_inference(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"amount": 5000.0, "v_features": [1.5] * 28}

    response = client.post(
        f"{settings.API_V1_STR}/transactions/evaluate",
        json=payload,
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "is_fraud" in data
    assert "fraud_probability" in data
    assert "status" in data