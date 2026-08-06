
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class APIModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


class ItemBase(APIModel):
    name: str
    description: str
    price: str


class ItemCreate(ItemBase):
    pass



class ItemUpdate(ItemBase):
    pass


class Item(ItemCreate):
    id: int
    created_at: datetime
    updated_at: datetime