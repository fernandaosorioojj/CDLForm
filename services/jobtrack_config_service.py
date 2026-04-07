from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path


class JobtrackConfigService:
    def __init__(self, ini_path: str | Path = "config/jobtrack.ini") -> None:
        self.ini_path = Path(ini_path)

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

    def obtener_estacion_local(self) -> str:
        parser = self._load_parser()
        estacion = parser.get("JOBTRACK", "Estacao", fallback="").strip()

        if not estacion:
            raise ValueError(
                f"La clave 'Estacao' no está configurada en {self.ini_path}."
            )

        return estacion

    def obtener_idioma(self) -> str:
        parser = self._load_parser()
        return parser.get("JOBTRACK", "idioma", fallback="").strip()