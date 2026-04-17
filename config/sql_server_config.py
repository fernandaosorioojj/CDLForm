from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


LOCAL_CONFIG_PATH = Path(__file__).with_name("sql_server.local.json")
DEFAULT_DRIVER = "ODBC Driver 18 for SQL Server"
DEFAULT_TRUST_SERVER_CERTIFICATE = "yes"
DEFAULT_ENCRYPT = "no"


def _normalizar_texto(valor: Any) -> str:
    if valor is None:
        return ""
    return str(valor).strip()


def _leer_config_local() -> dict[str, Any]:
    if not LOCAL_CONFIG_PATH.exists():
        return {}

    data = json.loads(LOCAL_CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(
            f"El archivo {LOCAL_CONFIG_PATH} debe contener un objeto JSON."
        )

    return data


def _obtener_config(clave: str, *, default: str = "") -> str:
    valor_entorno = _normalizar_texto(os.getenv(f"CDLFORM_SQL_{clave.upper()}"))
    if valor_entorno:
        return valor_entorno

    config_local = _leer_config_local()
    valor_local = _normalizar_texto(config_local.get(clave.lower()))
    if valor_local:
        return valor_local

    return default


def _obtener_config_requerida(clave: str) -> str:
    valor = _obtener_config(clave)
    if valor:
        return valor

    variable_entorno = f"CDLFORM_SQL_{clave.upper()}"
    raise RuntimeError(
        f"No hay configuracion SQL Server para {clave}. "
        f"Defina {variable_entorno} o config/sql_server.local.json."
    )


def build_connection_string() -> str:
    db_driver = _obtener_config("driver", default=DEFAULT_DRIVER)
    db_server = _obtener_config_requerida("server")
    db_database = _obtener_config_requerida("database")
    db_username = _obtener_config_requerida("username")
    db_password = _obtener_config_requerida("password")
    db_trust_server_certificate = _obtener_config(
        "trust_server_certificate",
        default=DEFAULT_TRUST_SERVER_CERTIFICATE,
    )
    db_encrypt = _obtener_config("encrypt", default=DEFAULT_ENCRYPT)

    return (
        f"DRIVER={{{db_driver}}};"
        f"SERVER={db_server};"
        f"DATABASE={db_database};"
        f"UID={db_username};"
        f"PWD={db_password};"
        f"Encrypt={db_encrypt};"
        f"TrustServerCertificate={db_trust_server_certificate};"
    )
