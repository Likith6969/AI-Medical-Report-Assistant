from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.report import Report
from app.schemas.dashboard import DashboardSummary
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves high-level summary metrics for the patient dashboard."""
    reports = db.query(Report).filter(Report.user_id == current_user.user_id).order_by(Report.created_at.desc()).all()
    
    total_count = len(reports)
    blood_count = sum(1 for r in reports if r.report_type == "Blood")
    mri_count = sum(1 for r in reports if r.report_type == "MRI")
    xray_count = sum(1 for r in reports if r.report_type == "X-ray")
    
    recent = reports[:5]
    
    return DashboardSummary(
        total_reports=total_count,
        blood_reports_count=blood_count,
        mri_reports_count=mri_count,
        xray_reports_count=xray_count,
        recent_reports=recent
    )
