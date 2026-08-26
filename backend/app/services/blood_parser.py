# import re
# import difflib
# from typing import Dict, Any, Tuple, Optional, List, TypedDict, Set
# from app.schemas.report import ParameterDetail, OverallStatus
# from app.core.logging import logger


# class ParameterConfig(TypedDict):
#     key: str
#     display_name: str
#     default_min: float
#     default_max: float
#     default_unit: str
#     exact_aliases: List[str]
#     regex_patterns: List[str]
#     fuzzy_targets: List[str]
#     priority: int


# # ──────────────────────────────────────────────────────────────
# # Modular Panel Configuration for CBC (21 Parameters)
# # ──────────────────────────────────────────────────────────────
# CBC_PANEL: List[ParameterConfig] = [
#     # ── Absolute Counts (Higher priority to avoid matching generic differential) ──
#     {
#         "key": "anc",
#         "display_name": "Absolute Neutrophils",
#         "default_min": 1.5,
#         "default_max": 8.0,
#         "default_unit": "x10^3/uL",
#         "exact_aliases": [
#             "anc", "absolute neutrophil count", "absolute neutrophils", "abs neutrophil",
#             "abs neutrophils", "abs. neutrophil", "absolule ncutrophil count", "absolute ncutrophil count"
#         ],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(absolu[te1l]+[\s\-_]*n[ecu1]+trophil(s)?(\s*count)?|anc|abs\.\s*neutrophil(s)?)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["absolute neutrophil count", "absolute neutrophils"],
#         "priority": 10
#     },
#     {
#         "key": "alc",
#         "display_name": "Absolute Lymphocytes",
#         "default_min": 1.0,
#         "default_max": 4.0,
#         "default_unit": "x10^3/uL",
#         "exact_aliases": [
#             "alc", "absolute lymphocyte count", "absolute lymphocytes", "abs lymphocyte",
#             "abs lymphocytes", "abs. lymphocyte", "absolutc lympbocytc count", "absolute lympbocyte count"
#         ],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(absolu[te1lc]+[\s\-_]*lymp[hboc1]+cyt[ec](\s*count)?|alc|abs\.\s*lymphocyte(s)?)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["absolute lymphocyte count", "absolute lymphocytes"],
#         "priority": 10
#     },
#     {
#         "key": "amc",
#         "display_name": "Absolute Monocytes",
#         "default_min": 0.2,
#         "default_max": 1.0,
#         "default_unit": "x10^3/uL",
#         "exact_aliases": ["amc", "absolute monocyte count", "absolute monocytes", "abs monocyte", "abs monocytes", "abs. monocyte"],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(absolute\s*monocyte(s)?(\s*count)?|amc|abs\.\s*monocyte(s)?)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["absolute monocyte count", "absolute monocytes"],
#         "priority": 10
#     },
#     {
#         "key": "aec",
#         "display_name": "Absolute Eosinophils",
#         "default_min": 0.05,
#         "default_max": 0.5,
#         "default_unit": "x10^3/uL",
#         "exact_aliases": ["aec", "absolute eosinophil count", "absolute eosinophils", "abs eosinophil", "abs eosinophils", "abs. eosinophil"],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(absolute\s*eosinophil(s)?(\s*count)?|aec|abs\.\s*eosinophil(s)?)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["absolute eosinophil count", "absolute eosinophils"],
#         "priority": 10
#     },
#     {
#         "key": "abc",
#         "display_name": "Absolute Basophils",
#         "default_min": 0.0,
#         "default_max": 0.2,
#         "default_unit": "x10^3/uL",
#         "exact_aliases": ["abc", "absolute basophil count", "absolute basophils", "abs basophil", "abs basophils", "abs. basophil"],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(absolute\s*basophil(s)?(\s*count)?|abc|abs\.\s*basophil(s)?)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["absolute basophil count", "absolute basophils"],
#         "priority": 10
#     },

#     # ── RDW Subtypes (Higher priority than generic RDW) ──
#     {
#         "key": "rdw_cv",
#         "display_name": "RDW-CV",
#         "default_min": 11.5,
#         "default_max": 14.5,
#         "default_unit": "%",
#         "exact_aliases": [
#             "rdw-cv", "rdw cv", "rdw_cv", "rdw(cv)", "red cell distribution width cv", "rdw - cv",
#             "ri)w-(t\"", "ri)w-(t", "rdw-(t", "rdw-(t\""
#         ],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(r[i1l\)]*w[\s\-_]*\(?[ctv]\"?|red\s*cell\s*distribution\s*width[\s\-_]*cv)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["red cell distribution width cv"],
#         "priority": 9
#     },
#     {
#         "key": "rdw_sd",
#         "display_name": "RDW-SD",
#         "default_min": 39.0,
#         "default_max": 46.0,
#         "default_unit": "fL",
#         "exact_aliases": ["rdw-sd", "rdw sd", "rdw_sd", "rdw(sd)", "red cell distribution width sd", "rdw - sd"],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(rdw[\s\-_]*sd|red\s*cell\s*distribution\s*width[\s\-_]*sd)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["red cell distribution width sd"],
#         "priority": 9
#     },

