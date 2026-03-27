from __future__ import annotations

from config.settings import SETTINGS
from core.enums import EventoEstadoProcesamiento, OrigenEvento
from core.exceptions import BusinessRuleError, NotFoundError
from models.evento_op import EventoOP
from repositories.evento_op_repository import EventoOPRepository
from utils.datetime_utils import DateTimeUtils
from utils.id_generator import IdGenerator


class EventoOPService:
    def __init__(self) -> None:
        self.repository = EventoOPRepository()

    def list_all(self) -> list[EventoOP]:
        return self.repository.list_all()

    def get_by_id(self, id_evento: str) -> EventoOP:
        return self.repository.get_by_id(id_evento)

    def get_by_op(self, op: str) -> list[EventoOP]:
        return self.repository.get_by_op(op)

    def get_pending_events(self) -> list[EventoOP]:
        return self.repository.get_pending_events()

    def is_trigger_status(self, estado_nuevo: str) -> bool:
        normalized_status = estado_nuevo.strip().casefold()
        allowed_statuses = {
            status.strip().casefold()
            for status in SETTINGS.trigger_status_values
        }
        return normalized_status in allowed_statuses

    def create(
        self,
        op: str,
        estado_anterior: str,
        estado_nuevo: str,
        area: str,
        maquina: str,
        fecha_evento: str,
        origen: OrigenEvento = OrigenEvento.JOBTRACK,
    ) -> EventoOP:
        eventos_existentes = self.repository.list_all()
        next_number = len(eventos_existentes) + 1
        id_evento = IdGenerator.generate("EVT", next_number)

        fecha_normalizada = DateTimeUtils.normalize_datetime_string(
            fecha_evento,
            "fecha_evento",
        )

        evento = EventoOP(
            id_evento=id_evento,
            op=op,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            area=area,
            maquina=maquina,
            fecha_evento=fecha_normalizada,
            origen=origen,
            estado_procesamiento=EventoEstadoProcesamiento.PENDIENTE,
        )

        self.repository.add(evento)
        return evento

    def create_if_trigger_status(
        self,
        op: str,
        estado_anterior: str,
        estado_nuevo: str,
        area: str,
        maquina: str,
        fecha_evento: str,
        origen: OrigenEvento = OrigenEvento.JOBTRACK,
    ) -> EventoOP:
        if not self.is_trigger_status(estado_nuevo):
            raise BusinessRuleError(
                f"el estado '{estado_nuevo}' no corresponde a un estado disparador configurado"
            )

        return self.create(
            op=op,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            area=area,
            maquina=maquina,
            fecha_evento=fecha_evento,
            origen=origen,
        )

    def mark_as_processed(self, id_evento: str) -> EventoOP:
        evento_actual = self.repository.get_by_id(id_evento)

        evento_actualizado = EventoOP(
            id_evento=evento_actual.id_evento,
            op=evento_actual.op,
            estado_anterior=evento_actual.estado_anterior,
            estado_nuevo=evento_actual.estado_nuevo,
            area=evento_actual.area,
            maquina=evento_actual.maquina,
            fecha_evento=evento_actual.fecha_evento,
            origen=evento_actual.origen,
            estado_procesamiento=EventoEstadoProcesamiento.PROCESADO,
        )

        self.repository.update(evento_actualizado)
        return evento_actualizado

    def delete(self, id_evento: str) -> None:
        self.repository.delete(id_evento)

    def ensure_exists(self, id_evento: str) -> None:
        try:
            self.repository.get_by_id(id_evento)
        except NotFoundError as exc:
            raise NotFoundError(
                f"no existe un evento con id '{id_evento}'"
            ) from exc