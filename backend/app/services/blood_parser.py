import re
import difflib
from typing import Dict, Any, Tuple, Optional, List, TypedDict, Set
from app.schemas.report import ParameterDetail, OverallStatus
from app.core.logging import logger


class ParameterConfig(TypedDict):
    key: str
    display_name: str
    default_min: float
    default_max: float
    default_unit: str
    exact_aliases: List[str]
    regex_patterns: List[str]
    fuzzy_targets: List[str]
    priority: int


# ──────────────────────────────────────────────────────────────
# Modular Panel Configuration for CBC (21 Parameters)
# ──────────────────────────────────────────────────────────────
CBC_PANEL: List[ParameterConfig] = [
    # ── Absolute Counts (Higher priority to avoid matching generic differential) ──
    {
        "key": "anc",
        "display_name": "Absolute Neutrophils",
        "default_min": 1.5,
        "default_max": 8.0,
        "default_unit": "x10^3/uL",
        "exact_aliases": ["anc", "absolute neutrophil count", "absolute neutrophils", "abs neutrophil", "abs neutrophils", "abs. neutrophil"],
        "regex_patterns": [r"\b(absolute\s*neutrophil(s)?(\s*count)?|anc|abs\.\s*neutrophil(s)?)\b"],
        "fuzzy_targets": ["absolute neutrophil count", "absolute neutrophils"],
        "priority": 10
    },
    {
        "key": "alc",
        "display_name": "Absolute Lymphocytes",
        "default_min": 1.0,
        "default_max": 4.0,
        "default_unit": "x10^3/uL",
        "exact_aliases": ["alc", "absolute lymphocyte count", "absolute lymphocytes", "abs lymphocyte", "abs lymphocytes", "abs. lymphocyte"],
        "regex_patterns": [r"\b(absolute\s*lymphocyte(s)?(\s*count)?|alc|abs\.\s*lymphocyte(s)?)\b"],
        "fuzzy_targets": ["absolute lymphocyte count", "absolute lymphocytes"],
        "priority": 10
    },
    {
        "key": "amc",
        "display_name": "Absolute Monocytes",
        "default_min": 0.2,
        "default_max": 1.0,
        "default_unit": "x10^3/uL",
        "exact_aliases": ["amc", "absolute monocyte count", "absolute monocytes", "abs monocyte", "abs monocytes", "abs. monocyte"],
        "regex_patterns": [r"\b(absolute\s*monocyte(s)?(\s*count)?|amc|abs\.\s*monocyte(s)?)\b"],
        "fuzzy_targets": ["absolute monocyte count", "absolute monocytes"],
        "priority": 10
    },
    {
        "key": "aec",
        "display_name": "Absolute Eosinophils",
        "default_min": 0.05,
        "default_max": 0.5,
        "default_unit": "x10^3/uL",
        "exact_aliases": ["aec", "absolute eosinophil count", "absolute eosinophils", "abs eosinophil", "abs eosinophils", "abs. eosinophil"],
        "regex_patterns": [r"\b(absolute\s*eosinophil(s)?(\s*count)?|aec|abs\.\s*eosinophil(s)?)\b"],
        "fuzzy_targets": ["absolute eosinophil count", "absolute eosinophils"],
        "priority": 10
    },
    {
        "key": "abc",
        "display_name": "Absolute Basophils",
        "default_min": 0.0,
        "default_max": 0.2,
        "default_unit": "x10^3/uL",
        "exact_aliases": ["abc", "absolute basophil count", "absolute basophils", "abs basophil", "abs basophils", "abs. basophil"],
        "regex_patterns": [r"\b(absolute\s*basophil(s)?(\s*count)?|abc|abs\.\s*basophil(s)?)\b"],
        "fuzzy_targets": ["absolute basophil count", "absolute basophils"],
        "priority": 10
    },

    # ── RDW Subtypes (Higher priority than generic RDW) ──
    {
        "key": "rdw_cv",
        "display_name": "RDW-CV",
        "default_min": 11.5,
        "default_max": 14.5,
        "default_unit": "%",
        "exact_aliases": ["rdw-cv", "rdw cv", "rdw_cv", "rdw(cv)", "red cell distribution width cv", "rdw - cv"],
        "regex_patterns": [r"\b(rdw[\s\-_]*cv|red\s*cell\s*distribution\s*width[\s\-_]*cv)\b"],
        "fuzzy_targets": ["red cell distribution width cv"],
        "priority": 9
    },
    {
        "key": "rdw_sd",
        "display_name": "RDW-SD",
        "default_min": 39.0,
        "default_max": 46.0,
        "default_unit": "fL",
        "exact_aliases": ["rdw-sd", "rdw sd", "rdw_sd", "rdw(sd)", "red cell distribution width sd", "rdw - sd"],
        "regex_patterns": [r"\b(rdw[\s\-_]*sd|red\s*cell\s*distribution\s*width[\s\-_]*sd)\b"],
        "fuzzy_targets": ["red cell distribution width sd"],
        "priority": 9
    },

    # ── Required Core Parameters ──
    {
        "key": "hemoglobin",
        "display_name": "Hemoglobin",
        "default_min": 12.0,
        "default_max": 17.5,
        "default_unit": "g/dL",
        "exact_aliases": [
            "hemoglobin", "hb", "hgb", "haemoglobin", "hcmoglobin", "harnoglobin",
            "hemo-globin", "hemoglobi", "haemoglobi", "hemoglobn"
        ],
        "regex_patterns": [r"\b(hemoglobin|haemoglobin|hcmoglobin|harnoglobin|hgb|hb)\b"],
        "fuzzy_targets": ["hemoglobin", "haemoglobin", "hcmoglobin", "harnoglobin"],
        "priority": 8
    },
    {
        "key": "hematocrit",
        "display_name": "Hematocrit",
        "default_min": 36.0,
        "default_max": 52.0,
        "default_unit": "%",
        "exact_aliases": [
            "hematocrit", "hct", "pcv", "packed cell volume", "hernatocrit",
            "haematocrit", "hematocrit (pcv)", "packed cell vol"
        ],
        "regex_patterns": [r"\b(hematocrit|haematocrit|hernatocrit|hct|pcv|packed\s*cell\s*volume)\b"],
        "fuzzy_targets": ["hematocrit", "haematocrit", "packed cell volume", "hernatocrit"],
        "priority": 8
    },
    {
        "key": "rbc",
        "display_name": "RBC Count",
        "default_min": 4.0,
        "default_max": 6.1,
        "default_unit": "x10^6/uL",
        "exact_aliases": [
            "rbc", "rbc count", "red blood cell", "red blood cells", "red blood cell count",
            "erythrocytes", "total rbc", "red cell count", "r.b.c."
        ],
        "regex_patterns": [r"\b(rbc(\s*count)?|red\s*blood\s*cell(s)?(\s*count)?|erythrocytes|red\s*cell\s*count)\b"],
        "fuzzy_targets": ["red blood cell count", "erythrocytes count"],
        "priority": 8
    },
    {
        "key": "wbc",
        "display_name": "WBC Count",
        "default_min": 4.0,
        "default_max": 11.0,
        "default_unit": "x10^3/uL",
        "exact_aliases": [
            "wbc", "wbc count", "total wbc", "white blood cell", "white blood cells",
            "white blood cell count", "leukocytes", "leucocytes", "tlc",
            "total leucocyte count", "total leukocyte count", "#bc", "total #bc count",
            "w.b.c."
        ],
        "regex_patterns": [
            r"\b(wbc(\s*count)?|total\s*wbc|white\s*blood\s*cell(s)?(\s*count)?|leukocytes|leucocytes|tlc|total\s*leucocyte\s*count|total\s*leukocyte\s*count|#bc(\s*count)?)\b"
        ],
        "fuzzy_targets": ["white blood cell count", "total leucocyte count", "total leukocyte count"],
        "priority": 8
    },
    {
        "key": "platelets",
        "display_name": "Platelet Count",
        "default_min": 150000.0,
        "default_max": 450000.0,
        "default_unit": "/uL",
        "exact_aliases": [
            "platelet", "platelets", "platelet count", "total platelet count",
            "plt", "platelet (ount", "platelet count (plt)", "platlet", "platlets",
            "thrombocytes", "plateletcount"
        ],
        "regex_patterns": [r"\b(platelet(s)?(\s*count)?|plt|thrombocytes|platelet\s*\(ount)\b"],
        "fuzzy_targets": ["platelet count", "total platelet count", "platelets count", "thrombocytes"],
        "priority": 8
    },
    {
        "key": "mcv",
        "display_name": "MCV",
        "default_min": 80.0,
        "default_max": 100.0,
        "default_unit": "fL",
        "exact_aliases": ["mcv", "mean corpuscular volume", "m.c.v."],
        "regex_patterns": [r"\b(mcv|mean\s*corpuscular\s*volume)\b"],
        "fuzzy_targets": ["mean corpuscular volume"],
        "priority": 7
    },
    {
        "key": "mch",
        "display_name": "MCH",
        "default_min": 27.0,
        "default_max": 33.0,
        "default_unit": "pg",
        "exact_aliases": ["mch", "mean corpuscular hemoglobin", "mean corpuscular haemoglobin", "m.c.h."],
        "regex_patterns": [r"\b(mch|mean\s*corpuscular\s*hemoglobin|mean\s*corpuscular\s*haemoglobin)\b"],
        "fuzzy_targets": ["mean corpuscular hemoglobin"],
        "priority": 7
    },
    {
        "key": "mchc",
        "display_name": "MCHC",
        "default_min": 32.0,
        "default_max": 36.0,
        "default_unit": "g/dL",
        "exact_aliases": [
            "mchc", "mean corpuscular hemoglobin concentration",
            "mean corpuscular haemoglobin concentration", "m.c.h.c."
        ],
        "regex_patterns": [
            r"\b(mchc|mean\s*corpuscular\s*hemoglobin\s*concentration|mean\s*corpuscular\s*haemoglobin\s*concentration)\b"
        ],
        "fuzzy_targets": ["mean corpuscular hemoglobin concentration"],
        "priority": 7
    },
    {
        "key": "mpv",
        "display_name": "MPV",
        "default_min": 7.4,
        "default_max": 10.4,
        "default_unit": "fL",
        "exact_aliases": ["mpv", "mean platelet volume", "m.p.v."],
        "regex_patterns": [r"\b(mpv|mean\s*platelet\s*volume)\b"],
        "fuzzy_targets": ["mean platelet volume"],
        "priority": 7
    },

    # ── Differential Count (% Parameters) ──
    {
        "key": "neutrophils",
        "display_name": "Neutrophils",
        "default_min": 40.0,
        "default_max": 75.0,
        "default_unit": "%",
        "exact_aliases": ["neutrophils", "neutrophil", "neuts", "polymorphs", "segmented neutrophils", "neutro"],
        "regex_patterns": [r"\b(neutrophil(s)?|neuts|polymorphs)\b"],
        "fuzzy_targets": ["neutrophils count", "segmented neutrophils"],
        "priority": 5
    },
    {
        "key": "lymphocytes",
        "display_name": "Lymphocytes",
        "default_min": 20.0,
        "default_max": 45.0,
        "default_unit": "%",
        "exact_aliases": ["lymphocytes", "lymphocyte", "lymphs", "lymph"],
        "regex_patterns": [r"\b(lymphocyte(s)?|lymphs)\b"],
        "fuzzy_targets": ["lymphocytes count"],
        "priority": 5
    },
    {
        "key": "monocytes",
        "display_name": "Monocytes",
        "default_min": 2.0,
        "default_max": 10.0,
        "default_unit": "%",
        "exact_aliases": ["monocytes", "monocyte", "mono"],
        "regex_patterns": [r"\b(monocyte(s)?|mono)\b"],
        "fuzzy_targets": ["monocytes count"],
        "priority": 5
    },
    {
        "key": "eosinophils",
        "display_name": "Eosinophils",
        "default_min": 1.0,
        "default_max": 6.0,
        "default_unit": "%",
        "exact_aliases": ["eosinophils", "eosinophil", "eos"],
        "regex_patterns": [r"\b(eosinophil(s)?|eos)\b"],
        "fuzzy_targets": ["eosinophils count"],
        "priority": 5
    },
    {
        "key": "basophils",
        "display_name": "Basophils",
        "default_min": 0.0,
        "default_max": 2.0,
        "default_unit": "%",
        "exact_aliases": ["basophils", "basophil", "baso"],
        "regex_patterns": [r"\b(basophil(s)?|baso)\b"],
        "fuzzy_targets": ["basophils count"],
        "priority": 5
    }
]

