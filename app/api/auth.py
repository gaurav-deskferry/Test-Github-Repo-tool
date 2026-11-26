from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core import security
from app.models import User
from app.schemas import Credentials, Error, Token, UserOut

from .deps import DB, CurrentUser

router = APIRouter(prefix="/auth", tags=["auth"])
UNAUTH = {401: {"model": Error, "description": "Missing, invalid or expired token"}}


@router.post("/register", response_model=UserOut, status_code=201, summary="Create an account",
             responses={409: {"model": Error, "description": "Username already taken"}})
def register(body: Credentials, db: DB):
    if db.scalar(select(User).where(User.username == body.username)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")
    user = User(username=body.username, password_hash=security.hash_password(body.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:  # concurrent register with the same username
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")
    return user


@router.post("/login", response_model=Token, summary="Log in and get a JWT",
             description="OAuth2 password flow (form fields `username`, `password`). Used by the Swagger **Authorize** button.",
             responses={401: {"model": Error, "description": "Wrong username or password"}})
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB) -> Token:
    user = db.scalar(select(User).where(User.username == form.username))
    if not user or not security.verify_password(form.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    return Token(access_token=security.create_token(user.id, user.username))


@router.get("/me", response_model=UserOut, summary="Current user", responses=UNAUTH)
def me(user: CurrentUser):
    return user
