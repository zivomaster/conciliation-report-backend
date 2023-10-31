from pydantic import BaseModel, Field
from fastapi import UploadFile
import uuid
from typing import Optional


class DatabaseConnectionBase(BaseModel):
    connectionName: Optional[str] = None
    hostname: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    isFile: Optional[bool] = False
    file: Optional[str] = None
    separator: Optional[str] = None
    connectorId: Optional[int] = None
    userId: Optional[uuid.UUID] = None

# Properties to receive via API on creation


class DatabaseConnectionCreate(DatabaseConnectionBase):
    id: Optional[str] = None
    currentUser: Optional[str] = None


class DatabaseConnectionUpdate(DatabaseConnectionBase):
    password: Optional[str] = None


class DatabaseConnectionSchema(DatabaseConnectionBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        orm_mode = True
