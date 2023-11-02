from pydantic import BaseModel
from typing import Optional


class Msg(BaseModel):
    msg: str


class MessageConnectionResponse(BaseModel):
    detail: str
    dialect: Optional[str] = ""


class StringConnectionResponse(BaseModel):
    message: Optional[MessageConnectionResponse] = None
    status: Optional[int] = None
