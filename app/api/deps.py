from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login", description="Log in via `/api/auth/login`, or use `demo` / `demo1234`.")

DB = Annotated[Session, Depends(get_db)]


def current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DB) -> User:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED, "Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    try:
        user_id = decode_token(token)
    except (jwt.PyJWTError, KeyError, ValueError):
        raise unauthorized
    user = db.get(User, user_id)
    if not user:
        raise unauthorized
    return user


CurrentUser = Annotated[User, Depends(current_user)]
