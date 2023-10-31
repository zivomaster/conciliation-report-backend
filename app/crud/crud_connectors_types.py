from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session, selectinload

from app.crud.base import CRUDBase
from app.models import Type, ConnectorType, AuthenticationMethod
from app.schemas.connector_types import ConnectorTypeSchema, ConnectorTypeUpdate


class CRUDConnectorsTypes(CRUDBase[ConnectorType, ConnectorTypeSchema, ConnectorTypeUpdate]):

    def get_by_label(self, db: Session, label: str) -> Optional[ConnectorType]:
        return db.query(ConnectorType).filter(ConnectorType.label == label).first()

    def get_all_connectors(self, db: Session,  skip: int = 0, limit: int = 100) -> Optional[Any]:
        # Query SQLAlchemy ORM
        query = (
            db.query(ConnectorType)
            .outerjoin(AuthenticationMethod, ConnectorType.auth_meth_id == AuthenticationMethod.auth_meth_id)
            .outerjoin(Type, ConnectorType.type_id == Type.type_id)
            .options(selectinload(ConnectorType.authentication_method), selectinload(ConnectorType.type))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return query

    def get_auth_methods(self, db: Session,  skip: int = 0, limit: int = 100) -> Optional[AuthenticationMethod]:
        # Query SQLAlchemy ORM db.query(self.model).offset(skip).limit(limit).all()
        query = (
            db.query(AuthenticationMethod)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return query

    def get_types_connections(self, db: Session,  skip: int = 0, limit: int = 100) -> Optional[Type]:
        # Query SQLAlchemy ORM db.query(self.model).offset(skip).limit(limit).all()
        query = (
            db.query(Type)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return query


connectors_types = CRUDConnectorsTypes(ConnectorType)
