from fastapi.testclient import TestClient
from app.main import app


def test_ping(client):
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.json() == {"ping": "pong"}
