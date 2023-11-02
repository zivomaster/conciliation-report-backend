from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4
Base = declarative_base()

class DatarulesDefinition(Base):
    __tablename__ = 'datarules_definition'
    datarules_definition_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)

class Datarules(Base):
    __tablename__ = 'datarules'

    datarules_id = Column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    type = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    datarules_definition_id = Column(UUID(as_uuid=True), ForeignKey('datarules_definition.datarules_definition_id'), nullable=False)

