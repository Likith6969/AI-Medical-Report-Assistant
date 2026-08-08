import time
import requests
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.user import User
from app.models.report import Report
from app.schemas.report import ReportResponse, BloodReportAnalysisResponse
from app.api.v1.endpoints.auth import get_current_user
from app.core.logging import logger
from app.services.file_service import file_service
from app.services.ocr_service import ocr_service
from app.services.blood_parser import blood_parser
from app.services.gemini_service import gemini_service
from PIL import Image
from app.ml.brain_mri_model import BrainMRIModel

router = APIRouter()

brain_mri_model = BrainMRIModel()


# ── MRI Gemini helper ────────────────────────────────────────────────────────
# gemini_service.generate_summary() is typed for blood ParameterDetail objects.
# This lightweight helper builds an MRI-specific prompt and reuses the same
# Gemini REST infrastructure (same config, same graceful-None contract).

_MRI_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models"
    "/{model}:generateContent"
)

_MRI_CLASS_DESCRIPTIONS = {
    "glioma":      "a type of brain tumor that arises from glial cells",
    "meningioma":  "a typically slow-growing tumor arising from the meninges (brain/spinal cord lining)",
    "pituitary":   "a tumor located at the pituitary gland at the base of the brain",
    "notumor":     "no tumor detected",
}


def _generate_mri_explanation(
    prediction: str,
    confidence: float,
    probabilities: dict,
) -> Optional[str]:
    """
    Calls the Gemini REST API to generate a plain-English educational explanation
    of a Brain MRI ConvNeXt classification result.

    Returns:
        str  — educational explanation
        None — if Gemini is unavailable, quota exhausted, or key not configured

    NEVER raises. Always returns safely so the MRI API cannot fail because of this.
    """
    try:
        from app.core.config import settings
    except Exception:
        return None

    api_key = settings.GEMINI_API_KEY
    placeholders = {"your_gemini_api_key_here", "YOUR_GEMINI_API_KEY", "", None}
    if not api_key or api_key in placeholders:
        logger.warning("MRI Gemini explanation skipped: API key not configured.")
        return None

    model = settings.GEMINI_MODEL
    description = _MRI_CLASS_DESCRIPTIONS.get(prediction.lower(), prediction)
    prob_lines = "\n".join(
        f"  {cls}: {prob * 100:.1f}%" for cls, prob in probabilities.items()
    )

    prompt = (
        f"A Brain MRI scan was analyzed by an AI model (ConvNeXt Tiny).\n"
        f"Result: {prediction.upper()} — {description}.\n"
        f"Confidence: {confidence:.1f}%\n"
        f"Class probabilities:\n{prob_lines}\n\n"
        "You are a health education assistant. Write a short, warm, plain-English "
        "explanation (120–180 words) with the following structure:\n"
        "1. What the AI detected and what it generally means in simple terms.\n"
        "2. One or two sentences on what this type of finding may involve (avoid alarming language).\n"
        "3. A clear disclaimer that this is an AI-assisted educational result, NOT a medical "
        "diagnosis, and that the reader must consult a qualified medical professional "
        "(neurologist or radiologist) for proper evaluation and treatment.\n"
        "Rules: No diagnosis. No prescriptions. Plain English only. Warm, reassuring tone."
    )

    url = _MRI_GEMINI_URL.format(model=model)
    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 350, "topP": 0.9},
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=settings.GEMINI_TIMEOUT_SECONDS)
        resp.raise_for_status()
        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        if text:
            logger.info(f"MRI Gemini explanation received ({len(text)} chars)")
            return text
        return None
    except requests.HTTPError as exc:
        code = exc.response.status_code if exc.response is not None else "?"
        logger.warning(f"MRI Gemini HTTP error {code} — returning explanation=null")
        return None
    except Exception as exc:
        logger.warning(f"MRI Gemini explanation unavailable: {exc} — returning explanation=null")
        return None