#     # ── Required Core Parameters ──
#     {
#         "key": "hemoglobin",
#         "display_name": "Hemoglobin",
#         "default_min": 12.0,
#         "default_max": 17.5,
#         "default_unit": "g/dL",
#         "exact_aliases": [
#             "hemoglobin", "hb", "hgb", "haemoglobin", "hcmoglobin", "harnoglobin",
#             "hemo-globin", "hemoglobi", "haemoglobi", "hemoglobn"
#         ],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(hemoglobin|haemoglobin|hcmoglobin|harnoglobin|hgb|hb)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["hemoglobin", "haemoglobin", "hcmoglobin", "harnoglobin"],
#         "priority": 8
#     },
#     {
#         "key": "hematocrit",
#         "display_name": "Hematocrit",
#         "default_min": 36.0,
#         "default_max": 52.0,
#         "default_unit": "%",
#         "exact_aliases": [
#             "hematocrit", "hct", "pcv", "packed cell volume", "hernatocrit",
#             "haematocrit", "hematocrit (pcv)", "packed cell vol", "tmhaematocrit", "hc tmhaematocrit"
#         ],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(hematocrit|haematocrit|hernatocrit|tmhaematocrit|hct|pcv|packed\s*cell\s*volume)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["hematocrit", "haematocrit", "packed cell volume", "hernatocrit"],
#         "priority": 8
#     },
#     {
#         "key": "rbc",
#         "display_name": "RBC Count",
#         "default_min": 4.0,
#         "default_max": 6.1,
#         "default_unit": "x10^6/uL",
#         "exact_aliases": [
#             "rbc", "rbc count", "red blood cell", "red blood cells", "red blood cell count",
#             "erythrocytes", "total rbc", "red cell count", "r.b.c."
#         ],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(rbc(\s*count)?|red\s*blood\s*cell(s)?(\s*count)?|erythrocytes|red\s*cell\s*count)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["red blood cell count", "erythrocytes count"],
#         "priority": 8
#     },
#     {
#         "key": "wbc",
#         "display_name": "WBC Count",
#         "default_min": 4.0,
#         "default_max": 11.0,
#         "default_unit": "x10^3/uL",
#         "exact_aliases": [
#             "wbc", "wbc count", "total wbc", "white blood cell", "white blood cells",
#             "white blood cell count", "leukocytes", "leucocytes", "tlc",
#             "total leucocyte count", "total leukocyte count", "#bc", "total #bc count",
#             "total #bc", "#bc count", "w.b.c.", "total #bc c ount", "total #bc count"
#         ],
#         "regex_patterns": [
#             r"(?<![a-zA-Z0-9])(wbc(\s*count)?|total\s*wbc|white\s*blood\s*cell(s)?(\s*count)?|leukocytes|leucocytes|tlc|total\s*leucocyte\s*count|total\s*leukocyte\s*count|#bc(\s*count)?|total\s*#bc(\s*c\s*ount)?)(?![a-zA-Z0-9])"
#         ],
#         "fuzzy_targets": ["white blood cell count", "total leucocyte count", "total leukocyte count"],
#         "priority": 8
#     },
#     {
#         "key": "platelets",
#         "display_name": "Platelet Count",
#         "default_min": 150000.0,
#         "default_max": 450000.0,
#         "default_unit": "/uL",
#         "exact_aliases": [
#             "platelet", "platelets", "platelet count", "total platelet count",
#             "plt", "platelet (ount", "platelet ( ount", "platelet count (plt)", "platlet", "platlets",
#             "thrombocytes", "plateletcount"
#         ],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(platelet(s)?(\s*c?\s*ount)?|plt|thrombocytes|platelet\s*\(\s*ount)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["platelet count", "total platelet count", "platelets count", "thrombocytes"],
#         "priority": 8
#     },
#     {
#         "key": "mcv",
#         "display_name": "MCV",
#         "default_min": 80.0,
#         "default_max": 100.0,
#         "default_unit": "fL",
#         "exact_aliases": ["mcv", "mct", "mean corpuscular volume", "m.c.v."],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(mcv|mct|mean\s*corpuscular\s*volume)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["mean corpuscular volume"],
#         "priority": 7
#     },
#     {
#         "key": "mch",
#         "display_name": "MCH",
#         "default_min": 27.0,
#         "default_max": 33.0,
#         "default_unit": "pg",
#         "exact_aliases": ["mch", "mean corpuscular hemoglobin", "mean corpuscular haemoglobin", "m.c.h."],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(mch|mean\s*corpuscular\s*hemoglobin|mean\s*corpuscular\s*haemoglobin)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["mean corpuscular hemoglobin"],
#         "priority": 7
#     },
#     {
#         "key": "mchc",
#         "display_name": "MCHC",
#         "default_min": 32.0,
#         "default_max": 36.0,
#         "default_unit": "g/dL",
#         "exact_aliases": [
#             "mchc", "mean corpuscular hemoglobin concentration",
#             "mean corpuscular haemoglobin concentration", "m.c.h.c."
#         ],
#         "regex_patterns": [
#             r"(?<![a-zA-Z0-9])(mchc|mean\s*corpuscular\s*hemoglobin\s*concentration|mean\s*corpuscular\s*haemoglobin\s*concentration)(?![a-zA-Z0-9])"
#         ],
#         "fuzzy_targets": ["mean corpuscular hemoglobin concentration"],
#         "priority": 7
#     },
#     {
#         "key": "mpv",
#         "display_name": "MPV",
#         "default_min": 7.4,
#         "default_max": 10.4,
#         "default_unit": "fL",
#         "exact_aliases": ["mpv", "mpi'", "mpi", "mean platelet volume", "m.p.v."],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(mpv|mpi\'?|mean\s*platelet\s*volume)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["mean platelet volume"],
#         "priority": 7
#     },

#     # ── Differential Count (% Parameters) ──
#     {
#         "key": "neutrophils",
#         "display_name": "Neutrophils",
#         "default_min": 40.0,
#         "default_max": 75.0,
#         "default_unit": "%",
#         "exact_aliases": ["neutrophils", "neutrophil", "ncutrophils", "neuts", "polymorphs", "segmented neutrophils", "neutro"],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(n[ecu1]+trophil(s)?|neuts|polymorphs)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["neutrophils count", "segmented neutrophils"],
#         "priority": 5
#     },
#     {
#         "key": "lymphocytes",
#         "display_name": "Lymphocytes",
#         "default_min": 20.0,
#         "default_max": 45.0,
#         "default_unit": "%",
#         "exact_aliases": ["lymphocytes", "lymphocyte", "lympbocytes", "lymphs", "lymph"],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(lymp[hboc1]+cyt[ec](s)?|lymphs)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["lymphocytes count"],
#         "priority": 5
#     },
#     {
#         "key": "monocytes",
#         "display_name": "Monocytes",
#         "default_min": 2.0,
#         "default_max": 10.0,
#         "default_unit": "%",
#         "exact_aliases": ["monocytes", "monocyte", "monocytcs", "mono"],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(monocyt[ec](s)?|mono)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["monocytes count"],
#         "priority": 5
#     },
#     {
#         "key": "eosinophils",
#         "display_name": "Eosinophils",
#         "default_min": 1.0,
#         "default_max": 6.0,
#         "default_unit": "%",
#         "exact_aliases": ["eosinophils", "eosinophil", "eosinopbils", "eos"],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(eosinop[hb]ils?|eos)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["eosinophils count"],
#         "priority": 5
#     },
#     {
#         "key": "basophils",
#         "display_name": "Basophils",
#         "default_min": 0.0,
#         "default_max": 2.0,
#         "default_unit": "%",
#         "exact_aliases": ["basophils", "basophil", "baso"],
#         "regex_patterns": [r"(?<![a-zA-Z0-9])(basophil(s)?|baso)(?![a-zA-Z0-9])"],
#         "fuzzy_targets": ["basophils count"],
#         "priority": 5
#     }
# ]

