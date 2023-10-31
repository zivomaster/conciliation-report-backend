from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session, selectinload

from app.crud.base import CRUDBase
from app.models import DatabaseConnection
from app.schemas.database_connection import DatabaseConnectionCreate, DatabaseConnectionUpdate, DatabaseConnectionSchema


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
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        # {
        #     "id": "",
        #     "database": "6",
        #     "connectionName": "asdfadsf",
        #     "hostname": "",
        #     "port": "",
        #     "databaseName": "",
        #     "connectionType": "",
        #     "username": "",
        #     "password": "",
        #     "file": "data:application/json;base64,ewogICJkZWZhdWx0IjogIk9wZXJhZG9yIGRlIHRvdXIgdHViaW5nIHJpbyBhcmVuYWxcblxuIiwKICAiRVMiOiAiT3BlcmFkb3IgZGUgdG91ciB0dWJpbmcgcmlvIGFyZW5hbCIsCiAgIkVOIjogIk9wZXJhZG9yIGRlIHRvdXIgdHViaW5nIHJpbyBhcmVuYWwiCn0=",
        #     "separator": ","
        # }
    #    def create(self, db: Session, user: UserCreate) -> User:
    #     db_obj = User(
    #         username=user.username,
    #         email=user.email,
    #         password_hash=get_password_hash(user.password)
    #     )
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj
    # def get_all_connectors(self, db: Session,  skip: int = 0, limit: int = 100) -> Optional[Any]:
    #     # Query SQLAlchemy ORM
    #     query = (
    #         db.query(ConnectorType)
    #         .outerjoin(AuthenticationMethod, ConnectorType.auth_meth_id == AuthenticationMethod.auth_meth_id)
    #         .outerjoin(Type, ConnectorType.type_id == Type.type_id)
    #         .options(selectinload(ConnectorType.authentication_method), selectinload(ConnectorType.type))
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )
    #     return query

    # def get_auth_methods(self, db: Session,  skip: int = 0, limit: int = 100) -> Optional[AuthenticationMethod]:
    #     # Query SQLAlchemy ORM db.query(self.model).offset(skip).limit(limit).all()
    #     query = (
    #         db.query(AuthenticationMethod)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )
    #     return query

    # def get_types_connections(self, db: Session,  skip: int = 0, limit: int = 100) -> Optional[Type]:
    #     # Query SQLAlchemy ORM db.query(self.model).offset(skip).limit(limit).all()
    #     query = (
    #         db.query(Type)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )
    #     return query


database_connections = CRUDDatabaseConnections(DatabaseConnection)
