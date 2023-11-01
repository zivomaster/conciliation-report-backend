from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.types import Type
from app.models.authentication_methods import AuthenticationMethod


class ConnectorType(Base):
    __tablename__ = "connectors_types"
    contype_id = Column(Integer, primary_key=True)
    label = Column(String, index=True)
    thumbnail_url = Column(String, index=True)
    auth_meth_id = Column(Integer, ForeignKey(
        'authentication_methods.auth_meth_id'))
    type_id = Column(Integer, ForeignKey('types.type_id'))
    # Definir las relaciones con las otras tablas
    # authentication_method = relationship(
    #     "AuthenticationMethod", backref="connectors")
    # type = relationship("Type", backref="connectors")
