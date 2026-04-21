from __future__ import annotations

import os
from configparser import ConfigParser
from pathlib import Path

from config.settings import SETTINGS


class JobtrackConfigService:
    def __init__(self, ini_path: str | Path | None = None) -> None:
        if ini_path is not None:
            self.ini_path = Path(ini_path)
            return

        override = self._normalizar_texto(os.getenv("CDLFORM_JOBTRACK_INI"))
        if override:
            self.ini_path = Path(override).expanduser()
            return

        ruta_local = SETTINGS.paths.jobtrack_config_file
        if ruta_local.exists():
            self.ini_path = ruta_local
            return

        self.ini_path = SETTINGS.paths.bundled_config_dir / "jobtrack.ini"

    @staticmethod
    def _normalizar_texto(valor: object) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

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
