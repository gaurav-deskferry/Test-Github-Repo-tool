"""scrypt password hashing + HS256 JWTs."""
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt

from .config import settings

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return salt.hex() + "$" + digest.hex()


def verify_password(password: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split("$")
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
    return hmac.compare_digest(digest.hex(), digest_hex)


def create_token(user_id: int, username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": str(user_id), "username": username, "iat": now,
               "exp": now + timedelta(minutes=settings.jwt_ttl_minutes)}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str) -> int:
    """Return the user id or raise jwt.PyJWTError / KeyError / ValueError."""
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    return int(payload["sub"])
