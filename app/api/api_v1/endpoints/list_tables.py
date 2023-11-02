from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import json

from app import crud, schemas, models
from app.api import deps
from app.core.config import settings
from app.services.AWS_handled_files import s3_download
# from app.schemas.user import User, UserCreate, UserUpdate
router = APIRouter()


@router.get("/", response_model=List[schemas.ConnectionTableSchema])
def list_connections_table(
    db: Session = Depends(deps.get_db),
    id: Optional[uuid.UUID] = None
) -> Any:
    """
    Retrieve connections table.
    """
    connection = crud.database_connections.get_connection_by_id(db, id=id)
    # check if exist in bucket

    # search file
    response = s3_download(key=connection.file,
                           path=settings.BUCKET_PATH_SAVE_CONNECTIONS)
    json_data = response['Body'].read().decode('utf-8')
    dict_data = json.loads(json_data)
    # get tables
    array_tables = dict_data["tables"]
    list_conn_table = []
    for tables in array_tables:
        schema = schemas.ConnectionTableSchema(name=tables["name"],
                                               key=tables["key"])
        list_conn_table.append(schema)
    return list_conn_table


@router.post("/", response_model=List[schemas.ConnectionTableSchema])
def select_tables(
    db: Session = Depends(deps.get_db),
    id: Optional[uuid.UUID] = None,
    tables: Optional[list[str]] = None
) -> Any:
    """
    Update isSelected field
    """
    connection = crud.database_connections.get_connection_by_id(db, id=id)
    # search file
    response = s3_download(key=connection.file,
                           path=settings.BUCKET_PATH_SAVE_CONNECTIONS)
    json_data = response['Body'].read().decode('utf-8')
    dict_data = json.loads(json_data)
    # get tables
    array_tables = dict_data["tables"]
    list_conn_table = []
    for tables in array_tables:
        schema = schemas.ConnectionTableSchema(name=tables["name"],
                                               key=tables["key"])
        list_conn_table.append(schema)
    return list_conn_table
