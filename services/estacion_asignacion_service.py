from __future__ import annotations

import json
from pathlib import Path


class EstacionAsignacionService:
    def __init__(self, file_path: Path | None = None) -> None:
        self.file_path = file_path or Path("config/estaciones_recursos.json")

    def _read_all(self) -> dict[str, list[str]]:
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo de asignación de estaciones: {self.file_path}"
            )

        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def obtener_recursos_por_estacion(self, estacion: str) -> list[str]:
        estacion_normalizada = str(estacion).strip().upper()
        data = self._read_all()

        recursos = data.get(estacion_normalizada, [])
        return [
            str(recurso).strip()
            for recurso in recursos
            if str(recurso).strip()
        ]