from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api.deps import get_db
import uuid

router = APIRouter()

@router.post("/create/", response_model=schemas.DatarulesDefinitionCreate)
def create_or_updated(datarules: schemas.DatarulesDefinitionCreate, 
                     db: Session = Depends(get_db)) -> schemas.DatarulesDefinition:
    if datarules.id is None:
          print("created")
          return crud.crud_datarules.datarules.create_datarules_definition(db,datarules_def=datarules)
    else:
          isExist = crud.datarules.get_datarules_definition(db, datarules.id)
    if isExist is None:
            raise HTTPException(status_code=404, detail="Datarules definition no existe")
    print("updated")
    return crud.crud_datarules.datarules.update_datarules_definition(db,updated_datarules_def=datarules,datarules_definition_id=datarules.id)
          


# @router.put("/update/{datarules_definition_id}", response_model=schemas.DatarulesDefinition)
# def update_datarules(datarules_def: schemas.DatarulesDefinitionCreate,
#                     db: Session = Depends(get_db),
#                     datarules_definition_id=uuid):
#     isExist = crud.datarules.get_datarules_definition(db, datarules_definition_id)
#     if isExist is None:
#             raise HTTPException(status_code=404, detail="Datarules definition no existe")

#     return crud.crud_datarules.datarules.update_datarules_definition(db,updated_datarules_def=datarules_def,datarules_definition_id=datarules_definition_id)

@router.get("/list/", response_model=list[schemas.DatarulesList])
def list_datarules( db: Session = Depends(get_db)):
    return crud.crud_datarules.datarules.get_all_datarules_definitions(db)

@router.get("/get/{datarules_definition_id}", response_model=schemas.DatarulesDefinition)
def list_especific_datarules(db: Session = Depends(get_db), datarules_definition_id=uuid):
    isExist = crud.datarules.get_datarules_definition(db, datarules_definition_id)
    if isExist is None:
            raise HTTPException(status_code=404, detail="Datarules definition no existe")
    return crud.crud_datarules.datarules.get_datarules_definitions_by_id(db,
                                                                         datarules_definition_id=datarules_definition_id)

@router.delete("/delete/{datarules_definition_id}")
def delete_datarules(db: Session = Depends(get_db),   datarules_definition_id=uuid):
    """
    Delete datarules
    """
    isExist = crud.datarules.get_datarules_definition(db, datarules_definition_id)
    if isExist is None:
            raise HTTPException(status_code=404, detail="Datarules definition no existe")
    return crud.crud_datarules.datarules.delete_datarules(db,datarules_definition_id=datarules_definition_id)