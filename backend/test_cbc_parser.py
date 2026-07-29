"""
Unit Test Suite for Production CBC Blood Report Parser.
Run with: python backend/test_cbc_parser.py
"""

import os
import sys

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.blood_parser import blood_parser


def test_standard_cbc_report():
    print("\n--- Test 1: Standard Clean CBC Report ---")
    ocr_text = """
    COMPLETE BLOOD COUNT (CBC)
    Hemoglobin 14.2 g/dL (12.0 - 17.5)
    RBC Count 4.80 x10^6/uL (4.0 - 6.1)
    WBC Count 7.50 x10^3/uL (4.0 - 11.0)
    Platelet Count 250000 /uL (150000 - 450000)
    Hematocrit 42.0 % (36.0 - 52.0)
    MCV 88.0 fL (80.0 - 100.0)
    MCH 29.5 pg (27.0 - 33.0)
    MCHC 34.0 g/dL (32.0 - 36.0)
    RDW-CV 13.0 % (11.5 - 14.5)
    RDW-SD 42.0 fL (39.0 - 46.0)
    MPV 8.5 fL (7.4 - 10.4)

    DIFFERENTIAL COUNT
    Neutrophils 60.0 % (40.0 - 75.0)
    Lymphocytes 30.0 % (20.0 - 45.0)
    Monocytes 6.0 % (2.0 - 10.0)
    Eosinophils 3.0 % (1.0 - 6.0)
    Basophils 1.0 % (0.0 - 2.0)

    ABSOLUTE COUNTS
    Absolute Neutrophil Count 4.5 x10^3/uL (1.5 - 8.0)
    Absolute Lymphocyte Count 2.25 x10^3/uL (1.0 - 4.0)
    Absolute Monocyte Count 0.45 x10^3/uL (0.2 - 1.0)
    Absolute Eosinophil Count 0.22 x10^3/uL (0.05 - 0.5)
    Absolute Basophil Count 0.08 x10^3/uL (0.0 - 0.2)
    """

    params, status = blood_parser.parse_text(ocr_text)

    print(f"Extracted {len(params)} parameters out of 21 CBC parameters.")
    print(f"Overall Status: Normal={status.normal}, High={status.high}, Low={status.low}")

    assert len(params) == 21, f"Expected 21 parameters, got {len(params)}"
    assert status.normal == 21, f"Expected all 21 Normal, got Normal={status.normal}"
    assert params["hemoglobin"].value == 14.2
    assert params["platelets"].value == 250000
    assert params["anc"].value == 4.5
    print("[PASSED] Test 1 Passed!")


def test_ocr_corrupted_report():
    print("\n--- Test 2: OCR-Corrupted Misspellings & Printed Range Test ---")
    ocr_text = """
    Hcmoglobin 10.5 g/dL 12.0 - 15.0
    Total #BC Count 14.5 x10^3/uL 4.0 - 11.0
    Platelet (ount 120000 /uL 150000 - 450000
    PCV 32.0 % 36.0 - 52.0
    ANC 1.1 x10^3/uL 1.5 - 8.0
    ALC 0.8 x10^3/uL 1.0 - 4.0
    RDW-CV 15.5 % 11.5 - 14.5
    """

    params, status = blood_parser.parse_text(ocr_text)

    print(f"Extracted {len(params)} parameters.")
    print(f"Overall Status: Normal={status.normal}, High={status.high}, Low={status.low}")

    assert "hemoglobin" in params, "Failed to extract Hcmoglobin alias"
    assert params["hemoglobin"].value == 10.5
    assert params["hemoglobin"].status == "Low"

    assert "wbc" in params, "Failed to extract Total #BC Count alias"
    assert params["wbc"].value == 14.5
    assert params["wbc"].status == "High"

    assert "platelets" in params, "Failed to extract Platelet (ount alias"
    assert params["platelets"].value == 120000
    assert params["platelets"].status == "Low"

    assert "hematocrit" in params, "Failed to extract PCV alias"
    assert params["hematocrit"].value == 32.0
    assert params["hematocrit"].status == "Low"

    assert "anc" in params, "Failed to extract ANC alias"
    assert params["anc"].status == "Low"

    assert params["rdw_cv"].status == "High"

    assert status.low == 5, f"Expected 5 Low parameters, got {status.low}"
    assert status.high == 2, f"Expected 2 High parameters, got {status.high}"
    print("[PASSED] Test 2 Passed!")


def test_scale_conversion():
    print("\n--- Test 3: Unit Scale Normalization Test ---")
    ocr_text = """
    Total Leucocyte Count 8500 /uL
    Platelet Count 245 x10^3/uL
    """

    params, status = blood_parser.parse_text(ocr_text)

    assert "wbc" in params
    assert params["wbc"].value == 8.5  # Scaled 8500 /uL -> 8.5 x10^3/uL
    assert params["wbc"].status == "Normal"

    assert "platelets" in params
    assert params["platelets"].value == 245000  # Scaled 245 -> 245000 /uL
    assert params["platelets"].status == "Normal"

    print("[PASSED] Test 3 Passed!")


def test_multi_line_and_partial():
    print("\n--- Test 4: Multi-line & Partial Subset Test ---")
    ocr_text = """
    HAEMOGLOBIN
    11.2 g/dL

    TOTAL LEUCOCYTE COUNT
    12.8 x10^3/uL
    """

    params, status = blood_parser.parse_text(ocr_text)

    assert len(params) == 2
    assert params["hemoglobin"].value == 11.2
    assert params["hemoglobin"].status == "Low"
    assert params["wbc"].value == 12.8
    assert params["wbc"].status == "High"

    print("[PASSED] Test 4 Passed!")


if __name__ == "__main__":
    print("Running CBC Parser Tests...")
    test_standard_cbc_report()
    test_ocr_corrupted_report()
    test_scale_conversion()
    test_multi_line_and_partial()
    print("\nALL CBC PARSER TESTS PASSED SUCCESSFULLY!")
