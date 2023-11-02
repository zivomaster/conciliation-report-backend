# typing
from typing import Any, List
# fastAPI
from fastapi import APIRouter, HTTPException, Depends, status
# sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# TODO app
from app import crud, schemas, models
from app.api import deps
from app.core.config import settings
from app.core import security
from app.services import database_connections_handlers as conn_handler
from app import utils

import json
# cryptography
router = APIRouter()


@router.post("/", response_model=schemas.DatabaseConnectionListSchema)
async def save_connection(
    payload: schemas.DatabaseConnectionCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Save and Update connections
    """
    sch_DCL = schemas.DatabaseConnectionListSchema()
    # get payload
    format_out = None
    # check if connection exists
    if payload.id is not None and payload.id != "":
        obj = crud.database_connections.get_connection_by_id(db, payload.id)

        update_conn_object = crud.database_connections.save_or_update_connection_db(
            db=db, payload=payload, db_update=obj, isUpdated=True)
        return update_conn_object

    obj = crud.database_connections.check_if_connection_exists(
        db, connection_name=payload.connectionName)
    if obj:
        if obj.is_file:
            sch_MCR = schemas.MessageConnectionResponse(
                detail=f'The connection {obj.connection_name} already exist!')
            sch_SCR = schemas.StringConnectionResponse(
                message=sch_MCR, status=status.HTTP_400_BAD_REQUEST)
            sch_DCL = schemas.DatabaseConnectionListSchema(response=sch_SCR)
            return sch_DCL
    else:
        if payload.isFile:
            output_file = utils.save_file(
                Base64file=payload.file, sep=payload.separator)
            if output_file.get("message") != 400:
                payload.file = output_file['message']['filename']
                connection = crud.database_connections.create_connection_raw(
                    db, db_conn=payload)
                format_out = crud.database_connections.format_struct_to_save(db,
                                                                             connections=connection)
                return format_out
            else:
                print("payload.is_file")
                sch_MCR = schemas.MessageConnectionResponse(
                    detail=f'Can"t create connection')
                sch_SCR = schemas.StringConnectionResponse(
                    message=sch_MCR, status=status.HTTP_400_BAD_REQUEST)
                sch_DCL = schemas.DatabaseConnectionListSchema(
                    response=sch_SCR)
                return sch_DCL
        else:
            print("ok")
            # creta and save connection db
            save_conn_object = crud.database_connections.save_or_update_connection_db(
                db=db, payload=payload)
            return save_conn_object


@router.get("/list-connections", response_model=List[schemas.DatabaseConnectionListSchema])
def list_connections(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve connections
    """
    return crud.database_connections.get_all_connections(db)
