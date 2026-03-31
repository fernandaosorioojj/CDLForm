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

    def list_all(self) -> list[Respuesta]:
        registros = self.get_all()
        return [self._from_dict(item) for item in registros]

    def get_by_id(self, id_respuesta: str) -> Respuesta | None:
        if not id_respuesta or not str(id_respuesta).strip():
            return None

        data = self.find_by_id(str(id_respuesta).strip())
        if not data:
            return None

        return self._from_dict(data)

    def add_respuesta(self, respuesta: Respuesta) -> Respuesta:
        self.add(respuesta.to_dict())
        return respuesta

    def update(self, respuesta: Respuesta) -> Respuesta:
        self.update_by_id(respuesta.id_respuesta, respuesta.to_dict())
        return respuesta

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