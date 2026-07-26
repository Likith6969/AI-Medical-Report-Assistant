import re
from typing import Dict, Any, Tuple, Optional
from app.schemas.report import ParameterDetail, OverallStatus
from app.core.logging import logger

# Configurable reference ranges for blood parameters
REFERENCE_RANGES = {
    # CBC
    "hemoglobin": {"min": 12.0, "max": 17.5, "unit": "g/dL", "display_name": "Hemoglobin"},
    "rbc": {"min": 4.2, "max": 6.1, "unit": "x10^6/uL", "display_name": "RBC"},
    "wbc": {"min": 4.0, "max": 11.0, "unit": "x10^3/uL", "display_name": "WBC"},
    "platelets": {"min": 150000, "max": 450000, "unit": "/uL", "display_name": "Platelets"},
    "hematocrit": {"min": 36.0, "max": 52.0, "unit": "%", "display_name": "Hematocrit"},
    "mcv": {"min": 80.0, "max": 100.0, "unit": "fL", "display_name": "MCV"},
    "mch": {"min": 27.0, "max": 33.0, "unit": "pg", "display_name": "MCH"},
    "mchc": {"min": 32.0, "max": 36.0, "unit": "g/dL", "display_name": "MCHC"},
    "rdw": {"min": 11.5, "max": 14.5, "unit": "%", "display_name": "RDW"},

    # Differential Count
    "neutrophils": {"min": 40.0, "max": 75.0, "unit": "%", "display_name": "Neutrophils"},
    "lymphocytes": {"min": 20.0, "max": 45.0, "unit": "%", "display_name": "Lymphocytes"},
    "monocytes": {"min": 2.0, "max": 10.0, "unit": "%", "display_name": "Monocytes"},
    "eosinophils": {"min": 1.0, "max": 6.0, "unit": "%", "display_name": "Eosinophils"},
    "basophils": {"min": 0.0, "max": 2.0, "unit": "%", "display_name": "Basophils"},

    # Metabolic
    "glucose": {"min": 70.0, "max": 140.0, "unit": "mg/dL", "display_name": "Glucose"},
    "creatinine": {"min": 0.6, "max": 1.3, "unit": "mg/dL", "display_name": "Creatinine"},
    "urea": {"min": 15.0, "max": 45.0, "unit": "mg/dL", "display_name": "Urea"},
    "sodium": {"min": 135.0, "max": 145.0, "unit": "mEq/L", "display_name": "Sodium"},
    "potassium": {"min": 3.5, "max": 5.1, "unit": "mEq/L", "display_name": "Potassium"},

    # Liver Function
    "bilirubin": {"min": 0.2, "max": 1.2, "unit": "mg/dL", "display_name": "Bilirubin"},
    "sgot": {"min": 5.0, "max": 40.0, "unit": "U/L", "display_name": "SGOT (AST)"},
    "sgpt": {"min": 7.0, "max": 56.0, "unit": "U/L", "display_name": "SGPT (ALT)"},
    "alp": {"min": 44.0, "max": 147.0, "unit": "U/L", "display_name": "ALP"},

    # Kidney Function
    "bun": {"min": 7.0, "max": 20.0, "unit": "mg/dL", "display_name": "BUN"},
    "egfr": {"min": 60.0, "max": 120.0, "unit": "mL/min/1.73m2", "display_name": "eGFR"}
}

