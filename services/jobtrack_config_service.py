from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path


class JobtrackConfigService:
    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path or Path("config/jobtrack.ini")

    def obtener_config(self) -> dict:
        parser = ConfigParser()
        parser.read(self.config_path, encoding="utf-8")

        if "JOBTRACK" not in parser:
            raise ValueError("No existe la sección [JOBTRACK] en config/jobtrack.ini")

        seccion = parser["JOBTRACK"]

        estacion = str(seccion.get("Estacao", "")).strip()
        idioma = str(seccion.get("idioma", "")).strip()

        if not estacion:
            raise ValueError("La clave 'Estacao' es obligatoria en config/jobtrack.ini")

        return {
            "estacion": estacion,
            "idioma": idioma,
        }

    def obtener_estacion_actual(self) -> str:
        return self.obtener_config()["estacion"]