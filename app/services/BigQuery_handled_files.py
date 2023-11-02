from google.cloud import bigquery
from google.oauth2 import service_account
from .AWS_handled_files import s3_download
from app import schemas
from app.schemas.metadata import TableColumnSchema, TableMetadataSchema
import uuid
import json

from app.core.config import settings


def BigQuery_auth(filename: str):
    # get s3 file
    response = s3_download(
        key=filename, path=settings.BUCKET_PATH_KEYS_AUTH_CONNECTIONS)
    json_data = response['Body'].read().decode('utf-8')
    data = json.loads(json_data)
    file_path = f'{settings.BASE_DIR}/services/tmp/{filename}'
    # Save the dictionary as a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(file_path)
    print("ok-key-extracted")

    # Set up credentials from the service account key file
    client = service_account.Credentials.from_service_account_file(file_path)
    print("client-ok")
    return client


def get_bigquery_client(credentials, project_id: str):
    # Create a BigQuery client with the service account credentials
    client = bigquery.Client(credentials=credentials,
                             project=project_id)
    return client


def get_tables_metadata_bq(client, dataset_id: str) -> list[TableMetadataSchema]:
    # Retrieve metadata (list of tables and their schemas) for the dataset
    dataset_ref = client.dataset(dataset_id)
    tables_metadata = []
    tables = client.list_tables(dataset_ref)

    for table in tables:
        columns_info = []
        for column in client.get_table(table).schema:
            column_info = TableColumnSchema(
                column_name=column.name, data_type=str(column.field_type)
            )
            columns_info.append(column_info)
        table_info = TableMetadataSchema(
            table_name=table.table_id, columns=columns_info
        )
        tables_metadata.append(table_info)
    return tables_metadata
