"""Servicios para leer configuracion JobTrack, homologar estaciones y consultar SQL productivo.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import os
from configparser import ConfigParser
from pathlib import Path

from config.settings import SETTINGS

JOBTRACK_INI_OFICIAL = Path(r"C:\JOBTRACK\jobtrack.ini")


# Bloque CDLform: clase JobtrackConfigService; agrupa estado y comportamiento de esta parte del flujo.
class JobtrackConfigService:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self, ini_path: str | Path | None = None) -> None:
        if ini_path is not None:
            self.ini_path = Path(ini_path)
            return

        override = self._normalizar_texto(os.getenv("CDLFORM_JOBTRACK_INI"))
        if override:
            self.ini_path = Path(override).expanduser()
            return

        self.ini_path = self._resolver_ini_path()

    # Bloque CDLform: funcion/metodo _normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_texto(valor: object) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo _resolver_ini_path; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _resolver_ini_path() -> Path:
        return JOBTRACK_INI_OFICIAL

    # Bloque CDLform: funcion/metodo _load_parser; encapsula una operacion del flujo del modulo.
    def _load_parser(self) -> ConfigParser:
        if not self.ini_path.exists():
            raise FileNotFoundError(
                f"No existe el archivo de configuración JobTrack: {self.ini_path}"
            )

        parser = ConfigParser()
        parser.read(str(self.ini_path), encoding="utf-8")

        if "JOBTRACK" not in parser:
            raise ValueError(
                f"El archivo {self.ini_path} no contiene la sección [JOBTRACK]."
            )

        return parser

    # Bloque CDLform: funcion/metodo obtener_estacion_local; encapsula una operacion del flujo del modulo.
    def obtener_estacion_local(self) -> str:
        parser = self._load_parser()
        estacion = parser.get("JOBTRACK", "Estacao", fallback="").strip()

        if not estacion:
            raise ValueError(
                f"La clave 'Estacao' no está configurada en {self.ini_path}."
            )

        return estacion

    # Bloque CDLform: funcion/metodo obtener_idioma; encapsula una operacion del flujo del modulo.
    def obtener_idioma(self) -> str:
        parser = self._load_parser()
        return parser.get("JOBTRACK", "idioma", fallback="").strip()
