from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_health():
    res = client.get("/")
    assert res.status_code == 200


def test_create_ticket():
    res = client.post(
        "/tickets",
        json={
            "customer_name": "Sawsan",
            "title": "Test Issue",
            "description": "Something is broken",
            "priority": "High",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test Issue"


def test_ticket_not_found():
    res = client.get("/tickets/invalid-id")
    assert res.status_code == 404