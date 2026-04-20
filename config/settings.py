from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppPaths:
    base_dir: Path
    config_dir: Path
    logs_dir: Path

    app_log_file: Path


@dataclass(frozen=True)
class AppSettings:
    app_name: str
    app_version: str
    environment: str
    timezone_name: str
    default_encoding: str
    log_level: str
    trigger_status_values: tuple[str, ...]
    paths: AppPaths


def _build_paths() -> AppPaths:
    base_dir = Path(__file__).resolve().parent.parent
    config_dir = base_dir / "config"
    logs_dir = base_dir / "logs"

    return AppPaths(
        base_dir=base_dir,
        config_dir=config_dir,
        logs_dir=logs_dir,
        app_log_file=logs_dir / "cdlform.log",
    )


def _build_settings() -> AppSettings:
    environment = os.getenv("CDLFORM_ENV", "development").strip().lower() or "development"
    log_level = os.getenv("CDLFORM_LOG_LEVEL", "INFO").strip().upper() or "INFO"

    return AppSettings(
        app_name="CDLform",
        app_version="1.0.0",
        environment=environment,
        timezone_name="America/Santiago",
        default_encoding="utf-8",
        log_level=log_level,
        trigger_status_values=("terminada", "finalizada", "cerrada", "completada"),
        paths=_build_paths(),
    )


SETTINGS = _build_settings()
