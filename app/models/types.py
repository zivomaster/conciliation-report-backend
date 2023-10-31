from sqlalchemy import Column, String, Integer
from app.db.session import Base


class Type(Base):
    __tablename__ = "types"
    type_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
