from pydantic import BaseModel, ConfigDict, Field


class CharacterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(examples=["Captain Mira"])
    emoji: str
    tagline: str
    description: str
    personality: list[str]
    greeting: str = Field(description="First message the character sends in a new chat.")
    tags: list[str]