# # Collect set of all exact aliases across all parameters for lookup
# ALL_EXACT_ALIASES: Set[str] = set()
# for p in CBC_PANEL:
#     for alias in p["exact_aliases"]:
#         ALL_EXACT_ALIASES.add(alias.lower())

# CBC_PANEL_SORTED = sorted(CBC_PANEL, key=lambda x: x["priority"], reverse=True)


# class ExtractedParameterInternal(TypedDict):
#     value: float
#     unit: str
#     status: str
#     reference_range: str
#     match_type: str        # "exact_alias", "regex", "fuzzy"
#     match_confidence: float # 1.0, 0.95, or fuzzy score float (e.g. 0.84)
#     matched_alias: str


# class BloodReportParser:
#     """
#     Production-grade CBC blood report parser.
#     Uses multi-stage OCR matching (exact alias, regex, fuzzy difflib),
#     extracts printed reference ranges when available (falling back to default reference values),
#     performs unit scaling, and calculates status + overall status.
#     """

#     def __init__(self, panel_config: List[ParameterConfig] = CBC_PANEL_SORTED) -> None:
#         self.panel_config = panel_config

#     def _clean_line_text(self, line: str) -> str:
#         """Normalizes OCR line text for consistent matching."""
#         cleaned = line.strip().lower()
#         cleaned = re.sub(r"[\{\}\[\]]", "", cleaned)
#         return cleaned

#     def _extract_printed_reference_range(self, line: str) -> Optional[Tuple[float, float]]:
#         """
#         Attempts to parse printed reference range (e.g. "12.0 - 15.5", "12-15", "4.0 to 11.0") from an OCR line.
#         Handles OCR comma-decimal substitutions (e.g., "11,5 - 14,5" -> 11.5 - 14.5).
#         """
#         clean_l = re.sub(r"(\d+),(\d{1,2})\b", r"\1.\2", line)
#         range_match = re.search(r"\b([0-9]+\.?[0-9]*)\s*(?:[\-\–\—\~]|to)\s*([0-9]+\.?[0-9]*)\b", clean_l, re.IGNORECASE)
#         if range_match:
#             try:
#                 min_v = float(range_match.group(1))
#                 max_v = float(range_match.group(2))
#                 if min_v <= max_v:
#                     return (min_v, max_v)
#             except ValueError:
#                 pass
#         return None

#     def _extract_unit(self, line: str, default_unit: str) -> str:
#         """Extracts standard unit string from OCR line/context if present, else returns default_unit."""
#         unit_patterns = [
#             (r"\bx?10\^?6\s*[\/\u002f\u2044]\s*(?:ul|mm3|cumm|l)\b", "x10^6/uL"),
#             (r"\bx?10\^?3\s*[\/\u002f\u2044]\s*(?:ul|mm3|cumm|l)\b", "x10^3/uL"),
#             (r"\b(?:g\s*[\/\u002f\u2044]\s*dl|g%|gm\/dl|2\s*dl)\b", "g/dL"),
#             (r"\b(?:fl|femtoliter|femtolitres)\b", "fL"),
#             (r"\b(?:pg|picogram|picograms)\b", "pg"),
#             (r"\b(?:lakhs|lacs|lakh)\b", "Lakhs/uL"),
#             (r"%", "%"),
#             (r"\b(?:cell[s:]*|cumm|cu\s*mm|mm3|ul|cunun|cruutn)\b", "cells/cumm"),
#             (r"[\/\u002f\u2044]\s*(?:ul|mm3|cumm|cmm)\b", "/uL")
#         ]
#         line_lower = line.lower()
#         for pat, canonical in unit_patterns:
#             if re.search(pat, line_lower):
#                 return canonical
#         return default_unit

