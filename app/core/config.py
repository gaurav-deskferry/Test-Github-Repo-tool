import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    # SQLite file by default; override with DATABASE_URL (any SQLAlchemy URL).
    database_url: str = field(default_factory=lambda: os.environ.get("DATABASE_URL") or f"sqlite:///{ROOT / 'data' / 'app.db'}")
    # Set JWT_SECRET in production. A random per-process secret is used otherwise.
    jwt_secret: str = field(default_factory=lambda: os.environ.get("JWT_SECRET") or secrets.token_urlsafe(32))
    jwt_ttl_minutes: int = field(default_factory=lambda: int(os.environ.get("JWT_TTL_MINUTES", "60")))
    seed_demo: bool = field(default_factory=lambda: os.environ.get("SEED_DEMO", "1") != "0")
    frontend_dist: Path = ROOT / "frontend" / "dist"


settings = Settings()
