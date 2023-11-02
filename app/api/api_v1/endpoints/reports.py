from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api.deps import get_db
import uuid

router = APIRouter()

@router.post("/create/", response_model=schemas.ReportReconciliationWithReconciliation)
def create_or_updated(report: schemas.ReportReconciliationWithReconciliation, 
                     db: Session = Depends(get_db)) -> schemas.ReportReconciliation:
    if report.id is None or report.id == "":
        return crud.reports.create_report(db,report=report)
    return {"existe": 200}
          
# @router.get("/list/", response_model=list[schemas.DatarulesList])
# def list_datarules( db: Session = Depends(get_db)):
#     return crud.crud_datarules.datarules.get_all_datarules_definitions(db)

# @router.get("/get/{datarules_definition_id}", response_model=schemas.DatarulesDefinition)
# def list_especific_datarules(db: Session = Depends(get_db), datarules_definition_id=uuid):
#     isExist = crud.datarules.get_datarules_definition(db, datarules_definition_id)
#     if isExist is None:
#             raise HTTPException(status_code=404, detail="Datarules definition no existe")
#     return crud.crud_datarules.datarules.get_datarules_definitions_by_id(db,
#                                                                          datarules_definition_id=datarules_definition_id)

# @router.delete("/delete/{datarules_definition_id}")
# def delete_datarules(db: Session = Depends(get_db),   datarules_definition_id=uuid):
#     """
#     Delete datarules
#     """
#     isExist = crud.datarules.get_datarules_definition(db, datarules_definition_id)
#     if isExist is None:
#             raise HTTPException(status_code=404, detail="Datarules definition no existe")
#     return crud.crud_datarules.datarules.delete_datarules(db,datarules_definition_id=datarules_definition_id)