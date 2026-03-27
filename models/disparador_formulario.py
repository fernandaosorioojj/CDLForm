from __future__ import annotations

from dataclasses import dataclass

from core.enums import DisparadorEstado
from core.validators import optional_string, require_non_empty_string


@dataclass(frozen=True)
class DisparadorFormulario:
    id_disparador: str
    id_evento: str
    op: str
    fecha_disparo: str
    estado_disparo: DisparadorEstado
    mensaje: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "id_disparador",
            require_non_empty_string(self.id_disparador, "id_disparador"),
        )
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
            "fecha_disparo",
            require_non_empty_string(self.fecha_disparo, "fecha_disparo"),
        )
        object.__setattr__(
            self,
            "mensaje",
            optional_string(self.mensaje, "mensaje"),
        )

        if not isinstance(self.estado_disparo, DisparadorEstado):
            raise TypeError("estado_disparo debe ser una instancia de DisparadorEstado")

    def to_dict(self) -> dict:
        return {
            "id_disparador": self.id_disparador,
            "id_evento": self.id_evento,
            "op": self.op,
            "fecha_disparo": self.fecha_disparo,
            "estado_disparo": self.estado_disparo.value,
            "mensaje": self.mensaje,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DisparadorFormulario":
        return cls(
            id_disparador=data["id_disparador"],
            id_evento=data["id_evento"],
            op=data["op"],
            fecha_disparo=data["fecha_disparo"],
            estado_disparo=DisparadorEstado(data["estado_disparo"]),
            mensaje=data.get("mensaje"),
        )