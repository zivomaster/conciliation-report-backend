from typing import Optional, Dict
from app.schemas.metadata import TableColumnSchema, TableMetadataSchema
from app.schemas import connection_builder as schema
from app.schemas import database_connection as db_conn_schema
from app.schemas import BigQuerySchemaAuth
import json
# import pyodbc
from uuid import uuid4
from sqlalchemy import create_engine, MetaData
from app.core.config import settings
from app.core import security
from .AWS_handled_files import s3_upload
from .BigQuery_handled_files import BigQuery_auth, get_bigquery_client, get_tables_metadata_bq


def check_dialect_connection(db_type: str = None,) -> Optional[schema.StringConnectionResponse]:
    if db_type not in settings.ALLOW_DIALECTS_DB:
        return schema.StringConnectionResponse(message=schema.MessageConnectionResponse(detail=f"El tipo de base de datos: {db_type} es incorrecto.Bases de datos permitidas {settings.ALLOW_DIALECTS_DB.keys()}"),
                                               status=400)
    dialect = settings.ALLOW_DIALECTS_DB[db_type]
    return schema.StringConnectionResponse(message=schema.MessageConnectionResponse(detail=db_type, dialect=dialect),
                                           status=200)


def create_string_connection(stringConnResponse: schema.StringConnectionResponse = None,
                             payload: db_conn_schema.DatabaseConnectionCreate = None,
                             password_encrypt: bytes = None) -> Optional[schema.StringConnectionResponse]:
    # get pa
    # decrypt password
    private_key = security.get_private_key()
    decrypt_password_byte = security.decrypt_message(
        private_key=private_key, encrypted=password_encrypt
    )
    decrypt_passsword_str = decrypt_password_byte.decode('utf-8')
    # check dialect
    dialect = settings.ALLOW_DIALECTS_DB[stringConnResponse.message.detail]
    str_conn = ''
    string_connection_response = None
    if dialect != "BigQuery" or "MongoDB":
        # schema: ConnectionBuilderRDSOrMongoDB
        rds_conn = schema.ConnectionBuilderRDS(database=payload.database,
                                               hostname=payload.hostname,
                                               username=payload.username,
                                               password=decrypt_passsword_str,
                                               port=payload.port
                                               )
        # Oracle
        key = next((key for key, value in settings.ALLOW_DIALECTS_DB.items(
        ) if value == dialect), None)

        if key == "Oracle":
            str_conn = f'{dialect}://{rds_conn.username}:{rds_conn.password}@{rds_conn.hostname}:{rds_conn.port}/?service_name={rds_conn.database}'
            string_connection_response = schema.StringConnectionResponse(
                message=schema.MessageConnectionResponse(
                    detail=key, dialect=str_conn),
                status=200
            )
        elif key == "PostgreSQL" or key == "MySQL":
            str_conn = f'{dialect}://{rds_conn.username}:{rds_conn.password}@{rds_conn.hostname}:{rds_conn.port}/{rds_conn.database}'
            string_connection_response = schema.StringConnectionResponse(
                message=schema.MessageConnectionResponse(
                    detail=key, dialect=str_conn),
                status=200
            )
        else:
            # Driver name may vary based on your system and installed drivers
            driver = 'ODBC+Driver+17+for+SQL+Server'
            str_conn = f'{dialect}://{rds_conn.username}:{rds_conn.password}@{rds_conn.hostname}:{rds_conn.port}/{rds_conn.database}?driver={driver}'
            string_connection_response = schema.StringConnectionResponse(
                message=schema.MessageConnectionResponse(
                    detail=key, dialect=str_conn),
                status=200
            )
    else:
        # big query
        if dialect == "BigQuery":
            return schema.StringConnectionResponse(
                message=schema.MessageConnectionResponse(
                    detail=key, dialect=key),
                status=200
            )
    return string_connection_response


def test_connection(payload: db_conn_schema.DatabaseConnectionCreate = None,
                    stringConnResponse: schema.StringConnectionResponse = None
                    ) -> Optional[schema.StringConnectionResponse]:

    # Test Connection
    if stringConnResponse.status == 400:
        return response
    else:
        output = None
        if stringConnResponse.message.dialect == "BigQuery":
            output = stringConnResponse
        else:
            try:
                public_key = security.get_public_key()
                # encrypt password
                print("encryptando password")
                encrypted_password = security.encrypt_message(
                    public_key, message=payload.password.encode('utf-8'))

                response = create_string_connection(
                    stringConnResponse, payload=payload, password_encrypt=encrypted_password)
                # Establish the connection
                engine = create_engine(response.message.dialect)
                isConnected = False
                # Test the connection by querying the database
                with engine.connect() as connection:
                    isConnected = True
                if isConnected:
                    output = schema.StringConnectionResponse(
                        message=schema.MessageConnectionResponse(
                            detail="testConnection", dialect=response.message.dialect),
                        status=200
                    )

            except Exception as error:
                output = schema.StringConnectionResponse(
                    message=schema.MessageConnectionResponse(
                        detail="testConnection", dialect=f"error: {error}"),
                    status=400
                )
    return output


def get_metadata(string_connection: str) -> Optional[MetaData]:
    # Establish the connection
    engine = create_engine(string_connection)
    # Reflect the database tables
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata


def get_tables_metadata(metadata: MetaData) -> list[TableMetadataSchema]:
    table_metadata = []
    for table in metadata.sorted_tables:
        columns_info = []
        for column in table.columns:
            column_info = TableColumnSchema(
                column_name=column.name, data_type=str(column.type))
            columns_info.append(column_info)
        table_info = TableMetadataSchema(
            table_name=table.name, columns=columns_info)
        table_metadata.append(table_info)
    return table_metadata


def get_metadata_bigquery(schema_auth: BigQuerySchemaAuth, filename: str):
    # get credentials
    credentials = BigQuery_auth(filename=filename)
    return get_bigquery_client(credentials=credentials,
                               project_id=schema_auth.project_id)


def get_tables_metadata_bigquery(client, dataset_id: str) -> list[TableMetadataSchema]:
    return get_tables_metadata_bq(client, dataset_id=dataset_id)


def save_format_tables(metadata_objects: TableMetadataSchema) -> Optional[Dict]:
    tables = []
    for metadata_object in metadata_objects:
        table = {
            "name": metadata_object.table_name,
            "key": metadata_object.table_name,
            "fields": [
                {
                    "name": field.column_name,
                    "key": field.column_name.lower(),
                    "type": field.data_type
                }
                for field in metadata_object.columns
            ]
        }
        tables.append(table)
    return {
        "tables": tables
    }


def save_file(metadata_objects: Optional[TableMetadataSchema],
              isUpdated: Optional[bool] = False,
              filename: Optional[str] = False) -> Optional[schema.StringConnectionResponse]:
    if isUpdated:
        pass
    else:
        filename = f'{uuid4()}.json'
    # save  JSON file
    metadata = save_format_tables(metadata_objects)
    # Convert dictionary to JSON
    json_data = json.dumps(metadata, indent=4)
    # upload to s3
    s3_upload(contents=json_data, key=filename,
              path=settings.BUCKET_PATH_SAVE_CONNECTIONS)
    return schema.StringConnectionResponse(
        message=schema.MessageConnectionResponse(
            detail="filename", dialect=filename),
        status=200
    )
