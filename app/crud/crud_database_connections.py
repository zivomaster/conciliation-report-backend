from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session, selectinload

from app.crud.base import CRUDBase
from app.crud.crud_connectors_types import connectors_types
from app.models import DatabaseConnection, Type, AuthenticationMethod, ConnectorType
from app.schemas.database_connection import *


class CRUDDatabaseConnections(CRUDBase[DatabaseConnection, DatabaseConnectionCreate, DatabaseConnectionUpdate]):

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
                    isFile=item.is_file
                ) for item in connections
            ]
            return elements
        else:
            return DatabaseConnectionListSchema(
                id=connections.id,
                connectionName=connections.connection_name,
                database=connections.database_name,
                hostname=connections.hostname,
                port=connections.port,
                connector=connectors[connections.contype_id],
                isFile=connections.is_file)

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

    def get_all_connections(self, db: Session) -> List[DatabaseConnectionListSchema]:
        connections = db.query(DatabaseConnection).all()
        return self.format_struct_to_save(db, connections=connections, get_all_files=True)


database_connections = CRUDDatabaseConnections(DatabaseConnection)
