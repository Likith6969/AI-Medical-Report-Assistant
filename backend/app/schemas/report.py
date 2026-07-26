from uuid import UUID
from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, ConfigDict, Field


class ReportBase(BaseModel):
    report_type: str  # "Blood", "MRI", "X-ray"


class ReportCreate(ReportBase):
    upload_path: str
    prediction: Optional[str] = None
    confidence: Optional[float] = None
    extracted_data: Optional[Dict[str, Any]] = None
    explanation: Optional[str] = None


class ReportResponse(ReportBase):
    report_id: UUID
    user_id: UUID
    upload_path: str
    prediction: Optional[str] = None
    confidence: Optional[float] = None
    extracted_data: Optional[Dict[str, Any]] = None
    explanation: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ParameterDetail(BaseModel):
    value: float
    unit: Optional[str] = None
    status: str  # "Normal", "High", "Low"
    reference_range: Optional[str] = None


class OverallStatus(BaseModel):
    normal: int = 0
    high: int = 0
    low: int = 0


class BloodReportAnalysisResponse(BaseModel):
    report_id: UUID
    ocr_success: bool
    ocr_text: str
    parameters: Dict[str, ParameterDetail]
    overall_status: OverallStatus
    ai_summary: Optional[str] = None
    processing_time: float

    model_config = ConfigDict(from_attributes=True)