#     def _extract_numeric_value(self, line: str, printed_range: Optional[Tuple[float, float]]) -> Optional[float]:
#         """
#         Extracts the patient's test numerical value from the line/context,
#         excluding numbers that belong to the printed reference range or year tags.
#         Handles OCR comma decimal separators (e.g. 10,6 -> 10.6) and trailing OCR symbols (e.g. 66, 20.} 6830}).
#         Prioritizes numbers occurring before the reference range match.
#         """
#         if not line:
#             return None
#
#         clean_l = re.sub(r"(\d+),(\d{1,2})\b", r"\1.\2", line)
#
#         # Skip reference lines to avoid mistaking reference range numbers for result values
#         if "reference" in line.lower():
#             return None
#         range_match = re.search(r"\b[0-9]+\.?[0-9]*\s*(?:[\-\–\—\~]|to)\s*[0-9]+\.?[0-9]*\b", clean_l, re.IGNORECASE)
#         range_start_pos = range_match.start() if range_match else len(clean_l)
#
#         # Match numbers, stripping trailing punctuation like commas, braces, quotes
#         number_matches = list(re.finditer(r"\b[0-9]+\.?[0-9]*[,\}\"]?", clean_l))
#         if not number_matches:
#             return None
#
#         before_range_candidates: List[float] = []
#         fallback_candidates: List[float] = []
#
#         for m in number_matches:
#             num_raw = m.group(0).rstrip(',}"')
#             if not num_raw:
#                 continue
#             try:
#                 val = float(num_raw)
#                 # Ignore year tags
#                 if 2020 <= val <= 2030 and "." not in num_raw:
#                     continue
#                 # Ignore reference range bounds when they appear within the range regex
#                 if printed_range and (val == printed_range[0] or val == printed_range[1]):
#                     if m.start() >= range_start_pos:
#                         continue
#
#                 if m.start() < range_start_pos:
#                     before_range_candidates.append(val)
#                 else:
#                     fallback_candidates.append(val)
#             except ValueError:
#                 continue
#
#         if before_range_candidates:
#             return before_range_candidates[0]
#         elif fallback_candidates:
#             return fallback_candidates[0]
#
#         return None
#
#     def _match_parameter_in_line(self, line: str, config: ParameterConfig) -> Tuple[bool, str, float, str]:
#         """
#         Matches a single line against a parameter config using exact alias, regex, or fuzzy matching.
#         Returns (is_match, match_type, match_confidence, matched_alias_str).
#         """
#         lower_line = self._clean_line_text(line)
#
#         # 1. Exact Alias Match (using boundary lookarounds)
#         for alias in config["exact_aliases"]:
#             pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias) + r"(?![a-zA-Z0-9])"
#             if re.search(pattern, lower_line):
#                 return True, "exact_alias", 1.00, alias
#
#         # 2. Regex Pattern Match
#         for pattern in config["regex_patterns"]:
#             match = re.search(pattern, lower_line, re.IGNORECASE)
#             if match:
#                 return True, "regex", 0.95, match.group(0)
#
#         # 3. Fuzzy Matching using difflib
#         words = re.findall(r"[a-zA-Z0-9\(\)\#\-\_]+", lower_line)
#         candidates: List[str] = []
#         for i in range(len(words)):
#             cand1 = words[i]
#             if len(cand1) >= 4 and cand1 not in ALL_EXACT_ALIASES:
#                 candidates.append(cand1)
#             if i + 1 < len(words):
#                 cand2 = f"{words[i]} {words[i+1]}"
#                 if cand2 not in ALL_EXACT_ALIASES:
#                     candidates.append(cand2)
#             if i + 2 < len(words):
#                 cand3 = f"{words[i]} {words[i+1]} {words[i+2]}"
#                 if cand3 not in ALL_EXACT_ALIASES:
#                     candidates.append(cand3)
#
#         for target in config["fuzzy_targets"]:
#             for candidate in candidates:
#                 ratio = difflib.SequenceMatcher(None, candidate, target).ratio()
#                 if ratio >= 0.85:  # 85% similarity threshold
#                     return True, "fuzzy", round(ratio, 2), candidate
#
#         return False, "none", 0.0, ""
#
#     def _line_starts_another_parameter(self, line: str, current_key: str) -> bool:
#         """Returns True if line matches a parameter config other than current_key."""
#         for config in self.panel_config:
#             if config["key"] != current_key:
#                 is_match, _, _, _ = self._match_parameter_in_line(line, config)
#                 if is_match:
#                     return True
#         return False
#
#     def evaluate_status(self, value: float, min_val: float, max_val: float) -> str:
#         """Determines whether a value is Normal, High, or Low relative to reference range."""
#         if value < min_val:
#             return "Low"
#         elif value > max_val:
#             return "High"
#         else:
#             return "Normal"
#
#     def parse_text(self, ocr_text: str) -> Tuple[Dict[str, ParameterDetail], OverallStatus]:
#         """
#         Parses raw EasyOCR text output line by line (with contextual window across lines),
#         matching 21 CBC parameters, extracting printed reference ranges or using hardcoded defaults,
#         scaling values, and logging internal metadata & confidence scores.
#         """
#         extracted_internal: Dict[str, ExtractedParameterInternal] = {}
#         extracted_params: Dict[str, ParameterDetail] = {}
#
#         normal_count = 0
#         high_count = 0
#         low_count = 0
#         ignored_lines: List[str] = []
#
#         lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
#         num_lines = len(lines)
#
#         logger.info(f"BloodReportParser started: processing {num_lines} OCR lines")
#
#         for idx, line in enumerate(lines):
#             line_matched = False
#
#             for config in self.panel_config:
#                 param_key = config["key"]
#                 if param_key in extracted_internal:
#                     continue  # Parameter already extracted
#
#                 is_match, match_type, confidence, matched_alias = self._match_parameter_in_line(line, config)
#                 if not is_match:
#                     continue
#
#                 # Build context window of up to 4 lines (stopping if another parameter is encountered)
#                 context_lines = [line]
#                 for lookahead_idx in range(idx + 1, min(idx + 4, num_lines)):
#                     next_l = lines[lookahead_idx]
#                     if self._line_starts_another_parameter(next_l, param_key):
#                         break
#                     context_lines.append(next_l)
#
#                 context_str = " ".join(context_lines)
#
#                 # 1. Extract printed reference range from context
#                 printed_range = None
#                 for c_line in context_lines:
#                     printed_range = self._extract_printed_reference_range(c_line)
#                     if printed_range:
#                         break
#                 if not printed_range:
#                     printed_range = self._extract_printed_reference_range(context_str)
#
#                 # 2. Extract numeric value from context
#                 val = None
#                 for c_line in context_lines:
#                     val = self._extract_numeric_value(c_line, printed_range)
#                     if val is not None:
#                         break
#                 if val is None:
#                     val = self._extract_numeric_value(context_str, printed_range)
#
#                 if val is None:
#                     continue
#
#                 line_matched = True
#
#                 unit = self._extract_unit(context_str, config["default_unit"])
#
#                 # Determine reference range and apply scale conversions
#                 ref_min = config["default_min"]
#                 ref_max = config["default_max"]
#                 ref_source = "hardcoded_fallback"
#
#                 if printed_range:
#                     ref_min, ref_max = printed_range
#                     ref_source = "printed_report"
#
#                 # Scale Normalization Logic
#                 if param_key in ("wbc", "anc", "alc", "amc", "aec", "abc"):
#                     is_in_thousands = False
#                     if printed_range and ref_max > 100:
#                         is_in_thousands = True
#                     elif re.search(r"\b(?:cumm|cu\s*mm|mm3|cells)\b", unit.lower()):
#                         is_in_thousands = True
#                     elif val > 100 and not re.search(r"10\^?[36]|k\/", unit.lower()):
#                         is_in_thousands = True
#
#                     if is_in_thousands:
#                         if printed_range and ref_max > 100:
#                             ref_min = round(ref_min / 1000.0, 2)
#                             ref_max = round(ref_max / 1000.0, 2)
#                         val = round(val / 1000.0, 2)
#                         unit = "x10^3/uL"
#                 elif param_key == "platelets":
#                     unit = "/uL"
#                 elif param_key == "rbc":
#                     if printed_range and ref_max > 100:
#                         ref_min = round(ref_min / 1000000.0, 2)
#                         ref_max = round(ref_max / 1000000.0, 2)
#                     if val > 100:
#                         val = round(val / 1000000.0, 2)
#                     unit = "x10^6/uL"

#                 status = self.evaluate_status(val, ref_min, ref_max)
#                 ref_str = f"{ref_min}-{ref_max} {unit}"

#                 if status == "Normal":
#                     normal_count += 1
#                 elif status == "High":
#                     high_count += 1
#                 elif status == "Low":
#                     low_count += 1

#                 extracted_internal[param_key] = ExtractedParameterInternal(
#                     value=val,
#                     unit=unit,
#                     status=status,
#                     reference_range=ref_str,
#                     match_type=match_type,
#                     match_confidence=confidence,
#                     matched_alias=matched_alias
#                 )

#                 extracted_params[param_key] = ParameterDetail(
#                     value=val,
#                     unit=unit,
#                     status=status,
#                     reference_range=ref_str
#                 )

#                 logger.info(
#                     f"[Parser] Extracted '{config['display_name']}' ({param_key}): "
#                     f"val={val} {unit}, status={status}, match_type={match_type}, "
#                     f"confidence={confidence}, alias='{matched_alias}', ref_source={ref_source}"
#                 )
#                 break

#             if not line_matched and len(line) > 3:
#                 ignored_lines.append(line)

