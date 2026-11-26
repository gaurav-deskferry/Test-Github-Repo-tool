from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: Literal["user", "character"]
    content: str
    created_at: datetime


class ChatSessionCreate(BaseModel):
    character_id: int
    title: str | None = Field(default=None, max_length=120, description="Defaults to `Chat with <name>`.")


class ChatSessionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    character_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int


class ChatSessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    character_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageOut]
