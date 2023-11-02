from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ConciliationReport(Base):
    __tablename__ = 'conciliation_report'

    reconciliation_id = Column(UUID(as_uuid=True), primary_key=True, server_default='uuid_generate_v4()')
    code = Column(String(100), nullable=False)
    observations = Column(Text)
    name = Column(String(100), nullable=False)
    origin_database = Column(String(100), nullable=False)
    detination_database = Column(String(100), nullable=False)
    reconciliation = Column(String(200))
    last_execution = Column(TIMESTAMP(timezone=True))
    last_execution_done = Column(Boolean,default=False)
