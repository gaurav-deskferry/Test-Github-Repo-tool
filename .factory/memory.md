# Project memory

Notes the coding agents read before working here. Written by Loopferry when a run learns something,
and yours to edit, reorder or delete at any time.

## Gotchas

- Sandbox cannot reach cdn.jsdelivr.net, so FastAPI /docs does not render in a browser unless CDN requests are intercepted (e.g. Playwright route to npm swagger-ui-dist). System python has no pip/venv; bootstrap pip from a wheel via files.pythonhosted.org.
- tests/conftest.py must set DATABASE_URL before importing app (settings are read at import time); startup runs Alembic migrations + seed, so schema changes need a new migration in alembic/versions.

## Conventions

- API routers are mounted under /api (app/main.py) because FastAPI also serves the built Vue SPA (frontend/dist) from / with an index.html fallback; unprefixed API routes would collide with SPA deep links like /characters/1.
