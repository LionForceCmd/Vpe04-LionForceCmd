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


def test_convert_ok() -> None:
    response = client.get("/convert", params={"time": "14:30", "city": "Europe/Moscow"})
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == {"time": "14:30", "city": "Europe/Moscow"}
    assert body["target"]["time"] == "11:30"


def test_convert_bad_time_format() -> None:
    response = client.get("/convert", params={"time": "25:99", "city": "UTC"})
    assert response.status_code == 400


def test_convert_unknown_city() -> None:
    response = client.get("/convert", params={"time": "10:00", "city": "Nowhere/Nothing"})
    assert response.status_code == 400


def test_openapi_available() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/convert" in response.json()["paths"]
