from __future__ import annotations

from config.settings import SETTINGS
from models.formulario import Formulario
from repositories.base_repository import BaseRepository


class FormularioRepository(BaseRepository[Formulario]):
    def __init__(self) -> None:
        super().__init__(SETTINGS.paths.formularios_file)

    def _from_dict(self, data: dict) -> Formulario:
        return Formulario.from_dict(data)

    def _get_entity_id(self, entity: Formulario) -> str:
        return entity.id_formulario

    def get_by_op(self, op: str) -> list[Formulario]:
        normalized_op = op.strip()

        return [
            formulario
            for formulario in self.list_all()
            if formulario.op == normalized_op
        ]

    def get_by_evento_origen(self, id_evento_origen: str) -> list[Formulario]:
        normalized_id_evento = id_evento_origen.strip()

        return [
            formulario
            for formulario in self.list_all()
            if formulario.id_evento_origen == normalized_id_evento
        ]