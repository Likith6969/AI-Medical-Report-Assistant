"""
Gemini AI Service — Blood Report Educational Summary Generator

Calls the Gemini REST API with structured blood parameter data
and returns a plain-English, educational summary string.

Design contract:
  - Input:  Dict[str, ParameterDetail], OverallStatus
  - Output: str | None  (NEVER raises — always returns safely)
  - Never sends raw OCR text to Gemini — only structured data
  - Timeout + retry handled internally
"""

import time
import requests
from typing import Dict, Optional

from app.schemas.report import ParameterDetail, OverallStatus
from app.core.logging import logger


# ──────────────────────────────────────────────────────────────
# Gemini REST endpoint template
# ──────────────────────────────────────────────────────────────
_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models"
    "/{model}:generateContent"
)

# Status emoji for prompt readability (Gemini sees these too — improves output)
_STATUS_LABEL = {
    "Normal": "✓ NORMAL",
    "High":   "↑ HIGH",
    "Low":    "↓ LOW",
}


class GeminiService:
    """
    Isolated service that generates an AI-powered educational summary
    for a blood report from structured parameter data.

    Usage:
        summary = gemini_service.generate_summary(parameters, overall_status)
    """

    def __init__(self) -> None:
        # Config is imported lazily inside methods to avoid circular imports
        # and to allow unit tests to patch settings cleanly.
        self._settings = None

    # ── Internal helpers ─────────────────────────────────────────

    def _get_settings(self):
        if self._settings is None:
            from app.core.config import settings
            self._settings = settings
        return self._settings

    def _build_prompt(
        self,
        parameters: Dict[str, ParameterDetail],
        overall_status: OverallStatus,
    ) -> str:
        """
        Builds a structured, injection-safe prompt from ParameterDetail objects.
        Raw OCR text is NEVER included.
        """
        lines = []

        # Separate abnormal from normal for clearer prompt structure
        abnormal = {k: v for k, v in parameters.items() if v.status != "Normal"}
        normal   = {k: v for k, v in parameters.items() if v.status == "Normal"}

        lines.append("=== BLOOD TEST RESULTS (Structured Data) ===\n")

        if abnormal:
            lines.append("ABNORMAL PARAMETERS:")
            for key, detail in abnormal.items():
                label = _STATUS_LABEL.get(detail.status, detail.status)
                ref   = detail.reference_range or "N/A"
                lines.append(
                    f"  • {key.upper()}: {detail.value} {detail.unit or ''}"
                    f" → {label}  (Reference: {ref})"
                )

        if normal:
            lines.append("\nNORMAL PARAMETERS:")
            normal_names = ", ".join(k.upper() for k in normal.keys())
            lines.append(f"  {normal_names}")

        lines.append(
            f"\nSummary counts: "
            f"{overall_status.normal} Normal | "
            f"{overall_status.high} High | "
            f"{overall_status.low} Low"
        )

        lines.append("\n=== INSTRUCTIONS ===\n")
        lines.append(
            "You are a health education assistant. Your role is strictly educational. "
            "You must NEVER diagnose, prescribe, or suggest medication.\n\n"
            "Write a clear, warm, and informative blood report summary with these sections:\n\n"
            "1. NORMAL PARAMETERS (1 sentence): Briefly mention which values are within range.\n\n"
            "2. ABNORMAL PARAMETERS (1–2 sentences per parameter): For each abnormal value:\n"
            "   - Explain in plain English what the parameter measures.\n"
            "   - Describe what being high or low may generally indicate in simple terms.\n"
            "   - Suggest a relevant, general lifestyle consideration if appropriate "
            "(e.g., hydration, diet, rest) — never medication.\n\n"
            "3. DISCLAIMER: End with a clear medical disclaimer recommending that the reader "
            "consult a qualified healthcare professional for proper interpretation and guidance.\n\n"
            "Rules:\n"
            "- No diagnosis. No prescriptions. No alarming language.\n"
            "- Plain English only — no medical jargon.\n"
            "- Warm, reassuring, and informative tone.\n"
            "- Write in flowing paragraphs (avoid bullet lists in your output).\n"
            "- Total length: 180–250 words."
        )

        return "\n".join(lines)

    def _call_gemini(self, prompt: str, api_key: str, model: str, timeout: int) -> Optional[str]:
        """
        Makes a single HTTP request to the Gemini REST API via x-goog-api-key header.
        Returns the response text or None on failure.
        """
        url = _GEMINI_URL.format(model=model)
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,       # Slightly creative but factual
                "maxOutputTokens": 512,   # ~250 words
                "topP": 0.9,
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }

        response = requests.post(url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()

        data = response.json()

        candidates = data.get("candidates", [])
        if not candidates:
            logger.warning("Gemini returned no candidates in response")
            return None

        content = candidates[0].get("content", {})
        parts   = content.get("parts", [])
        if not parts:
            logger.warning("Gemini candidate contained no parts")
            return None

        text = parts[0].get("text", "").strip()
        if not text:
            logger.warning("Gemini returned empty text in response part")
            return None

        return text

    # ── Public API ────────────────────────────────────────────────

    def generate_summary(
        self,
        parameters: Dict[str, ParameterDetail],
        overall_status: OverallStatus,
    ) -> Optional[str]:
        """
        Generates an educational AI summary for a blood report.

        Args:
            parameters:     Extracted blood parameters (from blood_parser)
            overall_status: Normal/High/Low counts (from blood_parser)

        Returns:
            str   — AI-generated educational summary
            None  — if Gemini is unavailable, not configured, or fails

        This method NEVER raises. All exceptions are caught and logged.
        OCR pipeline integrity is always preserved.
        """
        cfg = self._get_settings()

        # ── Guard: API key missing or default placeholder ────────
        if not cfg.GEMINI_API_KEY or cfg.GEMINI_API_KEY in ("your_gemini_api_key_here", "YOUR_GEMINI_API_KEY"):
            logger.warning(
                "Gemini API key not configured or set to placeholder. "
                "Skipping AI summary — returning null."
            )
            return None

        # ── Guard: No parameters extracted ───────────────────────
        if not parameters:
            logger.warning("No blood parameters available — skipping Gemini summary.")
            return None

        prompt  = self._build_prompt(parameters, overall_status)
        model   = cfg.GEMINI_MODEL
        timeout = cfg.GEMINI_TIMEOUT_SECONDS
        retries = cfg.GEMINI_MAX_RETRIES

        last_error: Optional[Exception] = None

        logger.info(
            f"Calling Gemini API ({model}) for blood report summary — "
            f"{len(parameters)} parameters, timeout={timeout}s, max_retries={retries}"
        )

        for attempt in range(1, retries + 2):   # retries + 1 total attempts
            try:
                summary = self._call_gemini(prompt, cfg.GEMINI_API_KEY, model, timeout)
                if summary:
                    logger.info(
                        f"Gemini summary generated successfully "
                        f"(attempt {attempt}, {len(summary)} chars)"
                    )
                    return summary
                else:
                    # _call_gemini returned None (empty response) — no point retrying
                    return None

            except requests.Timeout as exc:
                last_error = exc
                logger.warning(
                    f"Gemini request timed out "
                    f"(attempt {attempt}/{retries + 1}, timeout={timeout}s)"
                )

            except requests.HTTPError as exc:
                last_error = exc
                status_code = exc.response.status_code if exc.response is not None else "?"
                err_msg = ""
                if exc.response is not None:
                    try:
                        err_msg = exc.response.json().get("error", {}).get("message", "")
                    except Exception:
                        err_msg = exc.response.text[:100]

                logger.warning(
                    f"Gemini HTTP error {status_code} "
                    f"(attempt {attempt}/{retries + 1}): {err_msg or 'HTTP error'}"
                )

                # API key invalid — no point retrying
                if status_code in (400, 403) and "api key" in err_msg.lower():
                    logger.error("Gemini API key is invalid. Aborting retries.")
                    return None

                # Quota exhausted — no point retrying within this request
                if status_code == 429:
                    logger.warning("Gemini quota exhausted (429). Returning ai_summary=null.")
                    return None

                # Other non-retryable client errors
                if status_code in (400, 403, 404):
                    logger.error(
                        f"Gemini non-retryable error {status_code} "
                        f"({err_msg or 'see above'}). Aborting retries."
                    )
                    return None

            except requests.ConnectionError as exc:
                last_error = exc
                logger.warning(
                    f"Gemini connection error (attempt {attempt}/{retries + 1}): {exc}"
                )

            except Exception as exc:
                last_error = exc
                logger.error(
                    f"Unexpected error calling Gemini (attempt {attempt}/{retries + 1}): {exc}",
                    exc_info=True
                )
                break   # Unknown errors — stop immediately

            # Exponential backoff before next retry (1s, 2s)
            if attempt <= retries:
                backoff = 2 ** (attempt - 1)
                logger.info(f"Retrying Gemini in {backoff}s...")
                time.sleep(backoff)

        logger.warning(
            f"Gemini AI summary unavailable after {retries + 1} attempt(s) with model '{model}'. "
            f"Last error: {last_error}. Returning ai_summary=null — report saved successfully."
        )
        return None


# ── Module-level singleton (matches ocr_service / blood_parser pattern) ──
gemini_service = GeminiService()