# Collect set of all exact aliases across all parameters for lookup
ALL_EXACT_ALIASES: Set[str] = set()
for p in CBC_PANEL:
    for alias in p["exact_aliases"]:
        ALL_EXACT_ALIASES.add(alias.lower())

CBC_PANEL_SORTED = sorted(CBC_PANEL, key=lambda x: x["priority"], reverse=True)


class ExtractedParameterInternal(TypedDict):
    value: float
    unit: str
    status: str
    reference_range: str
    match_type: str        # "exact_alias", "regex", "fuzzy"
    match_confidence: float # 1.0, 0.95, or fuzzy score float (e.g. 0.84)
    matched_alias: str


class BloodReportParser:
    """
    Production-grade CBC blood report parser.
    Uses multi-stage OCR matching (exact alias, regex, fuzzy difflib),
    extracts printed reference ranges when available (falling back to default reference values),
    performs unit scaling, and calculates status + overall status.
    """

    def __init__(self, panel_config: List[ParameterConfig] = CBC_PANEL_SORTED) -> None:
        self.panel_config = panel_config

    def _clean_line_text(self, line: str) -> str:
        """Normalizes OCR line text for consistent matching."""
        cleaned = line.strip().lower()
        cleaned = re.sub(r"[\{\}\[\]]", "", cleaned)
        return cleaned

    def _extract_printed_reference_range(self, line: str) -> Optional[Tuple[float, float]]:
        """
        Attempts to parse printed reference range (e.g. "12.0 - 15.5", "12-15", "4.0 to 11.0") from an OCR line.
        """
        range_match = re.search(r"\b([0-9]+\.?[0-9]*)\s*(?:[\-\–\—\~]|to)\s*([0-9]+\.?[0-9]*)\b", line, re.IGNORECASE)
        if range_match:
            try:
                min_v = float(range_match.group(1))
                max_v = float(range_match.group(2))
                if min_v <= max_v:
                    return (min_v, max_v)
            except ValueError:
                pass
        return None

    def _extract_unit(self, line: str, default_unit: str) -> str:
        """Extracts standard unit string from OCR line if present, else returns default_unit."""
        unit_patterns = [
            (r"\bx?10\^?6\s*[\/\u002f\u2044]\s*(?:ul|mm3|cumm|l)\b", "x10^6/uL"),
            (r"\bx?10\^?3\s*[\/\u002f\u2044]\s*(?:ul|mm3|cumm|l)\b", "x10^3/uL"),
            (r"\b(?:g\s*[\/\u002f\u2044]\s*dl|g%|gm\/dl)\b", "g/dL"),
            (r"\b(?:fl|femtoliter|femtolitres)\b", "fL"),
            (r"\b(?:pg|picogram|picograms)\b", "pg"),
            (r"\b(?:lakhs|lacs)\b", "Lakhs/uL"),
            (r"%", "%"),
            (r"[\/\u002f\u2044]\s*(?:ul|mm3|cumm|cmm)\b", "/uL")
        ]
        line_lower = line.lower()
        for pat, canonical in unit_patterns:
            if re.search(pat, line_lower):
                return canonical
        return default_unit

    def _extract_numeric_value(self, line: str, printed_range: Optional[Tuple[float, float]]) -> Optional[float]:
        """
        Extracts the patient's test numerical value from the line,
        excluding numbers that belong to the printed reference range or year tags.
        """
        numbers_found = re.findall(r"\b[0-9]+\.?[0-9]*\b", line)
        if not numbers_found:
            return None

        valid_candidates: List[float] = []
        for num_str in numbers_found:
            try:
                val = float(num_str)
                if 2020 <= val <= 2030 and "." not in num_str:
                    continue
                if printed_range and (val == printed_range[0] or val == printed_range[1]):
                    continue
                valid_candidates.append(val)
            except ValueError:
                continue

        if valid_candidates:
            return valid_candidates[0]

        return None

    def _match_parameter_in_line(self, line: str, config: ParameterConfig) -> Tuple[bool, str, float, str]:
        """
        Matches a single line against a parameter config using exact alias, regex, or fuzzy matching.
        Returns (is_match, match_type, match_confidence, matched_alias_str).
        """
        lower_line = self._clean_line_text(line)

        # 1. Exact Alias Match
        for alias in config["exact_aliases"]:
            pattern = r"\b" + re.escape(alias) + r"\b"
            if re.search(pattern, lower_line):
                return True, "exact_alias", 1.00, alias

        # 2. Regex Pattern Match
        for pattern in config["regex_patterns"]:
            match = re.search(pattern, lower_line, re.IGNORECASE)
            if match:
                return True, "regex", 0.95, match.group(0)

        # 3. Fuzzy Matching using difflib
        words = re.findall(r"\b[a-zA-Z\(\)\#\-\_]+\b", lower_line)
        candidates: List[str] = []
        for i in range(len(words)):
            cand1 = words[i]
            if len(cand1) >= 4 and cand1 not in ALL_EXACT_ALIASES:
                candidates.append(cand1)
            if i + 1 < len(words):
                cand2 = f"{words[i]} {words[i+1]}"
                if cand2 not in ALL_EXACT_ALIASES:
                    candidates.append(cand2)
            if i + 2 < len(words):
                cand3 = f"{words[i]} {words[i+1]} {words[i+2]}"
                if cand3 not in ALL_EXACT_ALIASES:
                    candidates.append(cand3)

        for target in config["fuzzy_targets"]:
            for candidate in candidates:
                ratio = difflib.SequenceMatcher(None, candidate, target).ratio()
                if ratio >= 0.85:  # 85% similarity threshold
                    return True, "fuzzy", round(ratio, 2), candidate

        return False, "none", 0.0, ""

    def evaluate_status(self, value: float, min_val: float, max_val: float) -> str:
        """Determines whether a value is Normal, High, or Low relative to reference range."""
        if value < min_val:
            return "Low"
        elif value > max_val:
            return "High"
        else:
            return "Normal"

    def parse_text(self, ocr_text: str) -> Tuple[Dict[str, ParameterDetail], OverallStatus]:
        """
        Parses raw EasyOCR text output line by line, matching 21 CBC parameters,
        extracting printed reference ranges or using hardcoded defaults, scaling values,
        and logging internal metadata & confidence scores.
        """
        extracted_internal: Dict[str, ExtractedParameterInternal] = {}
        extracted_params: Dict[str, ParameterDetail] = {}

        normal_count = 0
        high_count = 0
        low_count = 0
        ignored_lines: List[str] = []

        lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
        num_lines = len(lines)

        logger.info(f"BloodReportParser started: processing {num_lines} OCR lines")

        for idx, line in enumerate(lines):
            line_matched = False

            for config in self.panel_config:
                param_key = config["key"]
                if param_key in extracted_internal:
                    continue  # Parameter already extracted

                is_match, match_type, confidence, matched_alias = self._match_parameter_in_line(line, config)
                if not is_match:
                    continue

                printed_range = self._extract_printed_reference_range(line)
                val = self._extract_numeric_value(line, printed_range)

                if val is None and idx + 1 < num_lines:
                    next_line = lines[idx + 1]
                    printed_range = printed_range or self._extract_printed_reference_range(next_line)
                    val = self._extract_numeric_value(next_line, printed_range)

                if val is None:
                    continue

                line_matched = True

                if printed_range:
                    ref_min, ref_max = printed_range
                    ref_source = "printed_report"
                else:
                    ref_min = config["default_min"]
                    ref_max = config["default_max"]
                    ref_source = "hardcoded_fallback"

                unit = self._extract_unit(line, config["default_unit"])

                if param_key == "platelets":
                    if ref_max >= 100000:
                        if val < 25:
                            val = val * 100000.0
                        elif val < 1000:
                            val = val * 1000.0
                elif param_key in ("wbc", "anc", "alc", "amc", "aec", "abc"):
                    if ref_max <= 50 and val > 500:
                        val = round(val / 1000.0, 2)
                    elif ref_max > 500 and val <= 50:
                        val = round(val * 1000.0, 2)

                status = self.evaluate_status(val, ref_min, ref_max)
                ref_str = f"{ref_min}-{ref_max} {unit}"

                if status == "Normal":
                    normal_count += 1
                elif status == "High":
                    high_count += 1
                elif status == "Low":
                    low_count += 1

                extracted_internal[param_key] = ExtractedParameterInternal(
                    value=val,
                    unit=unit,
                    status=status,
                    reference_range=ref_str,
                    match_type=match_type,
                    match_confidence=confidence,
                    matched_alias=matched_alias
                )

                extracted_params[param_key] = ParameterDetail(
                    value=val,
                    unit=unit,
                    status=status,
                    reference_range=ref_str
                )

                logger.info(
                    f"[Parser] Extracted '{config['display_name']}' ({param_key}): "
                    f"val={val} {unit}, status={status}, match_type={match_type}, "
                    f"confidence={confidence}, alias='{matched_alias}', ref_source={ref_source}"
                )
                break

            if not line_matched and len(line) > 3:
                ignored_lines.append(line)

        overall_status = OverallStatus(
            normal=normal_count,
            high=high_count,
            low=low_count
        )

        logger.info(
            f"BloodReportParser completed: extracted {len(extracted_params)} parameters "
            f"({normal_count} Normal, {high_count} High, {low_count} Low). "
            f"Ignored {len(ignored_lines)} unparsed lines."
        )

        return extracted_params, overall_status


blood_parser = BloodReportParser()
