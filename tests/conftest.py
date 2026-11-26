import os
import tempfile

# Must be set before `app` is imported: a throwaway SQLite file per test run.
_tmp = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp.name}/test.db"
os.environ["JWT_SECRET"] = "test-secret-test-secret-test-secret-123"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


def auth(client, u="demo", p="demo1234"):
    r = client.post("/api/auth/login", data={"username": u, "password": p})
    return {"Authorization": "Bearer " + r.json()["access_token"]}
