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


def test_real_world_multiline_and_edge_cases():
    print("\n--- Test 5: Real-World Multiline & Edge Cases Test ---")
    ocr_text = """
    Hemoglobin
    10.5
    g/dL
    12.0 - 15.0

    Hematocrit
    42
    %
    36 - 52

    RBC
    5.16
    x10^6/uL
    4.0 - 6.1

    MCV
    66
    fL
    83-101

    MCH
    20
    pg
    27-33

    MCHC
    30.6
    g/dL
    32-36

    Total #BC Count
    6830
    cells/cumm
    4000-11000

    Platelet (ount
    160
    x10^3/uL
    150-450

    RDW-CV
    19.6
    %
    reference 11.6-14

    RDW-SD
    49
    fL
    39-46

    MPV
    10.6
    fL
    reference 7.4-10.4

    Absolute Neutrophil Count
    439.50
    cells/cumm
    Reference: 2000-7000

    Absolute Lymphocyte Count
    2.15
    x10^3/uL
    1.0-4.0
    """

    params, status = blood_parser.parse_text(ocr_text)

    print(f"Extracted {len(params)} parameters from real-world multiline OCR text.")
    print(f"Overall Status: Normal={status.normal}, High={status.high}, Low={status.low}")

    # ANC Verification
    assert "anc" in params, "Failed to extract ANC"
    assert params["anc"].value == 0.44, f"Expected ANC value 0.44 x10^3/uL, got {params['anc'].value}"
    assert params["anc"].status == "Low", f"Expected ANC status Low, got {params['anc'].status}"

    # MCV Verification
    assert "mcv" in params, "Failed to extract MCV"
    assert params["mcv"].value == 66.0, f"Expected MCV 66.0, got {params['mcv'].value}"
    assert params["mcv"].status == "Low", f"Expected MCV Low, got {params['mcv'].status}"

    # WBC Verification
    assert "wbc" in params, "Failed to extract WBC"
    assert params["wbc"].value == 6.83, f"Expected WBC 6.83, got {params['wbc'].value}"
    assert params["wbc"].status == "Normal", f"Expected WBC Normal, got {params['wbc'].status}"

    # Platelets Verification
    assert "platelets" in params, "Failed to extract Platelets"
    assert params["platelets"].value == 160000.0, f"Expected Platelet 160000, got {params['platelets'].value}"
    assert params["platelets"].status == "Normal", f"Expected Platelet Normal, got {params['platelets'].status}"

    # RDW-CV Verification
    assert "rdw_cv" in params, "Failed to extract RDW-CV"
    assert params["rdw_cv"].value == 19.6, f"Expected RDW-CV 19.6, got {params['rdw_cv'].value}"
    assert params["rdw_cv"].status == "High", f"Expected RDW-CV High, got {params['rdw_cv'].status}"

    # MPV Verification
    assert "mpv" in params, "Failed to extract MPV"
    assert params["mpv"].value == 10.6, f"Expected MPV 10.6, got {params['mpv'].value}"
    assert params["mpv"].status == "High", f"Expected MPV High, got {params['mpv'].status}"

    print("[PASSED] Test 5 Passed!")


if __name__ == "__main__":
    print("Running CBC Parser Tests...")
    test_standard_cbc_report()
    test_ocr_corrupted_report()
    test_scale_conversion()
    test_multi_line_and_partial()
    test_real_world_multiline_and_edge_cases()
    print("\nALL CBC PARSER TESTS PASSED SUCCESSFULLY!")

