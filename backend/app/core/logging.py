import logging
import sys


def setup_logging() -> logging.Logger:
    """Configures structured application logging for FastAPI backend."""
    logger = logging.getLogger("medical_assistant")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if already initialized
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = setup_logging()
