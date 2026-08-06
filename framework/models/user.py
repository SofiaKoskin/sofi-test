from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr


class APIModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class UserBase(APIModel):
    name: str
    age: int
    interests: list[str] | None
    gender: str
    email: str
    phone: str
    birth_date: datetime


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
