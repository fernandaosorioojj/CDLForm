from __future__ import annotations

from config.settings import SETTINGS
from core.enums import EventoEstadoProcesamiento
from models.evento_op import EventoOP
from repositories.base_repository import BaseRepository


class EventoOPRepository(BaseRepository[EventoOP]):
    def __init__(self) -> None:
        super().__init__(SETTINGS.paths.eventos_op_file)

    def _from_dict(self, data: dict) -> EventoOP:
        return EventoOP.from_dict(data)

    def _get_entity_id(self, entity: EventoOP) -> str:
        return entity.id_evento

    def get_by_op(self, op: str) -> list[EventoOP]:
        normalized_op = op.strip()

        return [
            evento
            for evento in self.list_all()
            if evento.op == normalized_op
        ]

    def get_by_estado_procesamiento(
        self,
        estado_procesamiento: EventoEstadoProcesamiento,
    ) -> list[EventoOP]:
        return [
            evento
            for evento in self.list_all()
            if evento.estado_procesamiento == estado_procesamiento
        ]

    def get_by_estado_nuevo(self, estado_nuevo: str) -> list[EventoOP]:
        normalized_estado_nuevo = estado_nuevo.strip().casefold()

        return [
            evento
            for evento in self.list_all()
            if evento.estado_nuevo.casefold() == normalized_estado_nuevo
        ]

    def get_pending_events(self) -> list[EventoOP]:
        return self.get_by_estado_procesamiento(EventoEstadoProcesamiento.PENDIENTE)