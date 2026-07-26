import os
import io
import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
from typing import List, Tuple
from fastapi import HTTPException, status
from app.core.logging import logger

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    easyocr = None


class OCRService:
    def __init__(self):
        self._reader = None

    def _get_reader(self):
        """Lazy load EasyOCR reader singleton to avoid slow initial imports and model reloading."""
        if not EASYOCR_AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="EasyOCR library is not installed on the server."
            )
        if self._reader is None:
            logger.info("Initializing EasyOCR reader instance (English)...")
            self._reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            logger.info("EasyOCR reader initialized.")
        return self._reader


    def convert_pdf_to_images(self, pdf_path: str) -> List[np.ndarray]:
        """Converts every page of a PDF document into OpenCV BGR images."""
        images = []
        try:
            doc = fitz.open(pdf_path)
            if doc.page_count == 0:
                raise ValueError("PDF file contains no pages.")

            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                # Render at 200 DPI for high quality OCR
                pix = page.get_pixmap(dpi=200)
                img_data = np.frombuffer(pix.samples, dtype=np.uint8)
                img_shape = (pix.height, pix.width, pix.n)
                img = img_data.reshape(img_shape)

                # Convert to BGR format for OpenCV
                if pix.n == 4:  # RGBA
                    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
                elif pix.n == 3:  # RGB
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                elif pix.n == 1:  # Grayscale
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

                images.append(img)
            doc.close()
            logger.info(f"Converted PDF ({pdf_path}) into {len(images)} page image(s).")
        except Exception as e:
            logger.error(f"Error converting PDF to images: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to process PDF document: {str(e)}"
            )

        return images

    def preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """
        Applies computer vision preprocessing:
        1. Grayscale conversion
        2. Contrast enhancement / resizing
        3. Denoising
        4. Otsu Binarization / Thresholding
        """
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()

        # Resize if image resolution is too small
        height, width = gray.shape[:2]
        if width < 1000:
            scale = 1000.0 / width
            gray = cv2.resize(gray, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        # Denoising
        denoised = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)

        # Otsu thresholding
        _, thresholded = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return thresholded

    def extract_text(self, file_path: str) -> Tuple[str, float]:
        """
        Reads PDF or image file, performs preprocessing, runs OCR,
        and returns (full_ocr_text, average_confidence).
        """
        logger.info(f"OCR process started for file: {file_path}")
        ext = os.path.splitext(file_path)[1].lower()

        raw_images: List[np.ndarray] = []

        if ext == ".pdf":
            raw_images = self.convert_pdf_to_images(file_path)
        elif ext in [".png", ".jpg", ".jpeg"]:
            img = cv2.imread(file_path)
            if img is None:
                # Try Pillow fallback
                try:
                    pil_img = Image.open(file_path).convert("RGB")
                    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                except Exception as e:
                    logger.error(f"Could not read image file {file_path}: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Corrupted or unreadable image file."
                    )
            raw_images.append(img)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format '{ext}' for OCR."
            )

        if not raw_images:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No readable images found in document."
            )

        reader = self._get_reader()
        extracted_lines: List[str] = []
        confidence_scores: List[float] = []

        for idx, img in enumerate(raw_images):
            processed_img = self.preprocess_image(img)

            # Perform EasyOCR reading on both preprocessed and original image to get optimal text recall
            results = reader.readtext(processed_img, detail=1)

            # Fallback to original image if preprocessed yields very few results
            if len(results) < 3:
                results_orig = reader.readtext(img, detail=1)
                if len(results_orig) > len(results):
                    results = results_orig

            for bbox, text, prob in results:
                cleaned_line = text.strip()
                if cleaned_line:
                    extracted_lines.append(cleaned_line)
                    confidence_scores.append(float(prob))

        full_text = "\n".join(extracted_lines)
        avg_confidence = float(np.mean(confidence_scores)) if confidence_scores else 0.0

        logger.info(f"OCR completed. Extracted {len(extracted_lines)} lines, avg confidence: {avg_confidence:.2f}")

        if not full_text.strip() or (avg_confidence < 0.15 and len(extracted_lines) < 2):
            logger.warning(f"OCR confidence too low ({avg_confidence:.2f}) or text missing for file {file_path}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unable to extract clear text from document. OCR confidence is too low or report is unreadable."
            )

        return full_text, avg_confidence


ocr_service = OCRService()
