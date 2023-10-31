# typing
from typing import Any, List, Dict, Optional
# pandas
import pandas as pd
# fastAPI
from fastapi import APIRouter, HTTPException, Depends, UploadFile, status
# sqlalchemy
from sqlalchemy.orm import Session

# TODO app
from app import crud, schemas, models
from app.api import deps
from app.core.config import settings
from app.core import security
from app.services.AWS_handled_files import s3_upload
from app import utils

# cryptography
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
router = APIRouter()


@router.post("/", response_model=Optional[Dict])
async def save_connection(
    payload: schemas.DatabaseConnectionCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Save and Update connections
    """
    # get payload
    # check if connection exists
    obj = crud.database_connections.check_if_connection_exists(
        db, connection_name=payload.connectionName)
    if obj:
        if obj.is_file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'The connection {obj.connection_name} already exist!'
            )
    else:
        if payload.isFile:
            output_file = utils.save_file(Base64file=payload.file)
            if output_file.get("message") != 400:
                payload.database = output_file['message']['filename']
                connection = crud.database_connections.create_connection_raw(
                    db, db_conn=payload)
                print(connection)
                return {"message": {"connectionName": payload.database}, "status": 200}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Can"t create connection'
                )

    #     # plain files

    # # save csv

    # # save json
    # else:
    #     pass
    # # database

    return obj
# @router.post("/upload", response_model=Any)
# async def upload(file: UploadFile | None = None):
#     if not file:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='No file found!!'
#         )

#     contents = await file.read()
#     byte_stream = BytesIO(contents)
#     size = len(contents)

#     # if not 0 < size <= 1 * MB:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_400_BAD_REQUEST,
#     #         detail='Supported file size is 0 - 1 MB'
#     #     )
#     df = pd.read_excel(byte_stream)
#     print(df.columns)
#     file_type = magic.from_buffer(buffer=contents, mime=True)
#     if file_type not in settings.SUPPORTED_FILE_TYPES:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f'Unsupported file type: {file_type}. Supported types are {settings.SUPPORTED_FILE_TYPES}'
#         )
#     file_name = f'{uuid4()}.{settings.SUPPORTED_FILE_TYPES[file_type]}'
#     path_file_to_upload = 'development/development/files/raw-connections/'
#     s3_upload(contents=contents, key=file_name, path=path_file_to_upload)
#     return {'file_name': file_name}
