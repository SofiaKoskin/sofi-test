from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


class Item(APIModel):
    created_at: datetime
    description: str
    id: int
    name: str
    price: int
    updated_at: datetime


class ItemCreateResponse(APIModel):
    id: int


class ItemNameRequest(APIModel):
    name: str


class ItemRequest(APIModel):
    description: str = Field(
        min_length=3,
        max_length=100,
    )
    name: str
    price: int = Field(
        ge=0,
        le=1_000_000,
    )
