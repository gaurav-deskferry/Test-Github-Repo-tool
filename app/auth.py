"""Lightweight JWT auth: scrypt password hashing + HS256 tokens."""
import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .schemas import User
from .store import store

# Set JWT_SECRET in production. A random per-process secret is used otherwise
# (tokens are then invalidated on restart).
SECRET_KEY = os.environ.get("JWT_SECRET") or secrets.token_urlsafe(32)
ALGORITHM = "HS256"
TOKEN_TTL_MINUTES = int(os.environ.get("JWT_TTL_MINUTES", "60"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", description="Log in via `/auth/login`, or use `demo` / `demo1234`.")


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return salt.hex() + "$" + digest.hex()


def verify_password(password: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split("$")
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
    return hmac.compare_digest(digest.hex(), digest_hex)


def create_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": str(user.id), "username": user.username, "iat": now,
               "exp": now + timedelta(minutes=TOKEN_TTL_MINUTES)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate(username: str, password: str) -> User | None:
    record = store.users.get(username)
    if record and verify_password(password, record["password_hash"]):
        return User(id=record["id"], username=record["username"])
    return None


def current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED, "Invalid or expired token", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise unauthorized
    for record in store.users.values():
        if record["id"] == user_id:
            return User(id=record["id"], username=record["username"])
    raise unauthorized


CurrentUser = Annotated[User, Depends(current_user)]
