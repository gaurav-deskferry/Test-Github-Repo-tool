from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm

from . import auth
from .schemas import Character, ChatSession, ChatSessionSummary, Credentials, Error, Token, User
from .store import CHARACTERS, DEMO_PASSWORD, DEMO_USER, store

DESCRIPTION = """
API for browsing **AI Character cards** and your own **chat sessions**.

## Quick start
1. Click **Authorize** (top right) and log in with `demo` / `demo1234`
   (or create an account with `POST /auth/register`).
2. Call **GET /characters** (public) and **GET /sessions** (requires login).

Auth is JWT (HS256) sent as `Authorization: Bearer <token>`.
"""

TAGS = [
    {"name": "auth", "description": "Register, log in and inspect the current user."},
    {"name": "characters", "description": "AI Character cards. Public."},
    {"name": "sessions", "description": "The logged-in user's chat sessions. **Requires JWT.**"},
]

UNAUTH = {401: {"model": Error, "description": "Missing, invalid or expired token"}}


def _create_user(username: str, password: str) -> User:
    user = User(id=len(store.users) + 1, username=username)
    store.users[username] = {"id": user.id, "username": username, "password_hash": auth.hash_password(password)}
    return user


@asynccontextmanager
async def lifespan(_: FastAPI):
    if DEMO_USER not in store.users:
        store.seed(_create_user(DEMO_USER, DEMO_PASSWORD).id)
    yield


app = FastAPI(title="AI Character Cards API", version="0.1.0", description=DESCRIPTION,
              openapi_tags=TAGS, lifespan=lifespan)


@app.post("/auth/register", response_model=User, status_code=201, tags=["auth"], summary="Create an account",
          responses={409: {"model": Error, "description": "Username already taken"}})
def register(body: Credentials) -> User:
    if body.username in store.users:
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")
    return _create_user(body.username, body.password)


@app.post("/auth/login", response_model=Token, tags=["auth"], summary="Log in and get a JWT",
          description="OAuth2 password flow (form fields `username`, `password`). Used by the Swagger **Authorize** button.",
          responses={401: {"model": Error, "description": "Wrong username or password"}})
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = auth.authenticate(form.username, form.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    return Token(access_token=auth.create_token(user))


@app.get("/auth/me", response_model=User, tags=["auth"], summary="Current user", responses=UNAUTH)
def me(user: auth.CurrentUser) -> User:
    return user


@app.get("/characters", response_model=list[Character], tags=["characters"], summary="List character cards")
def list_characters(tag: Annotated[str | None, Query(description="Only characters with this tag")] = None):
    return [c for c in CHARACTERS.values() if tag is None or tag in c.tags]


@app.get("/characters/{character_id}", response_model=Character, tags=["characters"], summary="Get a character card",
         responses={404: {"model": Error, "description": "Character not found"}})
def get_character(character_id: int):
    if character_id not in CHARACTERS:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Character not found")
    return CHARACTERS[character_id]


@app.get("/sessions", response_model=list[ChatSessionSummary], tags=["sessions"],
         summary="List my chat sessions", responses=UNAUTH)
def list_sessions(user: auth.CurrentUser, character_id: Annotated[int | None, Query(description="Filter by character")] = None):
    return [
        ChatSessionSummary(**s.model_dump(exclude={"messages"}), message_count=len(s.messages))
        for owner, s in store.sessions.values()
        if owner == user.id and (character_id is None or s.character_id == character_id)
    ]


@app.get("/sessions/{session_id}", response_model=ChatSession, tags=["sessions"], summary="Get one of my chat sessions",
         responses={**UNAUTH, 404: {"model": Error, "description": "Session not found (or not yours)"}})
def get_session(session_id: int, user: auth.CurrentUser):
    entry = store.sessions.get(session_id)
    if not entry or entry[0] != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")
    return entry[1]
