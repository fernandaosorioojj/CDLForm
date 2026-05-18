"""Punto unico para abrir conexiones SQL Server de CDLform."""

from __future__ import annotations

from typing import Any

import pyodbc

from config.sql_server_config import build_connection_string, get_sql_profile


def get_sql_connection(profile: str | None = None, **kwargs: Any) -> pyodbc.Connection:
    """Abre una conexion SQL usando el perfil configurado para el proceso actual."""
    perfil = profile or get_sql_profile()
    connection_string = build_connection_string(profile=perfil)
    return pyodbc.connect(connection_string, **kwargs)
