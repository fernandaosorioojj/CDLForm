"""Configuracion compartida de CDLform; centraliza rutas, logging y conexion a servicios externos.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from config.settings import SETTINGS

LOCAL_CONFIG_PATH = SETTINGS.paths.sql_server_local_config_file
DEFAULT_DRIVER = "ODBC Driver 18 for SQL Server"
DEFAULT_TRUST_SERVER_CERTIFICATE = "yes"
DEFAULT_ENCRYPT = "no"
DEFAULT_PROFILE = "app"


# Bloque CDLform: funcion/metodo _normalizar_texto; encapsula una operacion del flujo del modulo.
def _normalizar_texto(valor: Any) -> str:
    if valor is None:
        return ""
    return str(valor).strip()


# Bloque CDLform: funcion/metodo _resolver_rutas_config_local; encapsula una operacion del flujo del modulo.
def _resolver_rutas_config_local() -> list[Path]:
    rutas: list[Path] = []

    override = _normalizar_texto(os.getenv("CDLFORM_SQL_CONFIG_PATH"))
    if override:
        rutas.append(Path(override).expanduser())

    rutas.append(LOCAL_CONFIG_PATH)
    rutas.append(SETTINGS.paths.bundled_config_dir / "sql_server.local.json")

    unicas: list[Path] = []
    for ruta in rutas:
        if ruta not in unicas:
            unicas.append(ruta)

    return unicas


# Bloque CDLform: funcion/metodo get_sql_server_local_config_path; encapsula una operacion del flujo del modulo.
def get_sql_server_local_config_path() -> Path:
    for ruta in _resolver_rutas_config_local():
        if ruta.exists():
            return ruta

    return _resolver_rutas_config_local()[0]


# Bloque CDLform: funcion/metodo _leer_config_local; encapsula una operacion del flujo del modulo.
def _leer_config_local() -> dict[str, Any]:
    for config_path in _resolver_rutas_config_local():
        if not config_path.exists():
            continue

        data = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(
                f"El archivo {config_path} debe contener un objeto JSON."
            )

        return data

    return {}


# Bloque CDLform: funcion/metodo _obtener_config; encapsula una operacion del flujo del modulo.
def get_sql_profile(default: str = DEFAULT_PROFILE) -> str:
    return _normalizar_texto(os.getenv("CDLFORM_SQL_PROFILE")) or default


# Bloque CDLform: funcion/metodo _obtener_config; encapsula una operacion del flujo del modulo.
def _obtener_config(clave: str, *, default: str = "", profile: str | None = None) -> str:
    perfil = _normalizar_texto(profile or get_sql_profile())
    clave_entorno = clave.upper()
    perfil_entorno = perfil.upper()

    if perfil:
        valor_entorno_perfil = _normalizar_texto(
            os.getenv(f"CDLFORM_SQL_{perfil_entorno}_{clave_entorno}")
        )
        if valor_entorno_perfil:
            return valor_entorno_perfil

    valor_entorno = _normalizar_texto(os.getenv(f"CDLFORM_SQL_{clave_entorno}"))
    if valor_entorno:
        return valor_entorno

    config_local = _leer_config_local()
    profiles = config_local.get("profiles")
    if isinstance(profiles, dict) and perfil:
        profile_config = profiles.get(perfil)
        if isinstance(profile_config, dict):
            valor_perfil = _normalizar_texto(profile_config.get(clave.lower()))
            if valor_perfil:
                return valor_perfil

    valor_local = _normalizar_texto(config_local.get(clave.lower()))
    if valor_local:
        return valor_local

    return default


# Bloque CDLform: funcion/metodo _obtener_config_requerida; encapsula una operacion del flujo del modulo.
def _obtener_config_requerida(clave: str, *, profile: str | None = None) -> str:
    valor = _obtener_config(clave, profile=profile)
    if valor:
        return valor

    perfil = _normalizar_texto(profile or get_sql_profile())
    variable_entorno = f"CDLFORM_SQL_{clave.upper()}"
    variable_entorno_perfil = (
        f" o CDLFORM_SQL_{perfil.upper()}_{clave.upper()}" if perfil else ""
    )
    ruta_config = get_sql_server_local_config_path()
    raise RuntimeError(
        f"No hay configuracion SQL Server para {clave}. "
        f"Defina {variable_entorno}{variable_entorno_perfil} o {ruta_config}."
    )


# Bloque CDLform: funcion/metodo build_connection_string; encapsula una operacion del flujo del modulo.
def build_connection_string(profile: str | None = None) -> str:
    db_driver = _obtener_config("driver", default=DEFAULT_DRIVER, profile=profile)
    db_server = _obtener_config_requerida("server", profile=profile)
    db_database = _obtener_config_requerida("database", profile=profile)
    db_username = _obtener_config_requerida("username", profile=profile)
    db_password = _obtener_config_requerida("password", profile=profile)
    db_trust_server_certificate = _obtener_config(
        "trust_server_certificate",
        default=DEFAULT_TRUST_SERVER_CERTIFICATE,
        profile=profile,
    )
    db_encrypt = _obtener_config("encrypt", default=DEFAULT_ENCRYPT, profile=profile)
    db_app_name = _obtener_config("app_name", default="CDLform", profile=profile)

    return (
        f"DRIVER={{{db_driver}}};"
        f"SERVER={db_server};"
        f"DATABASE={db_database};"
        f"UID={db_username};"
        f"PWD={db_password};"
        f"Encrypt={db_encrypt};"
        f"TrustServerCertificate={db_trust_server_certificate};"
        f"APP={db_app_name};"
    )