#         overall_status = OverallStatus(
#             normal=normal_count,
#             high=high_count,
#             low=low_count
#         )

#         logger.info(
#             f"BloodReportParser completed: extracted {len(extracted_params)} parameters "
#             f"({normal_count} Normal, {high_count} High, {low_count} Low). "
#             f"Ignored {len(ignored_lines)} unparsed lines."
#         )

#         return extracted_params, overall_status


# blood_parser = BloodReportParser()
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
        "exact_aliases": [
            "anc", "absolute neutrophil count", "absolute neutrophils", "abs neutrophil",
            "abs neutrophils", "abs. neutrophil", "absolule ncutrophil count", "absolute ncutrophil count"
        ],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(absolu[te1l]+[\s\-_]*n[ecu1]+trophil(s)?(\s*count)?|anc|abs\.\s*neutrophil(s)?)(?![a-zA-Z0-9])"],
        "fuzzy_targets": ["absolute neutrophil count", "absolute neutrophils"],
        "priority": 10
    },
    {
        "key": "alc",
        "display_name": "Absolute Lymphocytes",
        "default_min": 1.0,
        "default_max": 4.0,
        "default_unit": "x10^3/uL",
        "exact_aliases": [
            "alc", "absolute lymphocyte count", "absolute lymphocytes", "abs lymphocyte",
            "abs lymphocytes", "abs. lymphocyte", "absolutc lympbocytc count", "absolute lympbocyte count"
        ],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(absolu[te1lc]+[\s\-_]*lymp[hboc1]+cyt[ec](\s*count)?|alc|abs\.\s*lymphocyte(s)?)(?![a-zA-Z0-9])"],
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
        "regex_patterns": [r"(?<![a-zA-Z0-9])(absolute\s*monocyte(s)?(\s*count)?|amc|abs\.\s*monocyte(s)?)(?![a-zA-Z0-9])"],
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
        "regex_patterns": [r"(?<![a-zA-Z0-9])(absolute\s*eosinophil(s)?(\s*count)?|aec|abs\.\s*eosinophil(s)?)(?![a-zA-Z0-9])"],
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
        "regex_patterns": [r"(?<![a-zA-Z0-9])(absolute\s*basophil(s)?(\s*count)?|abc|abs\.\s*basophil(s)?)(?![a-zA-Z0-9])"],
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
        "exact_aliases": [
            "rdw-cv", "rdw cv", "rdw_cv", "rdw(cv)", "red cell distribution width cv", "rdw - cv",
            "ri)w-(t\"", "ri)w-(t", "rdw-(t", "rdw-(t\""
        ],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(r[i1l\)]*w[\s\-_]*\(?[ctv]\"?|red\s*cell\s*distribution\s*width[\s\-_]*cv)(?![a-zA-Z0-9])"],
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
        "regex_patterns": [r"(?<![a-zA-Z0-9])(rdw[\s\-_]*sd|red\s*cell\s*distribution\s*width[\s\-_]*sd)(?![a-zA-Z0-9])"],
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
        "regex_patterns": [r"(?<![a-zA-Z0-9])(hemoglobin|haemoglobin|hcmoglobin|harnoglobin|hgb|hb)(?![a-zA-Z0-9])"],
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
            "haematocrit", "hematocrit (pcv)", "packed cell vol", "tmhaematocrit", "hc tmhaematocrit"
        ],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(hematocrit|haematocrit|hernatocrit|tmhaematocrit|hct|pcv|packed\s*cell\s*volume)(?![a-zA-Z0-9])"],
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
        "regex_patterns": [r"(?<![a-zA-Z0-9])(rbc(\s*count)?|red\s*blood\s*cell(s)?(\s*count)?|erythrocytes|red\s*cell\s*count)(?![a-zA-Z0-9])"],
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
            "total #bc", "#bc count", "w.b.c.", "total #bc c ount", "total #bc count"
        ],
        "regex_patterns": [
            r"(?<![a-zA-Z0-9])(wbc(\s*count)?|total\s*wbc|white\s*blood\s*cell(s)?(\s*count)?|leukocytes|leucocytes|tlc|total\s*leucocyte\s*count|total\s*leukocyte\s*count|#bc(\s*count)?|total\s*#bc(\s*c\s*ount)?)(?![a-zA-Z0-9])"
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
            "plt", "platelet (ount", "platelet ( ount", "platelet count (plt)", "platlet", "platlets",
            "thrombocytes", "plateletcount"
        ],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(platelet(s)?(\s*c?\s*ount)?|plt|thrombocytes|platelet\s*\(\s*ount)(?![a-zA-Z0-9])"],
        "fuzzy_targets": ["platelet count", "total platelet count", "platelets count", "thrombocytes"],
        "priority": 8
    },
    {
        "key": "mcv",
        "display_name": "MCV",
        "default_min": 80.0,
        "default_max": 100.0,
        "default_unit": "fL",
        "exact_aliases": ["mcv", "mct", "mean corpuscular volume", "m.c.v."],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(mcv|mct|mean\s*corpuscular\s*volume)(?![a-zA-Z0-9])"],
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
        "regex_patterns": [r"(?<![a-zA-Z0-9])(mch|mean\s*corpuscular\s*hemoglobin|mean\s*corpuscular\s*haemoglobin)(?![a-zA-Z0-9])"],
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
            r"(?<![a-zA-Z0-9])(mchc|mean\s*corpuscular\s*hemoglobin\s*concentration|mean\s*corpuscular\s*haemoglobin\s*concentration)(?![a-zA-Z0-9])"
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
        "exact_aliases": ["mpv", "mpi'", "mpi", "mean platelet volume", "m.p.v."],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(mpv|mpi\'?|mean\s*platelet\s*volume)(?![a-zA-Z0-9])"],
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
        "exact_aliases": ["neutrophils", "neutrophil", "ncutrophils", "neuts", "polymorphs", "segmented neutrophils", "neutro"],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(n[ecu1]+trophil(s)?|neuts|polymorphs)(?![a-zA-Z0-9])"],
        "fuzzy_targets": ["neutrophils count", "segmented neutrophils"],
        "priority": 5
    },
    {
        "key": "lymphocytes",
        "display_name": "Lymphocytes",
        "default_min": 20.0,
        "default_max": 45.0,
        "default_unit": "%",
        "exact_aliases": ["lymphocytes", "lymphocyte", "lympbocytes", "lymphs", "lymph"],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(lymp[hboc1]+cyt[ec](s)?|lymphs)(?![a-zA-Z0-9])"],
        "fuzzy_targets": ["lymphocytes count"],
        "priority": 5
    },
    {
        "key": "monocytes",
        "display_name": "Monocytes",
        "default_min": 2.0,
        "default_max": 10.0,
        "default_unit": "%",
        "exact_aliases": ["monocytes", "monocyte", "monocytcs", "mono"],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(monocyt[ec](s)?|mono)(?![a-zA-Z0-9])"],
        "fuzzy_targets": ["monocytes count"],
        "priority": 5
    },
    {
        "key": "eosinophils",
        "display_name": "Eosinophils",
        "default_min": 1.0,
        "default_max": 6.0,
        "default_unit": "%",
        "exact_aliases": ["eosinophils", "eosinophil", "eosinopbils", "eos"],
        "regex_patterns": [r"(?<![a-zA-Z0-9])(eosinop[hb]ils?|eos)(?![a-zA-Z0-9])"],
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
        "regex_patterns": [r"(?<![a-zA-Z0-9])(basophil(s)?|baso)(?![a-zA-Z0-9])"],
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
    CBC blood-report parser with OCR-tolerant parameter matching.

    Important extraction rules:
    1. Prefer the patient's result immediately after the parameter name.
    2. Prefer a number immediately before the printed unit (% / g/dL / lakhs, etc.).
    3. Never use a printed reference-range number as the patient's result.
    4. Convert platelet "lakhs/cmm" values correctly:
           3.47 lakhs/cmm -> 347000 /uL
    5. Use printed reference ranges when available; otherwise use CBC_PANEL defaults.
    """

    def __init__(self, panel_config: List[ParameterConfig] = CBC_PANEL_SORTED) -> None:
        self.panel_config = panel_config

    def _clean_line_text(self, line: str) -> str:
        """Normalize OCR line text for consistent matching."""
        cleaned = line.strip().lower()
        cleaned = re.sub(r"[\{\}\[\]]", "", cleaned)
        return cleaned

    def _normalize_numbers(self, text: str) -> str:
        """
        Normalize common OCR number formatting:
        11,5 -> 11.5
        20,} -> 20
        """
        text = re.sub(r"(\d+),(\d{1,2})\b", r"\1.\2", text)
        text = re.sub(r"(?<=\d)[,}\"}]+", "", text)
        return text

    def _extract_printed_reference_range(
        self, line: str
    ) -> Optional[Tuple[float, float]]:
        """
        Extract ranges such as:
          12.0 - 15.5
          12-15
          4.0 to 11.0
          40)-Xu (40-80)
          20+40 (20-40)
          1,50-,14 (1.50-4.14)
          36.0-6.0 (36.0-46.0)

        Also handles OCR comma decimals.
        """
        if not line:
            return None

        clean_l = self._normalize_numbers(line)

        # Standard range pattern: 12.0 - 15.5, 40-80, 4.0 to 11.0, 20+40, 1.50-.14
        range_match = re.search(
            r"(?<!\d)"
            r"([0-9]+(?:\.[0-9]+)?)"
            r"\s*(?:-|–|—|~|\bto\b|\+)"
            r"\s*"
            r"(?:[0-9]*\.[0-9]+|[0-9]+)"
            r"(?!\d)",
            clean_l,
            re.IGNORECASE,
        )

        if range_match:
            try:
                lo = float(range_match.group(1))
                hi_str = re.search(r"(?:[0-9]*\.[0-9]+|[0-9]+)$", range_match.group(0))
                hi = float(hi_str.group(0)) if hi_str else lo
                if lo <= hi:
                    return lo, hi
                else:
                    return hi, lo
            except ValueError:
                pass

        # OCR-corrupted range patterns like 40)-Xu where upper bound was OCR-corrupted
        corrupted_range = re.search(
            r"\b([0-9]+(?:\.[0-9]+)?)\s*[\)\]\}]?\s*[-–—~+]\s*[A-Za-z0-9]+",
            clean_l,
        )
        if corrupted_range:
            try:
                lo = float(corrupted_range.group(1))
                return lo, lo
            except ValueError:
                pass

        return None

    def _extract_unit(self, line: str, default_unit: str) -> str:
        """Return a canonical unit detected in OCR text."""
        unit_patterns = [
            # Put lakh/lacs before generic cell/cumm patterns.
            (r"\b(?:lakhs|lacs|lakh)\b", "Lakhs/uL"),
            (r"\bx?10\^?6\s*[/⁄]\s*(?:ul|mm3|cumm|cmm|l)\b", "x10^6/uL"),
            (r"\bx?10\^?3\s*[/⁄]\s*(?:ul|mm3|cumm|cmm|l)\b", "x10^3/uL"),
            (r"\b(?:g\s*[/⁄]\s*dl|g%|gm\s*/\s*dl|g\s*dl)\b", "g/dL"),
            (r"\b(?:fl|femtoliter|femtolitres|femtoliters)\b", "fL"),
            (r"\b(?:pg|picogram|picograms)\b", "pg"),
            (r"%", "%"),
            (r"\b(?:cells?|cumm|cu\s*mm|mm3|ul)\b", "cells/cumm"),
            (r"[/⁄]\s*(?:ul|mm3|cumm|cmm)\b", "/uL"),
        ]

        lower = line.lower()
        for pattern, canonical in unit_patterns:
            if re.search(pattern, lower):
                return canonical

        return default_unit

    def _numeric_tokens(self, text: str) -> List[Tuple[float, int, int, str]]:
        """
        Return numeric tokens as:
            (value, start, end, raw_text)
        Masks out scientific notation multipliers (like 10^3, 10^6) to avoid false number tokens.
        """
        clean = self._normalize_numbers(text)

        # Mask scientific multipliers like 10^3, 10^6, 10³, 10⁶, x10^3, x10^6
        masked = re.sub(
            r"(?i)\b[xX]?10\s*[\^*/]?\s*[36]\b|10\s*[³⁶]",
            lambda m: " " * len(m.group(0)),
            clean,
        )

        tokens: List[Tuple[float, int, int, str]] = []

        # Decimal or integer.
        for m in re.finditer(
            r"(?<![A-Za-z0-9])\d+(?:\.\d+)?(?![A-Za-z0-9])", masked
        ):
            raw = m.group(0)
            try:
                value = float(raw)
            except ValueError:
                continue

            # Ignore likely years.
            if 2020 <= value <= 2030 and "." not in raw:
                continue

            tokens.append((value, m.start(), m.end(), raw))

        return tokens

    def _find_parameter_span(
        self, line: str, config: ParameterConfig
    ) -> Optional[Tuple[int, int]]:
        """Find the strongest parameter-name match in a line."""
        lower = self._clean_line_text(line)

        # Exact alias first.
        for alias in config["exact_aliases"]:
            pattern = (
                r"(?<![a-zA-Z0-9])"
                + re.escape(alias.lower())
                + r"(?![a-zA-Z0-9])"
            )
            m = re.search(pattern, lower)
            if m:
                return m.start(), m.end()

        # Regex next.
        for pattern in config["regex_patterns"]:
            m = re.search(pattern, lower, re.IGNORECASE)
            if m:
                return m.start(), m.end()

        return None

    def _extract_numeric_value(
        self,
        line: str,
        printed_range: Optional[Tuple[float, float]],
        config: ParameterConfig,
    ) -> Optional[float]:
        """
        Extract the patient's value from one OCR line.
        """
        if not line:
            return None

        clean = self._normalize_numbers(line)
        tokens = self._numeric_tokens(clean)
        if not tokens:
            return None

        # Check if line is purely a reference header/reference-only line
        lower_line = clean.lower()
        if any(kw in lower_line for kw in ("reference", "biological", "interval", "biological reference", "ref.")):
            param_span = self._find_parameter_span(clean, config)
            if not param_span:
                return None

        # Locate printed range spans to exclude reference range numbers
        range_spans: List[Tuple[int, int]] = []
        for rm in re.finditer(
            r"(?<!\d)[0-9]+(?:\.[0-9]+)?\s*(?:-|–|—|~|\bto\b|\+)\s*(?:[0-9]*\.[0-9]+|[0-9]+)(?!\d)|\b[0-9]+(?:\.[0-9]+)?\s*[\)\]\}]?\s*[-–—~+]\s*[A-Za-z0-9]+",
            clean,
            re.IGNORECASE,
        ):
            range_spans.append((rm.start(), rm.end()))

        param_span = self._find_parameter_span(clean, config)
        param_end = param_span[1] if param_span else -1

        unit_positions: List[int] = []
        unit_patterns = [
            r"%",
            r"\b(?:lakhs|lacs|lakh)\b",
            r"\b(?:g\s*[/⁄]\s*dl|g%|gm\s*/\s*dl)\b",
            r"\b(?:fl|pg)\b",
            r"\bx?10\^?[36]\b",
            r"[/⁄]\s*(?:ul|mm3|cumm|cmm)\b",
        ]
        for pattern in unit_patterns:
            for m in re.finditer(pattern, clean, re.IGNORECASE):
                unit_positions.append(m.start())

        candidates = []
        for value, start, end, raw in tokens:
            # Never select numbers belonging to the printed reference range
            in_range = any(
                r_start <= start < r_end or r_start < end <= r_end
                for r_start, r_end in range_spans
            )
            if in_range:
                continue

            # If printed range is known and this value matches printed range bounds on a line without unit
            if printed_range and (value == printed_range[0] or value == printed_range[1]):
                if not any(0 <= u - end <= 8 for u in unit_positions):
                    continue

            # For percentage parameters, reject impossible percentage values (> 100% or < 0%)
            if config["default_unit"] == "%" and not (0.0 <= value <= 100.0):
                continue

            # If hematocrit context lacks '%' and is adjacent to an invalid/corrupted range (e.g. 36.0-6.0), reject
            if config["key"] == "hematocrit" and "%" not in clean:
                if any(rm in clean for rm in ("36", "46", "36.0")):
                    continue

            after_parameter = param_span is None or start >= param_end

            if param_span:
                distance = start - param_end
            else:
                distance = start

            before_unit = any(0 <= u - end <= 8 for u in unit_positions)

            score = 0.0

            if after_parameter:
                score += 5.0
            else:
                score -= 4.0

            if before_unit:
                score += 7.0

            score += max(0.0, 3.0 - min(distance, 30) / 10.0)

            candidates.append((score, value, start))

        if not candidates:
            return None

        candidates.sort(key=lambda x: (-x[0], x[2]))
        return candidates[0][1]

    def _match_parameter_in_line(
        self, line: str, config: ParameterConfig
    ) -> Tuple[bool, str, float, str]:
        """
        Match using exact alias, regex, then fuzzy matching.
        """
        lower_line = self._clean_line_text(line)

        # 1. Exact alias
        for alias in config["exact_aliases"]:
            pattern = (
                r"(?<![a-zA-Z0-9])"
                + re.escape(alias.lower())
                + r"(?![a-zA-Z0-9])"
            )
            if re.search(pattern, lower_line):
                return True, "exact_alias", 1.00, alias

        # 2. Regex
        for pattern in config["regex_patterns"]:
            match = re.search(pattern, lower_line, re.IGNORECASE)
            if match:
                return True, "regex", 0.95, match.group(0)

        # 3. Fuzzy
        words = re.findall(r"[a-zA-Z0-9()#\-_]+", lower_line)
        candidates: List[str] = []

        for i in range(len(words)):
            cand1 = words[i]
            if len(cand1) >= 4 and cand1 not in ALL_EXACT_ALIASES:
                candidates.append(cand1)

            if i + 1 < len(words):
                candidates.append(f"{words[i]} {words[i + 1]}")

            if i + 2 < len(words):
                candidates.append(
                    f"{words[i]} {words[i + 1]} {words[i + 2]}"
                )

        best_ratio = 0.0
        best_candidate = ""

        for target in config["fuzzy_targets"]:
            for candidate in candidates:
                ratio = difflib.SequenceMatcher(
                    None, candidate, target
                ).ratio()

                if ratio > best_ratio:
                    best_ratio = ratio
                    best_candidate = candidate

        if best_ratio >= 0.85:
            return True, "fuzzy", round(best_ratio, 2), best_candidate

        return False, "none", 0.0, ""

    def _line_starts_another_parameter(
        self, line: str, current_key: str
    ) -> bool:
        """Return True if line matches a different CBC parameter."""
        for config in self.panel_config:
            if config["key"] == current_key:
                continue

            is_match, _, _, _ = self._match_parameter_in_line(
                line, config
            )
            if is_match:
                return True

        return False

    def evaluate_status(
        self, value: float, min_val: float, max_val: float
    ) -> str:
        """Return Normal, High, or Low."""
        if value < min_val:
            return "Low"
        if value > max_val:
            return "High"
        return "Normal"

    def _normalize_result_and_reference(
        self,
        param_key: str,
        value: float,
        ref_min: float,
        ref_max: float,
        unit: str,
    ) -> Tuple[float, float, float, str]:
        """
        Normalize result/reference into a consistent representation.

        Platelets:
          3.47 lakhs/cmm -> 347000 /uL
          150000 /uL     -> 150000 /uL
          3.47 x10^5/uL  -> 347000 /uL

        WBC/differential absolute counts:
          7500 /uL       -> 7.5 x10^3/uL
          6830 /cumm     -> 6.83 x10^3/uL
          439.50 /cumm   -> 0.44 x10^3/uL
          2147.30 /cumm  -> 2.15 x10^3/uL

        RBC:
          5.0 x10^6/uL   -> 5.0 x10^6/uL
          5000000 /uL    -> 5.0 x10^6/uL
        """
        unit_l = unit.lower()

        if param_key == "platelets":
            # Printed ranges such as 1.50-4.10 are lakhs/cmm; 150-450 are x10^3/uL.
            if ref_max <= 20.0:
                ref_min *= 100000.0
                ref_max *= 100000.0
            elif 20.0 < ref_max < 1000.0:
                ref_min *= 1000.0
                ref_max *= 1000.0

            if "lakh" in unit_l or "lac" in unit_l:
                value *= 100000.0
            elif "10^5" in unit_l or "10⁵" in unit_l:
                value *= 100000.0
            elif value <= 20.0:
                value *= 100000.0
            elif "10^3" in unit_l or "k" in unit_l or (20.0 < value < 1000.0):
                value *= 1000.0

            return (
                round(value, 2),
                round(ref_min, 2),
                round(ref_max, 2),
                "/uL",
            )

        if param_key in ("wbc", "anc", "alc", "amc", "aec", "abc"):
            # If the printed reference is 4500-11000, convert to 4.5-11.
            if ref_max > 100:
                ref_min /= 1000.0
                ref_max /= 1000.0

            if (
                "10^3" not in unit_l
                and "10³" not in unit_l
                and value > 100
            ) or value > 100:
                value /= 1000.0

            return (
                round(value, 2),
                round(ref_min, 2),
                round(ref_max, 2),
                "x10^3/uL",
            )

        if param_key == "rbc":
            if ref_max > 100:
                ref_min /= 1000000.0
                ref_max /= 1000000.0

            if (
                "10^6" not in unit_l
                and "10⁶" not in unit_l
                and value > 100
            ) or value > 100:
                value /= 1000000.0

            return (
                round(value, 2),
                round(ref_min, 2),
                round(ref_max, 2),
                "x10^6/uL",
            )

        return (
            round(value, 2),
            round(ref_min, 2),
            round(ref_max, 2),
            unit,
        )

    def parse_text(
        self, ocr_text: str
    ) -> Tuple[Dict[str, ParameterDetail], OverallStatus]:
        """
        Parse OCR text line-by-line with a short context window.

        The parser deliberately prefers values from the same line as the
        parameter. Context lines are only used when the result is split by OCR.
        """
        extracted_internal: Dict[str, ExtractedParameterInternal] = {}
        extracted_params: Dict[str, ParameterDetail] = {}

        normal_count = 0
        high_count = 0
        low_count = 0
        ignored_lines: List[str] = []

        lines = [
            line.strip()
            for line in ocr_text.splitlines()
            if line.strip()
        ]

        num_lines = len(lines)
        logger.info(
            f"BloodReportParser started: processing {num_lines} OCR lines"
        )

        for idx, line in enumerate(lines):
            line_matched = False

            for config in self.panel_config:
                param_key = config["key"]

                if param_key in extracted_internal:
                    continue

                is_match, match_type, confidence, matched_alias = (
                    self._match_parameter_in_line(line, config)
                )

                if not is_match:
                    continue

                # -------------------------------
                # 1. Prefer same-line extraction
                # -------------------------------
                printed_range = self._extract_printed_reference_range(line)

                val = self._extract_numeric_value(
                    line, printed_range, config
                )

                # -------------------------------
                # 2. If OCR split the row, inspect
                #    up to 3 following lines.
                # -------------------------------
                context_lines = [line]

                if val is None:
                    for lookahead_idx in range(
                        idx + 1, min(idx + 4, num_lines)
                    ):
                        next_line = lines[lookahead_idx]

                        if self._line_starts_another_parameter(
                            next_line, param_key
                        ):
                            break

                        context_lines.append(next_line)

                    context_str = " ".join(context_lines)
                    if printed_range is None:
                        printed_range = self._extract_printed_reference_range(
                            context_str
                        )

                    val = self._extract_numeric_value(
                        context_str, printed_range, config
                    )

                if val is None:
                    continue

                line_matched = True

                context_str = " ".join(context_lines)
                unit = self._extract_unit(
                    context_str, config["default_unit"]
                )

                # -------------------------------
                # 3. Reference range
                # -------------------------------
                ref_min = config["default_min"]
                ref_max = config["default_max"]
                ref_source = "hardcoded_fallback"

                if printed_range:
                    ref_min, ref_max = printed_range
                    ref_source = "printed_report"

                # -------------------------------
                # 4. Normalize result/reference
                # -------------------------------
                (
                    val,
                    ref_min,
                    ref_max,
                    unit,
                ) = self._normalize_result_and_reference(
                    param_key,
                    val,
                    ref_min,
                    ref_max,
                    unit,
                )

                status = self.evaluate_status(
                    val, ref_min, ref_max
                )

                ref_str = f"{ref_min:g}-{ref_max:g} {unit}"

                if status == "Normal":
                    normal_count += 1
                elif status == "High":
                    high_count += 1
                else:
                    low_count += 1

                extracted_internal[param_key] = (
                    ExtractedParameterInternal(
                        value=val,
                        unit=unit,
                        status=status,
                        reference_range=ref_str,
                        match_type=match_type,
                        match_confidence=confidence,
                        matched_alias=matched_alias,
                    )
                )

                extracted_params[param_key] = ParameterDetail(
                    value=val,
                    unit=unit,
                    status=status,
                    reference_range=ref_str,
                )

                logger.info(
                    f"[Parser] Extracted '{config['display_name']}' "
                    f"({param_key}): val={val} {unit}, "
                    f"status={status}, match_type={match_type}, "
                    f"confidence={confidence}, "
                    f"alias='{matched_alias}', "
                    f"ref_source={ref_source}"
                )

                break

            if not line_matched and len(line) > 3:
                ignored_lines.append(line)

        overall_status = OverallStatus(
            normal=normal_count,
            high=high_count,
            low=low_count,
        )

        logger.info(
            f"BloodReportParser completed: extracted "
            f"{len(extracted_params)} parameters "
            f"({normal_count} Normal, {high_count} High, "
            f"{low_count} Low). "
            f"Ignored {len(ignored_lines)} unparsed lines."
        )

        return extracted_params, overall_status


blood_parser = BloodReportParser()


