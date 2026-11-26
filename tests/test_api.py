from fastapi.testclient import TestClient

from app.main import app


def login(c, u="demo", p="demo1234"):
    return c.post("/auth/login", data={"username": u, "password": p})


def hdr(c, **kw):
    return {"Authorization": "Bearer " + login(c, **kw).json()["access_token"]}


def test_flow():
    with TestClient(app) as c:
        assert len(c.get("/characters").json()) == 3
        assert [x["id"] for x in c.get("/characters", params={"tag": "noir"}).json()] == [3]
        assert c.get("/characters/99").status_code == 404

        assert c.get("/sessions").status_code == 401
        assert login(c, p="wrongwrong").status_code == 401
        h = hdr(c)
        assert c.get("/auth/me", headers=h).json()["username"] == "demo"
        sessions = c.get("/sessions", headers=h).json()
        assert [s["message_count"] for s in sessions] == [3, 2]
        assert len(c.get("/sessions", headers=h, params={"character_id": 2}).json()) == 1
        assert len(c.get("/sessions/1", headers=h).json()["messages"]) == 3


def test_register_and_isolation():
    with TestClient(app) as c:
        assert c.post("/auth/register", json={"username": "bob", "password": "password1"}).status_code == 201
        assert c.post("/auth/register", json={"username": "bob", "password": "password1"}).status_code == 409
        h = hdr(c, u="bob", p="password1")
        assert c.get("/sessions", headers=h).json() == []
        assert c.get("/sessions/1", headers=h).status_code == 404


def test_bad_token():
    with TestClient(app) as c:
        assert c.get("/auth/me", headers={"Authorization": "Bearer junk"}).status_code == 401
