from typing import Any, List, Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
import json


from app import crud, schemas, models
from app.api import deps
from app.core.config import settings
# from app.schemas.user import User, UserCreate, UserUpdate
router = APIRouter()


@router.get("/", response_model=Dict)
def list_connectors_types(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_authenticated_user),
) -> Any:
    """
    Retrieve connectors types.
    """
    connectors_types = crud.connectors_types.get_all_connectors(
        db=db, skip=skip, limit=limit)
    # auth_methods
    auth_methods = crud.connectors_types.get_auth_methods(
        db=db, skip=skip, limit=limit)
    # types
    types_connections = crud.connectors_types.get_types_connections(
        db=db, skip=skip, limit=limit)

    # cast data to dict
    dicts_auth_method = {}
    for obj in auth_methods:
        dicts_auth_method[obj.auth_meth_id] = {
            "type": obj.type, "label": obj.label}

    dicts_types_connections = {}
    for obj in types_connections:
        dicts_types_connections[obj.type_id] = {"name": obj.name}
    # get datastructure output
    output_data = {
        "connectorTypes": []
    }
    # iterate main object
    for obj in connectors_types:
        auth_methods = []
        if obj.auth_meth_id is not None:
            auth_methods.append(dicts_auth_method[obj.auth_meth_id])
        # generate output
        output_obj = {
            "id": obj.contype_id,
            "authenticationMethods": auth_methods,
            "label": obj.label,
            "thumbnailUrl": obj.thumbnail_url,
            # Asignar los tipos según la lógica
            "type": dicts_types_connections[obj.type_id]["name"]
        }
        output_data["connectorTypes"].append(output_obj)

    return output_data
