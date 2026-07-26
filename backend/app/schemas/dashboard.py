from typing import List, Dict, Any
from pydantic import BaseModel
from app.schemas.report import ReportResponse


class DashboardSummary(BaseModel):
    total_reports: int
    blood_reports_count: int
    mri_reports_count: int
    xray_reports_count: int
    recent_reports: List[ReportResponse]
    disclaimer: str = "This dashboard presents educational analysis summaries and is not a substitute for clinical medical evaluation."
