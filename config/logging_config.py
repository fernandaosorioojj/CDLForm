from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import SETTINGS


def configure_logging() -> None:
    logs_dir: Path = SETTINGS.paths.logs_dir
    logs_dir.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    root_logger.setLevel(getattr(logging, SETTINGS.log_level, logging.INFO))

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename=SETTINGS.paths.app_log_file,
        maxBytes=2 * 1024 * 1024,
        backupCount=5,
        encoding=SETTINGS.default_encoding,
    )
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)