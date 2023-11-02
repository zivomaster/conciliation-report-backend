from datetime import datetime, timedelta
from typing import Dict, Optional, List
from jose import jwt
import pandas as pd
import base64
import io
import json
from uuid import uuid4

from app.core.config import settings
from app.services.AWS_handled_files import s3_upload, s3_download
from app.schemas.msg import StringConnectionResponse, MessageConnectionResponse
from app.schemas.connection_table import ConnectionTableSchema


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


def check_base64_file(Base64file: str) -> Optional[Dict]:
    # output message
    output = {}
    # check header
    header = Base64file.split(",")[0]
    print(header)
    if header not in settings.SUPPORTED_FILE_TYPES.keys():
        output = {
            "message": f'Unsupported file type: {header}. Supported types are {settings.SUPPORTED_FILE_TYPES}',
            "status": 400
        }
        return output
    # switch beetween datatype file
    if settings.SUPPORTED_FILE_TYPES[header] == 'csv':
        output = {"message": "csv",
                  "extension": "data:application/csv;base64",
                  "status": 200}
    else:
        output = {"message": "xlsx",
                  "extension": 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64',
                  "status": 200}
    return output


def get_structure_of_save_tables(filename: str, columns: list = []) -> Optional[Dict]:
    structure = {
        "tables": [
            {
                "name": filename,
                "key": filename,
                "fields": [
                    {"name": col, "key": col.lower(), "type": "VARCHAR"} for col in columns
                ]
            }
        ]
    }
    return structure


def convert_base64_to_file(Base64file: str, sep: str = ',') -> Optional[Dict]:
    # error message
    error_message = {
        "message": f'The file: {Base64file}. is empty, please check again.',
        "status": 400
    }
    # chek base64 file
    file_type = check_base64_file(Base64file)
    if file_type.get("status") == 400:
        return file_type

    # convert_base64_file
    if file_type.get("message") == "csv":
        decoded_data = base64.b64decode(
            Base64file.split(",")[1]).decode('utf-8')
        # decoded_data = base64.b64decode(Base64file)
        csv_data = io.StringIO(decoded_data)
        data = pd.read_csv(csv_data, sep=sep)
        # check if the CSV content is not empty
        if data.columns is not None:
            # save  JSON file
            filename = f'{uuid4()}.json'
            columns = list(data.columns)
            dict_structure = get_structure_of_save_tables(
                filename=filename, columns=columns)
            # Convert dictionary to JSON
            json_data = json.dumps(dict_structure, indent=4)
            # upload to s3
            s3_upload(contents=json_data, key=filename,
                      path=settings.BUCKET_PATH_SAVE_CONNECTIONS)
            # data.to_csv(path, sep=sep, index=False)
            return {
                "message": {"filename": filename},
                "status": 200
            }
        else:
            return error_message
    else:
        decoded_data = base64.b64decode(
            Base64file.split(",")[1])
        excel_data = io.BytesIO(decoded_data)
        data = pd.read_excel(excel_data)
        # check if the XLSX content is not empty
        if data.columns is not None:
            # save  JSON file
            filename = f'{uuid4()}.json'
            columns = list(data.columns)
            dict_structure = get_structure_of_save_tables(
                filename=filename, columns=columns)
            # Convert dictionary to JSON
            json_data = json.dumps(dict_structure, indent=4)
            # upload to s3
            s3_upload(contents=json_data, key=filename,
                      path=settings.BUCKET_PATH_SAVE_CONNECTIONS)
            # data.to_csv(path, sep=sep, index=False)
            return {
                "message": {"filename": filename},
                "status": 200
            }
        else:
            return error_message


def save_file(Base64file: str, sep: str = ',') -> Optional[Dict]:
    return convert_base64_to_file(Base64file=Base64file, sep=sep)


def convert_base64_to_big_query(Base64file: str, projectId: str) -> Optional[StringConnectionResponse]:
    # s3 upload
    filename = f'{projectId}-{uuid4()}.json'
    decoded_data = base64.b64decode(Base64file).decode('utf-8')
    # upload to s3
    response = s3_upload(contents=decoded_data, key=filename,
                         path=settings.BUCKET_PATH_KEYS_AUTH_CONNECTIONS)
    print(response)
    MCR = MessageConnectionResponse(detail="filename", dialect=filename)
    return StringConnectionResponse(message=MCR, status=200)


def get_array_list_tables(key: str,
                          id_conn: Optional[str],
                          isExist: Optional[bool] = False) -> List[ConnectionTableSchema]:
    list_conn_table = []
    if isExist:
        path = settings.BUCKET_PATH_TABLES_SELECTED
        # search file
        response = s3_download(key=id_conn+'.json',
                               path=path)
        # convert to dict
        json_data = response['Body'].read().decode('utf-8')
        # Deserialize the JSON string to a Python list
        json_list = json.loads(json_data)
        # Convert each dictionary to ConnectionTableSchema instances
        list_conn_table = [ConnectionTableSchema(**item) for item in json_list]
    else:
        path = settings.BUCKET_PATH_SAVE_CONNECTIONS
        # search file
        response = s3_download(key=key,
                               path=path)
        # convert to dict
        json_data = response['Body'].read().decode('utf-8')
        dict_data = json.loads(json_data)

        # get tables
        array_tables = dict_data["tables"]

        for tables in array_tables:
            schema = ConnectionTableSchema(name=tables["name"],
                                           key=tables["key"])
            list_conn_table.append(schema)
        # upload file
        # Convert each ConnectionTableSchema instance to a dictionary and collect in a list
        list_as_dict = [item.dict() for item in list_conn_table]
        # Serialize the list to JSON
        json_data = json.dumps(list_as_dict)
        key = id_conn + '.json'
        upload = s3_upload(contents=json_data, key=key,
                           path=settings.BUCKET_PATH_TABLES_SELECTED)
    return list_conn_table


def update_selected_tables(key: str,
                           selectedTables: Optional[List[str]] = False) -> List[ConnectionTableSchema]:
    list_conn_table = []
    path = settings.BUCKET_PATH_TABLES_SELECTED
    # search file
    response = s3_download(key=key,
                           path=path)
    # convert to dict
    json_data = response['Body'].read().decode('utf-8')
    # Deserialize the JSON string to a Python list
    json_list = json.loads(json_data)
    # check selected tables
    list_updated = [
        {**table,
            "isSelected": True} if table["name"] in selectedTables else table
        for table in json_list
    ]

    # Convert each dictionary to ConnectionTableSchema instances
    list_conn_table = [ConnectionTableSchema(**item) for item in list_updated]
    # upload file
    # Convert each ConnectionTableSchema instance to a dictionary and collect in a list
    list_as_dict = [item.dict() for item in list_conn_table]
    # Serialize the list to JSON
    contents = json.dumps(list_as_dict)
    upload = s3_upload(contents=contents, key=key,
                       path=settings.BUCKET_PATH_TABLES_SELECTED)
    return list_conn_table
