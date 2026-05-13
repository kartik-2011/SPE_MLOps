"""Logging configuration for the application."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Minimal JSON log formatter for ELK-friendly output."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "event"):
            payload["event"] = record.event
        if hasattr(record, "model_version"):
            payload["model_version"] = record.model_version
        return json.dumps(payload)


def configure_logging() -> None:
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(console_handler)

    log_file_path = os.getenv("APP_LOG_FILE")
    if log_file_path:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(JsonFormatter())
        root_logger.addHandler(file_handler)
