from __future__ import annotations

from config.settings import SETTINGS
from core.enums import DisparadorEstado
from models.disparador_formulario import DisparadorFormulario
from repositories.base_repository import BaseRepository


class DisparadorFormularioRepository(BaseRepository[DisparadorFormulario]):
    def __init__(self) -> None:
        super().__init__(SETTINGS.paths.disparadores_file)

    def _from_dict(self, data: dict) -> DisparadorFormulario:
        return DisparadorFormulario.from_dict(data)

    def _get_entity_id(self, entity: DisparadorFormulario) -> str:
        return entity.id_disparador

    def get_by_evento(self, id_evento: str) -> list[DisparadorFormulario]:
        normalized_id_evento = id_evento.strip()

        return [
            disparador
            for disparador in self.list_all()
            if disparador.id_evento == normalized_id_evento
        ]

    def get_by_op(self, op: str) -> list[DisparadorFormulario]:
        normalized_op = op.strip()

        return [
            disparador
            for disparador in self.list_all()
            if disparador.op == normalized_op
        ]

    def get_by_estado(
        self,
        estado_disparo: DisparadorEstado,
    ) -> list[DisparadorFormulario]:
        return [
            disparador
            for disparador in self.list_all()
            if disparador.estado_disparo == estado_disparo
        ]