from __future__ import annotations

from pathlib import Path

from models.respuesta import Respuesta
from repositories.base_repository import BaseRepository


class RespuestaRepository(BaseRepository):
    def __init__(self, file_path: Path | None = None) -> None:
        super().__init__(file_path or Path("storage/respuestas.json"))

    def _from_dict(self, data: dict) -> Respuesta:
        return Respuesta.from_dict(data)

    def _get_entity_id(self, entity: Respuesta) -> str:
        return entity.id_respuesta

    def get_respuestas_por_formulario(self, id_formulario: str) -> list[Respuesta]:
        id_formulario = id_formulario.strip()

        return [
            respuesta
            for respuesta in self.list_all()
            if respuesta.id_formulario == id_formulario
        ]

    def get_respuestas_por_pregunta(self, id_pregunta: str) -> list[Respuesta]:
        id_pregunta = id_pregunta.strip()

        return [
            respuesta
            for respuesta in self.list_all()
            if respuesta.id_pregunta == id_pregunta
        ]