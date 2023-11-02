from pydantic import BaseModel
from typing import Optional


class TableColumnSchema(BaseModel):
    column_name: Optional[str] = None
    data_type: Optional[str] = None


class TableMetadataSchema(BaseModel):
    table_name: Optional[str] = None
    columns: list[TableColumnSchema]

# def get_tables_metadata(metadata: MetaData) -> list[TableMetadataSchema]:
#     table_metadata = []
#     for table in metadata.sorted_tables:
#         columns_info = []
#         for column in table.columns:
#             column_info = TableColumnSchema(
#                 column_name=column.name, data_type=str(column.type))
#             columns_info.append(column_info)
#         table_info = TableMetadataSchema(
#             table_name=table.name, columns=columns_info)
#         table_metadata.append(table_info)
#     return table_metadata