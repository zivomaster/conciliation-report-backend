from sqlalchemy import Column, Boolean, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.connectors_types import ConnectorType
from app.models.user import User
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class DatabaseConnection(Base):
    __tablename__ = "database_connections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    connection_name = Column(String, index=True, nullable=False, unique=True)
    hostname = Column(String, index=True)
    port = Column(Integer)
    database_name = Column(String)
    username = Column(String)
    password = Column(String)
    is_file = Column(Boolean(), default=False)
    file = Column(String)
    separator = Column(String)
    contype_id = Column(Integer, ForeignKey('connectors_types.contype_id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.user_id'))
    # Definir las relaciones con las otras tablas
    conn_type_connector = relationship(
        "ConnectorType", backref="connectors")
    user_connector = relationship("User", backref="users")
