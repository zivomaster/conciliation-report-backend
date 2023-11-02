from pydantic import BaseModel
from typing import Optional


class ConnectionTableSchema(BaseModel):
    name: Optional[str] = None
    key: Optional[str] = None
    isSelected: Optional[bool] = False


class FieldsTableSchema(BaseModel):
    key: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None


class TableDatabaseSchema(BaseModel):
    key: Optional[str] = None
    name: Optional[str] = None
    fields: Optional[list[FieldsTableSchema]]
