from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class Reconciliation(BaseModel):
    originTable: Optional[str]  = None
    originField: Optional[str]  = None
    originFieldApplySum: bool = False
    originFieldApplyHomologation: bool = False
    definitionHomologationId: Optional[str]  = None
    homologationId: Optional[str]  = None
    originFieldApplyCount: bool = False
    originFieldApplyKey: bool = False
    destinationTable: Optional[str]  = None
    destinationField: Optional[str]  = None
    destinationFieldApplySum: bool = False
    destinationFieldApplyHomologation: bool = False
    destinationFieldApplyCount: bool = False
    destinationFieldApplyKey: bool = False

class ReportReconciliationBase(BaseModel):
    id: Optional[UUID4]
    code: Optional[str]  = None
    observations: Optional[str]
    name: Optional[str]  = None
    originDatabase: Optional[str]  = None
    destinationDatabase: Optional[str]  = None
    lastExecutionAt: Optional[datetime]

class ReportReconciliation(ReportReconciliationBase):
    lastExecutionIsDone: bool = False

class ReportReconciliationWithReconciliation(ReportReconciliation):
    reconciliation: List[Reconciliation]