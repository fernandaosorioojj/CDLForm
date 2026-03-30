from __future__ import annotations

from pathlib import Path
from typing import Optional

from repositories.base_repository import BaseRepository


class PreguntaRepository(BaseRepository):
    def __init__(self, file_path: Path | None = None) -> None:
        super().__init__(file_path or Path("storage/preguntas.json"))

    def obtener_todas(self) -> list[dict]:
        return self.get_all()

    def obtener_por_id(self, id_pregunta: str) -> Optional[dict]:
        return self.find_by_id(id_pregunta)

    def crear(self, pregunta: dict) -> dict:
        self.add(pregunta)
        return pregunta

    def actualizar(self, id_pregunta: str, data: dict) -> Optional[dict]:
        actualizado = self.update_by_id(id_pregunta, data)
        if not actualizado:
            return None
        return self.find_by_id(id_pregunta)

    def eliminar(self, id_pregunta: str) -> bool:
        return self.delete_by_id(id_pregunta)