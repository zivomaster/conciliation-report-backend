from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import json

from app import crud, schemas, models
from app.api import deps
from app.core.config import settings
from app.services.AWS_handled_files import s3_search
from app.utils import get_array_list_tables, update_selected_tables
# from app.schemas.user import User, UserCreate, UserUpdate
router = APIRouter()


@router.get("/", response_model=List[schemas.ConnectionTableSchema])
def list_connections_table(
    db: Session = Depends(deps.get_db),
    id: Optional[uuid.UUID] = None
) -> Any:
    """
    Retrieve schemas table
    """
    # get connection details
    connection = crud.database_connections.get_connection_by_id(db, id=id)

    # check if exist in bucket
    key = str(connection.id)+'.json'
    isExist = s3_search(key=key,
                        path=settings.BUCKET_PATH_TABLES_SELECTED)
    if isExist:
        # isSelected
        response = get_array_list_tables(
            key=connection.file, id_conn=str(connection.id), isExist=isExist)
        return response
    else:
        # full
        response = get_array_list_tables(
            key=connection.file, id_conn=str(connection.id))
        return response


@router.post("-selected/", response_model=List[schemas.ConnectionTableSchema])
def select_tables(
    db: Session = Depends(deps.get_db),
    id: Optional[uuid.UUID] = None,
    selected_tables: Optional[list[str]] = None
) -> Any:
    """
    Update selected tables
    """ 
    # get connection details
    connection = crud.database_connections.get_connection_by_id(db, id=id)

    # check if exist in bucket
    key = str(connection.id)+'.json'
    isExist = s3_search(key=key,
                        path=settings.BUCKET_PATH_TABLES_SELECTED)
    if isExist:
        response = update_selected_tables(
            key=key, selectedTables=selected_tables)
        return response
    else:
        # full
        response = get_array_list_tables(
            key=connection.file, id_conn=str(connection.id))
        return response
