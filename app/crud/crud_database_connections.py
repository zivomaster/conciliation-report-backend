from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session, selectinload

from app.crud.base import CRUDBase
from app.crud.crud_connectors_types import connectors_types
from app.services import database_connections_handlers as conn_handler
from app.models import DatabaseConnection, Type, AuthenticationMethod, ConnectorType
from app.schemas.database_connection import *
from app.schemas.bigquery_schema import *
from app.core.config import settings
from app.services.AWS_handled_files import s3_delete
from app import utils


class CRUDDatabaseConnections(CRUDBase[DatabaseConnection, DatabaseConnectionCreate, DatabaseConnectionUpdate]):

    def get_connection_by_id(self, db: Session, id: uuid) -> Optional[DatabaseConnection]:
        return db.query(DatabaseConnection).filter(DatabaseConnection.id == id).first()

    def check_if_connection_exists(self, db: Session, connection_name: str) -> Optional[DatabaseConnection]:
        return db.query(DatabaseConnection).filter(DatabaseConnection.connection_name == connection_name).first()

    def create_connection_raw(self, db: Session, db_conn: DatabaseConnectionCreate) -> DatabaseConnection:

        db_obj = DatabaseConnection(
            connection_name=db_conn.connectionName,
            database_name=db_conn.database,
            is_file=db_conn.isFile,
            file=db_conn.file,
            separator=db_conn.separator,
            contype_id=db_conn.connectorId
        )
        # Add objects to the session
        db.add(db_obj)
        # Commit changes to the database
        db.commit()
        return db_obj

    def format_struct_to_save(self,
                              db: Session,
                              connections: DatabaseConnection,
                              get_all_files: bool = False) -> Optional[DatabaseConnectionListSchema]:

        # retrieve auth_methods, connector_types, types_connections
        auth_methods = db.query(AuthenticationMethod).all()
        connector_types = db.query(ConnectorType).all()
        types = db.query(Type).all()

        # mapping schemas
        dct_conn_types = [ConnectorTypeModelSchema(contype_id=item.contype_id,
                                                   label=item.label,
                                                   thumbnail_url=item.thumbnail_url,
                                                   type_id=item.type_id,
                                                   auth_meth_id=item.auth_meth_id) for item in connector_types]
        dict_types = {type.type_id: type.name for type in types}

        # Assuming 'auth_methods' is a list of objects containing 'auth_meth_id', 'label', and 'type' attributes
        dict_auth_meth = {auth.auth_meth_id: {
            "label": auth.label, "type": auth.type} for auth in auth_methods}
        connectors = {}
        for conn in dct_conn_types:
            auth_method = []
            if conn.auth_meth_id is not None:
                auth = dict_auth_meth[conn.auth_meth_id]
                auth_method.append(AuthMethodSchema(
                    label=auth["label"], type=auth["type"]))

            obj = ConnectorSchema(
                id=conn.contype_id,
                label=conn.label,
                thumbnailUrl=conn.thumbnail_url,
                type=dict_types[conn.type_id],
                authenticationMethods=auth_method
            )
            connectors[conn.contype_id] = obj
        # check full select or any
        if get_all_files:  # full connections
            connections = db.query(DatabaseConnection).all()
            elements = [
                DatabaseConnectionListSchema(
                    id=item.id,
                    connectionName=item.connection_name,
                    database=item.database_name,
                    hostname=item.hostname,
                    port=item.port,
                    connector=connectors[item.contype_id],
                    isFile=item.is_file,
                    username=item.username
                ) for item in connections
            ]
            return elements
        else:
            msg = StringConnectionResponse(status=200)
            return DatabaseConnectionListSchema(
                id=connections.id,
                connectionName=connections.connection_name,
                database=connections.database_name,
                hostname=connections.hostname,
                port=connections.port,
                connector=connectors[connections.contype_id],
                isFile=connections.is_file,
                username=connections.username,
                response=msg)

    def create_connection_db(self, db: Session,
                             db_conn: DatabaseConnectionCreate) -> DatabaseConnection:

        db_obj = DatabaseConnection(
            connection_name=db_conn.connectionName,
            hostname=db_conn.hostname,
            port=db_conn.port,
            database_name=db_conn.database,
            username=db_conn.username,
            password=db_conn.password,
            file=db_conn.file,
            contype_id=db_conn.connectorId
        )
        # Add objects to the session
        db.add(db_obj)
        # Commit changes to the database
        db.commit()
        return db_obj

    def update_connection_db(self, db: Session,
                             db_conn: DatabaseConnection,
                             current_object: DatabaseConnection) -> Optional[DatabaseConnectionListSchema]:
        """
        retrive database connection details
        """
        obj_update = None
        id_conn = db_conn.id
        if id_conn is not None and id_conn != "":
            conn_update = db.query(DatabaseConnection).filter(
                DatabaseConnection.id == db_conn.id).first()

            if conn_update:
                # update connection
                conn_update.connection_name = db_conn.connectionName
                conn_update.hostname = db_conn.hostname
                conn_update.port = db_conn.port
                conn_update.username = db_conn.username
                conn_update.password = db_conn.password
                # Update
                db.commit()
                return self.format_struct_to_save(db,
                                                  connections=conn_update,
                                                  get_all_files=False)
            else:
                obj = self.check_if_connection_exists(
                    db, connection_name=db_conn.connection_name)
                return self.format_struct_to_save(
                    db, connections=obj, get_all_files=False)
        else:
            return self.format_struct_to_save(
                db, connections=current_object
            )

        return DatabaseConnectionListSchema

    def get_all_connections(self, db: Session) -> List[DatabaseConnectionListSchema]:
        connections = db.query(DatabaseConnection).all()
        return self.format_struct_to_save(db, connections=connections, get_all_files=True)

    def save_or_update_connection_db(self,
                                     db: Session,
                                     payload: Optional[DatabaseConnectionCreate] = None,
                                     db_update: Optional[DatabaseConnectionCreate] = None,
                                     isUpdated: Optional[bool] = False
                                     ) -> Optional[DatabaseConnectionListSchema]:

        # CREATE
        # 1. check dialect
        connector_type = connectors_types.get_connector_by_id(
            db, contype_id=payload.connectorId)
        check_connection_dialet = conn_handler.check_dialect_connection(
            db_type=connector_type.label)
        if check_connection_dialet.status == 400:
            sch_SCR = StringConnectionResponse(
                message=check_connection_dialet.message, status=check_connection_dialet.status)
            sch_DCL = DatabaseConnectionListSchema(
                response=sch_SCR)
            return sch_DCL
        else:
            # 2. test connection
            test_connection = conn_handler.test_connection(
                payload=payload, stringConnResponse=check_connection_dialet)
            if test_connection.status == 400:
                print("test-connection")
                sch_SCR = StringConnectionResponse(
                    message=test_connection.message, status=test_connection.status)
                sch_DCL = DatabaseConnectionListSchema(
                    response=sch_SCR)
                return sch_DCL
            else:

                # BUCKET_PATH_KEYS_AUTH_CONNECTIONS
                print(test_connection.status)
                # 3. save file in s3
                if test_connection.message.detail == "BigQuery":
                    big_query_schema = BigQuerySchemaAuth(password=payload.password,
                                                          project_id=payload.hostname,
                                                          dataset_id=payload.database,
                                                          response=test_connection)
                    print("entro-convertir_base64")
                    response = utils.convert_base64_to_big_query(
                        Base64file=big_query_schema.password, projectId=big_query_schema.project_id)
                    print("obteniendo metadata")
                    client = conn_handler.get_metadata_bigquery(
                        schema_auth=big_query_schema, filename=response.message.dialect)
                    print("obteniendo_metadata_objects")
                    metadata_objects = conn_handler.get_tables_metadata_bigquery(
                        client, big_query_schema.dataset_id)
                    print("se completó la metadata")
                else:
                    metadata = conn_handler.get_metadata(
                        test_connection.message.dialect)
                    metadata_objects = conn_handler.get_tables_metadata(
                        metadata=metadata)
                # check Create or update
                if isUpdated:
                    upload_file_s3_details = conn_handler.save_file(
                        metadata_objects=metadata_objects,
                        isUpdated=True, filename=db_update.file)
                    payload.file = upload_file_s3_details.message.dialect
                    update_connection = self.update_connection_db(db,
                                                                  db_conn=payload,
                                                                  current_object=db_update)
                    return update_connection
                else:
                    # 4. save connection in db
                    upload_file_s3_details = conn_handler.save_file(
                        metadata_objects=metadata_objects)
                    payload.file = upload_file_s3_details.message.dialect
                    create_connection = self.create_connection_db(
                        db=db, db_conn=payload)
                    format_output = self.format_struct_to_save(db,
                                                               connections=create_connection)
                    return format_output

    def delete_connection(self, db: Session, id: Optional[uuid.UUID] = None) -> StringConnectionResponse:
        obj = db.query(DatabaseConnection).get(id)
        # delete s3 object
        try:
            deleted_item = s3_delete(
                key=obj.file, path=settings.BUCKET_PATH_SAVE_CONNECTIONS)
            db.delete(obj)
            db.commit()
            sch_MCR = MessageConnectionResponse(
                detail='message',
                dialect=f"se eliminó la conexión {obj.id} correctamente")
            sch_SCR = StringConnectionResponse(
                message=sch_MCR, status=200)
            return sch_SCR
        except Exception as e:
            sch_MCR = MessageConnectionResponse(
                detail='message',
                dialect=f"No se pudo eliminar el objeto {obj.id} correctamente: error{e}")
            sch_SCR = StringConnectionResponse(
                message=sch_MCR, status=200)
            return sch_SCR


database_connections = CRUDDatabaseConnections(DatabaseConnection)
