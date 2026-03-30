from __future__ import annotations

from core.enums import OrigenEvento
from core.exceptions import ValidationError
from core.validators import require_non_empty_string
from models.evento_op import EventoOP
from services.evento_op_service import EventoOPService


class JobTrackListener:
    def __init__(self) -> None:
        self.evento_service = EventoOPService()

    def validate_payload(self, payload: dict) -> dict:
        if not isinstance(payload, dict):
            raise ValidationError("el payload del evento debe ser un diccionario")

        return {
            "op": require_non_empty_string(payload.get("op"), "op"),
            "estado_anterior": require_non_empty_string(
                payload.get("estado_anterior"),
                "estado_anterior",
            ),
            "estado_nuevo": require_non_empty_string(
                payload.get("estado_nuevo"),
                "estado_nuevo",
            ),
            "area": require_non_empty_string(payload.get("area"), "area"),
            "maquina": require_non_empty_string(payload.get("maquina"), "maquina"),
            "fecha_evento": require_non_empty_string(
                payload.get("fecha_evento"),
                "fecha_evento",
            ),
        }

    def receive_event(self, payload: dict) -> EventoOP:
        data = self.validate_payload(payload)

        return self.evento_service.create(
            op=data["op"],
            estado_anterior=data["estado_anterior"],
            estado_nuevo=data["estado_nuevo"],
            area=data["area"],
            maquina=data["maquina"],
            fecha_evento=data["fecha_evento"],
            origen=OrigenEvento.JOBTRACK,
        )

    def receive_trigger_event(self, payload: dict) -> EventoOP:
        data = self.validate_payload(payload)

        return self.evento_service.create_if_trigger_status(
            op=data["op"],
            estado_anterior=data["estado_anterior"],
            estado_nuevo=data["estado_nuevo"],
            area=data["area"],
            maquina=data["maquina"],
            fecha_evento=data["fecha_evento"],
            origen=OrigenEvento.JOBTRACK,
        )