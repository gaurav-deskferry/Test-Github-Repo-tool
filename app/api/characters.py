from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from app.models import Character
from app.schemas import CharacterOut, Error

from .deps import DB

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("", response_model=list[CharacterOut], summary="List character cards")
def list_characters(db: DB, tag: Annotated[str | None, Query(description="Only characters with this tag")] = None):
    rows = db.scalars(select(Character).order_by(Character.id)).all()
    return [c for c in rows if tag is None or tag in c.tags]


@router.get("/{character_id}", response_model=CharacterOut, summary="Get a character card",
            responses={404: {"model": Error, "description": "Character not found"}})
def get_character(character_id: int, db: DB):
    character = db.get(Character, character_id)
    if not character:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Character not found")
    return character
