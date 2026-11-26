from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(description="JWT to send as `Authorization: Bearer <token>`.")
    token_type: Literal["bearer"] = "bearer"


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[A-Za-z0-9_.-]+$", examples=["alice"])
    password: str = Field(min_length=8, max_length=128, examples=["s3cret-pass"])


class User(BaseModel):
    id: int
    username: str


class Character(BaseModel):
    id: int
    name: str = Field(examples=["Captain Mira"])
    tagline: str
    description: str
    personality: list[str]
    greeting: str = Field(description="First message the character sends in a new chat.")
    tags: list[str]


class Message(BaseModel):
    role: Literal["user", "character"]
    content: str
    created_at: datetime


class ChatSession(BaseModel):
    id: int
    character_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[Message]


class ChatSessionSummary(BaseModel):
    id: int
    character_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int


class Error(BaseModel):
    detail: str