# Regex patterns for matching blood parameter names
PARAM_PATTERNS = {
    "hemoglobin": r"\b(hemoglobin|hb|hgb)\b",
    "rbc": r"\b(rbc|red\s*blood\s*cell(s)?\s*(count)?|erythrocytes)\b",
    "wbc": r"\b(wbc|white\s*blood\s*cell(s)?\s*(count)?|leukocytes|tlc|total\s*leucocyte\s*count)\b",
    "platelets": r"\b(platelet(s)?\s*(count)?|plt)\b",
    "hematocrit": r"\b(hematocrit|hct|pcv|packed\s*cell\s*volume)\b",
    "mcv": r"\b(mcv|mean\s*corpuscular\s*volume)\b",
    "mch": r"\b(mch|mean\s*corpuscular\s*hemoglobin)\b",
    "mchc": r"\b(mchc|mean\s*corpuscular\s*hemoglobin\s*concentration)\b",
    "rdw": r"\b(rdw|red\s*cell\s*distribution\s*width(-cv|-sd)?)\b",

    "neutrophils": r"\b(neutrophils|neutrophil|neuts|polymorphs)\b",
    "lymphocytes": r"\b(lymphocytes|lymphocyte|lymphs)\b",
    "monocytes": r"\b(monocytes|monocyte|mono)\b",
    "eosinophils": r"\b(eosinophils|eosinophil|eos)\b",
    "basophils": r"\b(basophils|basophil|baso)\b",

    "glucose": r"\b(glucose|blood\s*glucose|fasting\s*glucose|random\s*glucose|serum\s*glucose|blood\s*sugar)\b",
    "creatinine": r"\b(creatinine|serum\s*creatinine)\b",
    "urea": r"\b(urea|serum\s*urea|blood\s*urea)\b",
    "sodium": r"\b(sodium|serum\s*sodium|na\+)\b",
    "potassium": r"\b(potassium|serum\s*potassium|k\+)\b",

    "bilirubin": r"\b(bilirubin|total\s*bilirubin|serum\s*bilirubin)\b",
    "sgot": r"\b(sgot|ast|aspartate\s*aminotransferase)\b",
    "sgpt": r"\b(sgpt|alt|alanine\s*aminotransferase)\b",
    "alp": r"\b(alp|alkaline\s*phosphatase)\b",

    "bun": r"\b(bun|blood\s*urea\s*nitrogen)\b",
    "egfr": r"\b(egfr|estimated\s*gfr|gfr)\b"
}


class BloodReportParser:
    """Standalone parser that extracts blood parameter values and compares them against reference ranges."""

    def evaluate_status(self, param_key: str, value: float) -> str:
        """Determines whether a value is Normal, High, or Low relative to reference ranges."""
        ref = REFERENCE_RANGES.get(param_key)
        if not ref:
            return "Normal"

        min_val = ref["min"]
        max_val = ref["max"]

        if value < min_val:
            return "Low"
        elif value > max_val:
            return "High"
        else:
            return "Normal"

    def parse_text(self, ocr_text: str) -> Tuple[Dict[str, ParameterDetail], OverallStatus]:
        """
        Parses OCR text line by line to extract known blood parameters, their values, units, and status.
        Returns (extracted_parameters_dict, overall_status).
        """
        extracted_params: Dict[str, ParameterDetail] = {}
        normal_count = 0
        high_count = 0
        low_count = 0

        lines = ocr_text.splitlines()

        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue

            lower_line = clean_line.lower()

            for param_key, pattern in PARAM_PATTERNS.items():
                if param_key in extracted_params:
                    continue  # Already extracted this parameter

                if re.search(pattern, lower_line, re.IGNORECASE):
                    # Search for numerical values in the line
                    # Matches numbers like 11.4, 280000, 13.5, 6.8, etc.
                    num_match = re.search(r"[:\s\-\=\|\t]+([0-9]+\.?[0-9]*)", lower_line)
                    if not num_match:
                        # Try finding any floating/int number in line
                        numbers = re.findall(r"\b[0-9]+\.?[0-9]*\b", lower_line)
                        if numbers:
                            # Avoid picking pure year or timestamp numbers if possible
                            val_str = numbers[0]
                        else:
                            val_str = None
                    else:
                        val_str = num_match.group(1)

                    if val_str:
                        try:
                            val = float(val_str)
                            # Handle platelets unit scaling if reported in thousands (e.g. 280 -> 280000)
                            if param_key == "platelets" and val < 1000:
                                val = val * 1000

                            ref = REFERENCE_RANGES[param_key]
                            status = self.evaluate_status(param_key, val)

                            if status == "Normal":
                                normal_count += 1
                            elif status == "High":
                                high_count += 1
                            elif status == "Low":
                                low_count += 1

                            extracted_params[param_key] = ParameterDetail(
                                value=val,
                                unit=ref["unit"],
                                status=status,
                                reference_range=f"{ref['min']}-{ref['max']} {ref['unit']}"
                            )
                            logger.info(f"Extracted parameter '{param_key}': value={val}, status={status}")
                        except ValueError:
                            continue

        overall_status = OverallStatus(
            normal=normal_count,
            high=high_count,
            low=low_count
        )

        return extracted_params, overall_status


blood_parser = BloodReportParser()
