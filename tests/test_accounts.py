import uuid


def make_name():
    return f"test_{uuid.uuid4().hex[:8]}"


def test_create_account_ok(client):
    r = client.post("/accounts", json={"name": make_name()})
    assert r.status_code == 201
    assert isinstance(r.json()["id"], int)


def test_create_account_conflict(client):
    name = make_name()
    client.post("/accounts", json={"name": name})
    r = client.post("/accounts", json={"name": name})
    assert r.status_code == 409
