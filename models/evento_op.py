from __future__ import annotations

from dataclasses import dataclass

from core.enums import EventoEstadoProcesamiento, OrigenEvento
from core.validators import require_non_empty_string


@dataclass(frozen=True)
class EventoOP:
    id_evento: str
    op: str
    estado_anterior: str
    estado_nuevo: str
    area: str
    maquina: str
    fecha_evento: str
    origen: OrigenEvento = OrigenEvento.JOBTRACK
    estado_procesamiento: EventoEstadoProcesamiento = EventoEstadoProcesamiento.PENDIENTE

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "id_evento",
            require_non_empty_string(self.id_evento, "id_evento"),
        )
        object.__setattr__(
            self,
            "op",
            require_non_empty_string(self.op, "op"),
        )
        object.__setattr__(
            self,
            "estado_anterior",
            require_non_empty_string(self.estado_anterior, "estado_anterior"),
        )
        object.__setattr__(
            self,
            "estado_nuevo",
            require_non_empty_string(self.estado_nuevo, "estado_nuevo"),
        )
        object.__setattr__(
            self,
            "area",
            require_non_empty_string(self.area, "area"),
        )
        object.__setattr__(
            self,
            "maquina",
            require_non_empty_string(self.maquina, "maquina"),
        )
        object.__setattr__(
            self,
            "fecha_evento",
            require_non_empty_string(self.fecha_evento, "fecha_evento"),
        )

        if not isinstance(self.origen, OrigenEvento):
            raise TypeError("origen debe ser una instancia de OrigenEvento")

        if not isinstance(self.estado_procesamiento, EventoEstadoProcesamiento):
            raise TypeError(
                "estado_procesamiento debe ser una instancia de EventoEstadoProcesamiento"
            )

    def to_dict(self) -> dict:
        return {
            "id_evento": self.id_evento,
            "op": self.op,
            "estado_anterior": self.estado_anterior,
            "estado_nuevo": self.estado_nuevo,
            "area": self.area,
            "maquina": self.maquina,
            "fecha_evento": self.fecha_evento,
            "origen": self.origen.value,
            "estado_procesamiento": self.estado_procesamiento.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EventoOP":
        return cls(
            id_evento=data["id_evento"],
            op=data["op"],
            estado_anterior=data["estado_anterior"],
            estado_nuevo=data["estado_nuevo"],
            area=data["area"],
            maquina=data["maquina"],
            fecha_evento=data["fecha_evento"],
            origen=OrigenEvento(data.get("origen", OrigenEvento.JOBTRACK.value)),
            estado_procesamiento=EventoEstadoProcesamiento(
                data.get(
                    "estado_procesamiento",
                    EventoEstadoProcesamiento.PENDIENTE.value,
                )
            ),
        )