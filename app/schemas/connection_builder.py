from pydantic import BaseModel
from typing import Optional, Dict


class ConnectionBuilderRDS(BaseModel):
    database: Optional[str] = None
    hostname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = 0


class ConnectionBuilderMongoDB(ConnectionBuilderRDS):
    pass


class ConnectionBuilderBigQuery(BaseModel):
    credentials: Optional[dict] = None
    project_id: Optional[str] = None
    dataset_id: Optional[str] = None


class MessageConnectionResponse(BaseModel):
    detail: str
    dialect: Optional[str] = ""


class StringConnectionResponse(BaseModel):
    message: Optional[MessageConnectionResponse] = None
    status: Optional[int] = None
