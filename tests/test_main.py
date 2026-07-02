"""Tests for the FastAPI application"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 20
    data = response.json()
    assert data["message"] == "Hello, CI/CD!"
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_add():
    response = client.get("/add/3/5")
    assert response.status_code == 200
    assert response.json()["result"] == 8


def test_add_negative():
    response = client.get("/add/-1/10")
    assert response.status_code == 200
    assert response.json()["result"] == 9


def test_multiply():
    response = client.get("/multiply/4/6")
    assert response.status_code == 200
    assert response.json()["result"] == 24


def test_multiply_zero():
    response = client.get("/multiply/0/100")
    assert response.status_code == 200
    assert response.json()["result"] == 0


def test_add_invalid_input():
    response = client.get("/add/abc/5")
    assert response.status_code == 422  # FastAPI validation error
