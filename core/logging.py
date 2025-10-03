"""Logging helpers for the CLI tool."""
import logging
from typing import Optional


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s %(name)s - %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name if name else __name__)

