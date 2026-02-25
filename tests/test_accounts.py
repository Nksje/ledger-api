import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def make_name():
    return f"test_{uuid.uuid4().hex[:8]}"

def test_create_account_ok():
    r = client.post("/accounts", json={"name": make_name()})
    assert r.status_code == 201
    data = r.json()
    assert isinstance(data["id"], int)

def test_create_account_conflict():
    name = make_name()
    client.post("/accounts", json={"name": name})
    r = client.post("/accounts", json={"name": name})
    assert r.status_code == 409
