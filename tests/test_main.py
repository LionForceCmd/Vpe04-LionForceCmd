import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Добро пожаловать в Time Server API"


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.parametrize("path", ["/time", "/datetime", "/date"])
def test_time_endpoints(path: str) -> None:
    response = client.get(path)
    assert response.status_code == 200
    assert response.json()["timezone"] == "UTC"


def test_openapi_available() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/time" in response.json()["paths"]
