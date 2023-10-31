from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str


class Token(BaseModel):
    accessToken: str
    tokenType: str


class LoginResponse(BaseModel):
    user: User
    auth: Token


class TokenPayload(BaseModel):
    sub: Optional[str] = None
