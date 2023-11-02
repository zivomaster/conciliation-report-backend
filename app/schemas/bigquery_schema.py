from pydantic import BaseModel, Field
from fastapi import UploadFile
from .msg import StringConnectionResponse
import uuid
from typing import Optional


class BigQuerySchemaAuth(BaseModel):
    id_connection: Optional[uuid.UUID] = None
    password: Optional[str] = None
    project_id: Optional[str] = None
    dataset_id: Optional[str] = None
    response: Optional[StringConnectionResponse]
