"""Configuracion compartida de CDLform; centraliza rutas, logging y conexion a servicios externos.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path


# Bloque CDLform: clase AppPaths; agrupa estado y comportamiento de esta parte del flujo.
@dataclass(frozen=True)
class AppPaths:
    package_dir: Path
    bundled_config_dir: Path
    assets_dir: Path
    styles_dir: Path
    data_dir: Path
    logs_dir: Path
    jobtrack_config_file: Path
    sql_server_local_config_file: Path
    gestion_login_file: Path
    admin_login_file: Path
    app_log_file: Path


# Bloque CDLform: clase AppSettings; agrupa estado y comportamiento de esta parte del flujo.
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


# Bloque CDLform: funcion/metodo _resolve_package_dir; encapsula una operacion del flujo del modulo.
def _resolve_package_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent.parent


# Bloque CDLform: funcion/metodo _resolve_data_dir; encapsula una operacion del flujo del modulo.
def _resolve_data_dir(app_name: str) -> Path:
    override = os.getenv("CDLFORM_DATA_DIR", "").strip()
    if override:
        return Path(override).expanduser().resolve()

    appdata = os.getenv("APPDATA", "").strip()
    if appdata:
        return Path(appdata).expanduser().resolve() / app_name

    return (_resolve_package_dir() / ".local").resolve()


# Bloque CDLform: funcion/metodo _build_paths; encapsula una operacion del flujo del modulo.
def _build_paths() -> AppPaths:
    app_name = "CDLform"
    package_dir = _resolve_package_dir()
    bundled_config_dir = package_dir / "config"
    data_dir = _resolve_data_dir(app_name)
    logs_dir = data_dir / "logs"

    return AppPaths(
        package_dir=package_dir,
        bundled_config_dir=bundled_config_dir,
        assets_dir=package_dir / "assets",
        styles_dir=package_dir / "styles",
        data_dir=data_dir,
        logs_dir=logs_dir,
        jobtrack_config_file=data_dir / "jobtrack.ini",
        sql_server_local_config_file=data_dir / "sql_server.local.json",
        gestion_login_file=data_dir / "gestion_login.json",
        admin_login_file=data_dir / "admin_login.json",
        app_log_file=logs_dir / "cdlform.log",
    )


# Bloque CDLform: funcion/metodo _build_settings; encapsula una operacion del flujo del modulo.
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
