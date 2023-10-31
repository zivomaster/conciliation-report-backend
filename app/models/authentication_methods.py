from sqlalchemy import Column, String, Integer
from app.db.session import Base


class AuthenticationMethod(Base):
    __tablename__ = "authentication_methods"
    auth_meth_id = Column(Integer, primary_key=True)
    type = Column(String, index=True)
    label = Column(String, index=True)