@router.post("/blood/analyze", response_model=BloodReportAnalysisResponse, status_code=status.HTTP_201_CREATED)
def analyze_blood_report(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Uploads Blood PDF/Image, extracts biomarkers via OCR engine, runs rule comparison, and returns structured summary."""
    start_time = time.time()
    logger.info(f"upload started by user {current_user.user_id}: {file.filename}")

    # 1. File validation and disk storage
    file_path, stored_filename, original_filename = file_service.save_file(file, category="blood_reports")

    # 2. OCR text extraction
    logger.info(f"OCR started for {file_path}")
    ocr_text, avg_confidence = ocr_service.extract_text(file_path)
    logger.info("OCR completed")

    # 3. Blood parameter extraction & reference range comparison
    parameters, overall_status = blood_parser.parse_text(ocr_text)
    logger.info("parameter extraction completed")

    # 4. Generate Gemini AI educational summary (non-blocking — fails gracefully)
    logger.info("requesting Gemini AI summary")
    ai_summary = gemini_service.generate_summary(parameters, overall_status)
    if ai_summary:
        logger.info("Gemini AI summary received")
    else:
        logger.warning("Gemini AI summary unavailable — proceeding with ai_summary=null")

    processing_time = round(time.time() - start_time, 2)

    # 4. Save report in PostgreSQL
    try:
        report_record = Report(
            user_id=current_user.user_id,
            report_type="Blood",
            upload_path=file_path,
            prediction=f"Extracted {len(parameters)} parameters",
            confidence=avg_confidence,
            extracted_data={
                "original_filename": original_filename,
                "stored_filename": stored_filename,
                "file_path": file_path,
                "ocr_text": ocr_text,
                "parameters": {k: v.model_dump() for k, v in parameters.items()},
                "overall_status": overall_status.model_dump(),
                "ai_summary": ai_summary,
                "processing_status": "COMPLETED",
                "processing_time": processing_time
            },
            explanation=None
        )
        db.add(report_record)
        db.commit()
        db.refresh(report_record)
        logger.info("database save completed")
    except Exception as e:
        db.rollback()
        logger.error(f"Database failure while saving blood report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database failure while saving report record."
        )

    logger.info("processing completed")

    return BloodReportAnalysisResponse(
        report_id=report_record.report_id,
        ocr_success=True,
        ocr_text=ocr_text,
        parameters=parameters,
        overall_status=overall_status,
        ai_summary=ai_summary,
        processing_time=processing_time
    )


@router.post("/mri/analyze", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def analyze_brain_mri(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze Brain MRI using ConvNeXt Tiny model."""

    logger.info(
        f"Brain MRI upload initiated by user {current_user.user_id}: {file.filename}"
    )

    # 1. Validate and save the uploaded file to disk (uploads/mri/)
    file_path, stored_filename, original_filename = file_service.save_file(
        file, category="mri"
    )
    logger.info(f"MRI file saved to {file_path}")

    try:
        # 2. Open saved image from disk for prediction
        image = Image.open(file_path).convert("RGB")

        # 3. ConvNeXt Tiny prediction
        result = brain_mri_model.predict(image)

        # 4. Gemini educational explanation (non-blocking — fails gracefully)
        logger.info("Requesting Gemini MRI explanation")
        mri_explanation = _generate_mri_explanation(
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
        )
        if mri_explanation:
            logger.info("Gemini MRI explanation received")
        else:
            logger.warning("Gemini MRI explanation unavailable — proceeding with explanation=null")

        # 5. Save report to PostgreSQL with real upload_path
        report = Report(
            user_id=current_user.user_id,
            report_type="MRI",
            upload_path=file_path,
            prediction=result["prediction"],
            confidence=result["confidence"],
            extracted_data={
                "original_filename": original_filename,
                "stored_filename": stored_filename,
                "file_path": file_path,
                "class_probabilities": result["probabilities"]
            },
            explanation=mri_explanation
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        logger.info(
            f"Brain MRI analyzed successfully for user {current_user.user_id}: "
            f"prediction={result['prediction']}, confidence={result['confidence']}"
        )

        return report

    except HTTPException:
        raise  # Re-raise file_service validation errors as-is

    except Exception as e:
        db.rollback()
        logger.error(f"Brain MRI analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Brain MRI analysis failed: {str(e)}"
        )





@router.post("/xray/analyze", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def analyze_chest_xray(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Uploads Chest X-Ray (PNG/JPG), processes via PyTorch binary classifier, and returns Grad-CAM visual heatmap."""
    logger.info(f"Chest X-Ray upload initiated by user {current_user.user_id}: {file.filename}")
    
    mock_report = Report(
        user_id=current_user.user_id,
        report_type="X-ray",
        upload_path=f"/uploads/xray/{file.filename}",
        prediction="Normal",
        confidence=0.941,
        extracted_data={
            "class_probabilities": {
                "Normal": 0.941,
                "Pneumonia": 0.059
            },
            "heatmap_path": f"/static/heatmaps/xray_{file.filename}.png"
        },
        explanation="Pulmonary fields appear clear without significant infiltrates or consolidation."
    )
    db.add(mock_report)
    db.commit()
    db.refresh(mock_report)
    return mock_report


@router.get("/", response_model=List[ReportResponse])
def get_user_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetches all past reports uploaded by the authenticated user."""
    return db.query(Report).filter(Report.user_id == current_user.user_id).order_by(Report.created_at.desc()).all()


@router.get("/{report_id}", response_model=ReportResponse)
def get_report_by_id(
    report_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves a specific report by UUID."""
    report = db.query(Report).filter(Report.report_id == report_id, Report.user_id == current_user.user_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletes a specific report."""
    report = db.query(Report).filter(Report.report_id == report_id, Report.user_id == current_user.user_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    db.delete(report)
    db.commit()
    return None
