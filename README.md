# AI Character Cards API

FastAPI app: list AI character cards and a user's chat sessions, with lightweight JWT auth.
Data is in-memory and seeded on startup (demo user `demo` / `demo1234`).

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload      # Swagger UI: http://localhost:8000/docs
pytest
```

| Endpoint | Auth | Description |
|---|---|---|
| `POST /auth/register` | – | create account |
| `POST /auth/login` | – | form login → JWT |
| `GET /auth/me` | JWT | current user |
| `GET /characters`, `/characters/{id}` | – | character cards (`?tag=`) |
| `GET /sessions`, `/sessions/{id}` | JWT | your chat sessions (`?character_id=`) |

Env: `JWT_SECRET` (set in production), `JWT_TTL_MINUTES` (default 60).
