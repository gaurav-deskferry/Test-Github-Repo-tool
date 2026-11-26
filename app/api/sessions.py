from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy import select

from app.db.base import utcnow
from app.models import Character, ChatSession, Message
from app.schemas import ChatSessionCreate, ChatSessionOut, ChatSessionSummary, Error, MessageCreate, MessageOut
from app.services import stub_reply

from .deps import DB, CurrentUser

router = APIRouter(prefix="/sessions", tags=["sessions"])
UNAUTH = {401: {"model": Error, "description": "Missing, invalid or expired token"}}
NOT_FOUND = {404: {"model": Error, "description": "Session not found (or not yours)"}}


def _own_session(db, session_id: int, user_id: int) -> ChatSession:
    session = db.get(ChatSession, session_id)
    if not session or session.user_id != user_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")
    return session


@router.get("", response_model=list[ChatSessionSummary], summary="List my chat sessions", responses=UNAUTH)
def list_sessions(user: CurrentUser, db: DB,
                  character_id: Annotated[int | None, Query(description="Filter by character")] = None):
    q = select(ChatSession).where(ChatSession.user_id == user.id).order_by(ChatSession.id)
    if character_id is not None:
        q = q.where(ChatSession.character_id == character_id)
    return db.scalars(q).all()


@router.post("", response_model=ChatSessionOut, status_code=201, summary="Start a chat with a character",
             responses={**UNAUTH, 404: {"model": Error, "description": "Character not found"}})
def create_session(body: ChatSessionCreate, user: CurrentUser, db: DB):
    character = db.get(Character, body.character_id)
    if not character:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Character not found")
    session = ChatSession(user_id=user.id, character_id=character.id,
                          title=body.title or f"Chat with {character.name}")
    session.messages.append(Message(role="character", content=character.greeting))
    db.add(session)
    db.commit()
    return session


@router.get("/{session_id}", response_model=ChatSessionOut, summary="Get one of my chat sessions",
            responses={**UNAUTH, **NOT_FOUND})
def get_session(session_id: int, user: CurrentUser, db: DB):
    return _own_session(db, session_id, user.id)


@router.post("/{session_id}/messages", response_model=list[MessageOut], status_code=201,
             summary="Send a message", responses={**UNAUTH, **NOT_FOUND},
             description="Stores your message and returns `[your message, character reply]`. "
                         "**Under development:** replies are canned placeholders, not a real AI model yet.")
def send_message(session_id: int, body: MessageCreate, user: CurrentUser, db: DB):
    session = _own_session(db, session_id, user.id)
    character = db.get(Character, session.character_id)
    mine = Message(role="user", content=body.content.strip())
    reply = Message(role="character", content=stub_reply(character, body.content))
    session.messages.extend([mine, reply])
    session.updated_at = utcnow()
    db.commit()
    return [mine, reply]


@router.delete("/{session_id}", status_code=204, summary="Delete a chat session", responses={**UNAUTH, **NOT_FOUND})
def delete_session(session_id: int, user: CurrentUser, db: DB):
    db.delete(_own_session(db, session_id, user.id))
    db.commit()
    return Response(status_code=204)
