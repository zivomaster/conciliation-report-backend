from pydantic import BaseModel
from typing import Optional


class TypeSchema(BaseModel):
    type_id: Optional[int]
    name: Optional[str]

    class Config:
        orm_mode = True
        field_defaults = {
            "type_id": "",
            "name": ""
        }


class AuthenticationMethodSchema(BaseModel):
    auth_meth_id: Optional[int]
    type: Optional[str]
    label: Optional[str]

    class Config:
        orm_mode = True
        field_defaults = {
            "type": "",
            "label": "",
            "auth_meth_id": ""
        }


class ConnectorTypeSchema(BaseModel):
    contype_id: int
    label: str
    thumbnail_url: str
    auth_meth_id: Optional[int]
    type_id: Optional[int]

    # authentication_method: AuthenticationMethodSchema
    # type: TypeSchema

    class Config:
        orm_mode = True

# Properties to receive via API on update


class ConnectorTypeUpdate(ConnectorTypeSchema):
    contype_id: Optional[int] = None
