from pydantic import BaseModel
from typing import Optional


class TableColumnSchema(BaseModel):
    column_name: Optional[str] = None
    data_type: Optional[str] = None


class TableMetadataSchema(BaseModel):
    table_name: Optional[str] = None
    columns: list[TableColumnSchema]