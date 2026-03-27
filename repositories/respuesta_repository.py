from __future__ import annotations

from config.settings import SETTINGS
from models.respuesta import Respuesta
from repositories.base_repository import BaseRepository


class RespuestaRepository(BaseRepository[Respuesta]):
    def __init__(self) -> None:
        super().__init__(SETTINGS.paths.respuestas_file)

    def _from_dict(self, data: dict) -> Respuesta:
        return Respuesta.from_dict(data)

    def _get_entity_id(self, entity: Respuesta) -> str:
        return entity.id_respuesta

    def get_by_formulario(self, id_formulario: str) -> list[Respuesta]:
        normalized_id_formulario = id_formulario.strip()

        return [
            respuesta
            for respuesta in self.list_all()
            if respuesta.id_formulario == normalized_id_formulario
        ]

    def get_by_pregunta(self, id_pregunta: str) -> list[Respuesta]:
        normalized_id_pregunta = id_pregunta.strip()

        return [
            respuesta
            for respuesta in self.list_all()
            if respuesta.id_pregunta == normalized_id_pregunta
        ]