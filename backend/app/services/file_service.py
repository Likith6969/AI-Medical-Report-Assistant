import os
import uuid
from typing import Tuple, List, Optional
from fastapi import UploadFile, HTTPException, status
from app.core.logging import logger

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/pjpeg"
}
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB


class FileService:
    def __init__(self, base_upload_dir: str = "uploads"):
        self.base_upload_dir = base_upload_dir
        self.categories = ["blood_reports", "mri", "xray", "profile", "temp"]
        self._init_directories()

    def _init_directories(self):
        """Ensures that all upload subdirectories exist."""
        for category in self.categories:
            dir_path = os.path.join(self.base_upload_dir, category)
            os.makedirs(dir_path, exist_ok=True)

    def validate_file(
        self,
        file: UploadFile,
        allowed_extensions: Optional[set] = None,
        max_size_bytes: int = MAX_FILE_SIZE_BYTES
    ) -> None:
        """Validates file extension, MIME type, emptiness, and file size."""
        if allowed_extensions is None:
            allowed_extensions = ALLOWED_EXTENSIONS

        filename = file.filename or ""
        ext = os.path.splitext(filename)[1].lower()

        if not ext or ext not in allowed_extensions:
            logger.warning(f"File upload rejected: unsupported extension '{ext}' for file '{filename}'")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(sorted(allowed_extensions))}"
            )

        if file.content_type and file.content_type.lower() not in ALLOWED_MIME_TYPES and ext != ".pdf":
            logger.warning(f"File upload rejected: unsupported content-type '{file.content_type}'")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file content-type '{file.content_type}'."
            )

        # Read contents to check size & empty status
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size == 0:
            logger.warning(f"File upload rejected: empty file '{filename}'")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )

        if file_size > max_size_bytes:
            max_mb = max_size_bytes / (1024 * 1024)
            logger.warning(f"File upload rejected: file size {file_size} exceeds {max_mb} MB")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum limit of {max_mb:.1f} MB."
            )

    def save_file(
        self,
        file: UploadFile,
        category: str = "blood_reports"
    ) -> Tuple[str, str, str]:
        """
        Validates and stores the uploaded file into the category directory.
        Returns (stored_relative_path, unique_filename, original_filename).
        """
        if category not in self.categories:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Invalid upload category '{category}'"
            )

        self.validate_file(file)

        original_filename = file.filename or "unknown"
        ext = os.path.splitext(original_filename)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}{ext}"

        category_dir = os.path.join(self.base_upload_dir, category)
        file_path = os.path.join(category_dir, unique_filename)

        # Standardize path separators for consistency
        relative_path = os.path.normpath(file_path).replace("\\", "/")

        try:
            file.file.seek(0)
            with open(file_path, "wb") as buffer:
                while chunk := file.file.read(8192):
                    buffer.write(chunk)
            logger.info(f"File saved successfully at {relative_path}")
        except Exception as e:
            logger.error(f"Failed to write uploaded file to disk: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save uploaded file to storage."
            )

        return relative_path, unique_filename, original_filename


file_service = FileService()
