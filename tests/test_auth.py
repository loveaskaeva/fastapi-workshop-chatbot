import pytest


async def test_register_and_login(async_client):
    r = await async_client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "alice"
    r2 = await async_client.post("/auth/login", json={"username": "alice", "password": "secret123"})
    assert r2.status_code == 200
    token = r2.json()["access_token"]
    assert isinstance(token, str) and len(token) > 10
