from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base
from uuid import uuid4


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_authenticated = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
