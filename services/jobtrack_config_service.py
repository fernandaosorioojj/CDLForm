from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path


class JobtrackConfigService:
    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path or Path(r"C:\JOBTRACK\jobtrack.ini")

    def obtener_config(self) -> dict:
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo de configuración: {self.config_path}"
            )

        parser = ConfigParser()
        parser.read(self.config_path, encoding="utf-8")

        if "JOBTRACK" not in parser:
            raise ValueError(
                f"No existe la sección [JOBTRACK] en {self.config_path}"
            )

        seccion = parser["JOBTRACK"]

        estacion = str(seccion.get("Estacao", "")).strip()
        idioma = str(seccion.get("idioma", "")).strip()

        if not estacion:
            raise ValueError(
                f"La clave 'Estacao' es obligatoria en {self.config_path}"
            )

        return {
            "estacion": estacion,
            "idioma": idioma,
        }

    def obtener_estacion_actual(self) -> str:
        return self.obtener_config()["estacion"]