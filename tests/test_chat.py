async def test_session_message_history(async_client):
    r = await async_client.post("/auth/register", json={"username": "bob", "password": "secret123"})
    assert r.status_code == 200
    token = (await async_client.post("/auth/login", json={"username": "bob", "password": "secret123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    s = await async_client.post("/chat/session", headers=headers)
    assert s.status_code == 200
    session_id = s.json()["session_id"]
    m = await async_client.post("/chat/message", headers=headers, json={"session_id": session_id, "text": "привет"})
    assert m.status_code == 200
    h = await async_client.get(f"/chat/history/{session_id}", headers=headers)
    assert h.status_code == 200
    hist = h.json()
    assert hist["session_id"] == session_id
    assert len(hist["messages"]) == 2
    assert hist["messages"][0]["sender"] == "user"
    assert hist["messages"][1]["sender"] == "bot"
