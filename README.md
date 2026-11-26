# AI Character Cards

FastAPI + SQLAlchemy/Alembic (SQLite) backend and a Vue 3 (Vite) frontend, run with [Bun](https://bun.sh).
Browse AI character cards, sign up, and chat. **Under development:** character replies are placeholders.
See [docs/FEATURE_PLAN.md](docs/FEATURE_PLAN.md) for scope and user flows.

## Run

```bash
pip install -r requirements.txt
bun install
bun run dev        # API on :8000 and Vite on :5173, in parallel -> open http://localhost:5173
```

The DB (`data/app.db`) is created, migrated (Alembic) and seeded on API startup.
`bun run dev` sets `SEED_DEMO=1`, which creates a dev-only login `demo` / `demo1234` (never enabled by default; leave `SEED_DEMO` unset in production and set `JWT_SECRET`). Swagger UI: http://localhost:8000/docs

Single-origin (production-like): `bun run build`, then `uvicorn app.main:app` serves the SPA at http://localhost:8000.

## Test

```bash
bun run test       # pytest + vitest in parallel
```

## Database

```bash
alembic upgrade head                           # (also done automatically on startup)
alembic revision --autogenerate -m "message"   # after changing app/models
python -m app.db.seed                          # re-run seed (idempotent)
```

Env: `DATABASE_URL` (default `sqlite:///data/app.db`), `JWT_SECRET` (set in production), `JWT_TTL_MINUTES` (60), `SEED_DEMO` (`0` disables seeding).

## API (all under `/api`)

| Endpoint | Auth | Description |
|---|---|---|
| `POST /api/auth/register` | – | create account |
| `POST /api/auth/login` | – | form login → JWT |
| `GET /api/auth/me` | JWT | current user |
| `GET /api/characters`, `/api/characters/{id}` | – | character cards (`?tag=`) |
| `GET/POST /api/sessions`, `GET/DELETE /api/sessions/{id}` | JWT | your chat sessions (`?character_id=`) |
| `POST /api/sessions/{id}/messages` | JWT | send message, get placeholder reply |
