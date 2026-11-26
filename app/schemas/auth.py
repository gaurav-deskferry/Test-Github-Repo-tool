from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str = Field(description="JWT to send as `Authorization: Bearer <token>`.")
    token_type: Literal["bearer"] = "bearer"


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[A-Za-z0-9_.-]+$", examples=["alice"])
    password: str = Field(min_length=8, max_length=128, examples=["s3cret-pass"])


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
