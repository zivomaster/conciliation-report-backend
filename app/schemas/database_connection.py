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


class AuthMethodSchema(BaseModel):
    label: Optional[str]
    type: Optional[str]


class DatabaseConnectionCreate(DatabaseConnectionBase):
    id: Optional[str] = None
    currentUser: Optional[str] = None


class DatabaseConnectionUpdate(DatabaseConnectionBase):
    password: Optional[str] = None


class DatabaseConnectionSchema(DatabaseConnectionBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        orm_mode = True


class ConnectorTypeModelSchema(BaseModel):
    contype_id: int
    label: str
    thumbnail_url: str
    type_id: int
    auth_meth_id: Optional[int] = None


class ConnectorSchema(BaseModel):
    id: Optional[int]
    label: str
    thumbnailUrl: Optional[str]
    type: str
    authenticationMethods: Optional[list[AuthMethodSchema]] = []


class DatabaseConnectionListSchema(BaseModel):
    id:  uuid.UUID
    connectionName: str
    database: Optional[str]
    hostname: Optional[str]
    port: Optional[str]
    connector: ConnectorSchema
    isFile: Optional[bool] = False
