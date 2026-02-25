import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def make_account():
    r = client.post("/accounts", json={"name": f"acc_{uuid.uuid4().hex[:8]}"})
    return r.json()["id"]


def test_create_entry_ok():
    acc1 = make_account()
    acc2 = make_account()

    r = client.post("/entries", json={
        "description": "Initial deposit",
        "lines": [
            {"account_id": acc1, "amount": "100.00", "type": "debit"},
            {"account_id": acc2, "amount": "100.00", "type": "credit"},
        ]
    })
    assert r.status_code == 201
    data = r.json()
    assert data["description"] == "Initial deposit"
    assert len(data["lines"]) == 2


def test_create_entry_unbalanced():
    acc1 = make_account()
    acc2 = make_account()

    r = client.post("/entries", json={
        "description": "Bad entry",
        "lines": [
            {"account_id": acc1, "amount": "100.00", "type": "debit"},
            {"account_id": acc2, "amount": "50.00", "type": "credit"},
        ]
    })
    assert r.status_code == 422
