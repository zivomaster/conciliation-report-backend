from pydantic import BaseModel
from typing import Optional


class ConnectionTableSchema(BaseModel):
    name: Optional[str] = None
    key: Optional[str] = None
    isSelected: Optional[bool] = False