from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException

from app.api import auth, characters, sessions
from app.core.config import ROOT, settings
from app.db.seed import seed
from app.db.session import SessionLocal

DESCRIPTION = """
API for browsing **AI Character cards** and your own **chat sessions** (SQLite via SQLAlchemy + Alembic).

## Quick start
1. Click **Authorize** (top right) and log in with `demo` / `demo1234`
   (or create an account with `POST /api/auth/register`).
2. Call **GET /api/characters** (public) and **GET /api/sessions** (requires login).

Auth is JWT (HS256) sent as `Authorization: Bearer <token>`.
"""

TAGS = [
    {"name": "auth", "description": "Register, log in and inspect the current user."},
    {"name": "characters", "description": "AI Character cards. Public."},
    {"name": "sessions", "description": "The logged-in user's chat sessions. **Requires JWT.**"},
]


def migrate() -> None:
    cfg = Config(str(ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(ROOT / "alembic"))
    command.upgrade(cfg, "head")


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.database_url.startswith("sqlite:///"):
        from pathlib import Path
        Path(settings.database_url.removeprefix("sqlite:///")).parent.mkdir(parents=True, exist_ok=True)
    migrate()
    if settings.seed_demo:
        with SessionLocal() as db:
            seed(db)
    yield


app = FastAPI(title="AI Character Cards API", version="0.2.0", description=DESCRIPTION,
              openapi_tags=TAGS, lifespan=lifespan)
for r in (auth.router, characters.router, sessions.router):
    app.include_router(r, prefix="/api")



class SPAStaticFiles(StaticFiles):
    """Static files that fall back to index.html so Vue-router deep links survive a reload."""

    async def get_response(self, path, scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException as exc:
            if exc.status_code == 404 and not path.startswith("api/"):
                return await super().get_response("index.html", scope)
            raise


# Serve the built Vue app (`bun run build`) from the same origin, if present.
# Mounted last so API routes win.
if settings.frontend_dist.is_dir():
    app.mount("/", SPAStaticFiles(directory=settings.frontend_dist, html=True), name="frontend")
