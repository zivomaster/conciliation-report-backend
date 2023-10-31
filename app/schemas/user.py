from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_authenticated: Optional[bool] = False
    is_superuser: bool = False

# Properties to receive via API on creation


class UserCreate(UserBase):
    username: Optional[str] = None
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        orm_mode = True
