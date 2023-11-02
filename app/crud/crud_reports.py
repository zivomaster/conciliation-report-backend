from sqlalchemy.orm import Session
from app.models import ConciliationReport
from app import schemas
from app.crud.base import CRUDBase

class CRUDReports(CRUDBase[ConciliationReport, schemas.ReportReconciliation, schemas.ReportReconciliation]):
    
    def create_report(self, db: Session, report: schemas.ReportReconciliationWithReconciliation):
        # get Reconciliation
        reconciliation = report.reconciliation
        # pop reconciliation
        add_report = ConciliationReport(
            code=report.code,
            observations=report.observations,
            name=report.name,
            origin_database=report.originDatabase,
            target_database=report.destinationDatabase,
            )
        db.add(add_report)
        db.commit()
        db.refresh(add_report)
        return add_report

reports = CRUDReports(ConciliationReport)