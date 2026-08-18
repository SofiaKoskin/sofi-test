from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class User(APIModel):
    age: int
    birth_date: datetime
    email: str
    gender: Gender
    id: int
    interests: list[str]
    name: str
    phone: str


class UserCreateResponse(APIModel):
    id: int


class UserNameRequest(APIModel):
    name: str


class UserRequest(APIModel):
    age: int = Field(
        ge=18,
        le=100,
    )
    birth_date: datetime
    email: str
    gender: Gender
    interests: list[str]
    name: str
    phone: str
