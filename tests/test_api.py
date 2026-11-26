from sqlalchemy import inspect

from app.db.session import engine
from tests.conftest import auth


def test_migrated_and_seeded(client):
    assert {"users", "characters", "chat_sessions", "messages", "alembic_version"} <= set(inspect(engine).get_table_names())
    assert len(client.get("/api/characters").json()) == 6


def test_characters(client):
    assert [x["name"] for x in client.get("/api/characters", params={"tag": "noir"}).json()] == ["Detective Noir"]
    assert client.get("/api/characters/999").status_code == 404


def test_seeded_demo_sessions(client):
    assert client.get("/api/sessions").status_code == 401
    assert client.post("/api/auth/login", data={"username": "demo", "password": "wrongwrong"}).status_code == 401
    h = auth(client)
    assert client.get("/api/auth/me", headers=h).json()["username"] == "demo"
    assert [s["message_count"] for s in client.get("/api/sessions", headers=h).json()][:2] == [3, 2]
    assert len(client.get("/api/sessions", headers=h, params={"character_id": 2}).json()) == 1
    assert len(client.get("/api/sessions/1", headers=h).json()["messages"]) == 3


def test_register_and_isolation(client):
    body = {"username": "bob", "password": "password1"}
    assert client.post("/api/auth/register", json=body).status_code == 201
    assert client.post("/api/auth/register", json=body).status_code == 409
    h = auth(client, "bob", "password1")
    assert client.get("/api/sessions", headers=h).json() == []
    assert client.get("/api/sessions/1", headers=h).status_code == 404
    assert client.delete("/api/sessions/1", headers=h).status_code == 404


def test_chat_lifecycle(client):
    client.post("/api/auth/register", json={"username": "carol", "password": "password1"})
    h = auth(client, "carol", "password1")
    assert client.post("/api/sessions", headers=h, json={"character_id": 999}).status_code == 404
    s = client.post("/api/sessions", headers=h, json={"character_id": 1}).json()
    assert s["title"] == "Chat with Captain Mira" and len(s["messages"]) == 1
    assert client.post(f"/api/sessions/{s['id']}/messages", headers=h, json={"content": ""}).status_code == 422
    pair = client.post(f"/api/sessions/{s['id']}/messages", headers=h, json={"content": "Hello there"}).json()
    assert [m["role"] for m in pair] == ["user", "character"]
    assert client.get(f"/api/sessions/{s['id']}", headers=h).json()["messages"][-1]["role"] == "character"
    assert client.get("/api/sessions", headers=h).json()[0]["message_count"] == 3
    assert client.delete(f"/api/sessions/{s['id']}", headers=h).status_code == 204
    assert client.get(f"/api/sessions/{s['id']}", headers=h).status_code == 404


def test_bad_token(client):
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer junk"}).status_code == 401


def test_register_duplicate_is_409(client):
    body = {"username": "dupe_user", "password": "password123"}
    assert client.post("/api/auth/register", json=body).status_code == 201
    assert client.post("/api/auth/register", json=body).status_code == 409
