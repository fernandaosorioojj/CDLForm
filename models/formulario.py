from __future__ import annotations

from dataclasses import dataclass

from core.enums import FormularioEstado, OrigenEvento
from core.validators import optional_string, require_non_empty_string


@dataclass(frozen=True)
class Formulario:
    id_formulario: str
    op: str
    area: str
    maquina: str
    fecha: str
    estado_formulario: FormularioEstado = FormularioEstado.PENDIENTE
    id_evento_origen: str | None = None
    origen_disparo: OrigenEvento | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "id_formulario", require_non_empty_string(self.id_formulario, "id_formulario"))
        object.__setattr__(self, "op", require_non_empty_string(self.op, "op"))
        object.__setattr__(self, "area", require_non_empty_string(self.area, "area"))
        object.__setattr__(self, "maquina", require_non_empty_string(self.maquina, "maquina"))
        object.__setattr__(self, "fecha", require_non_empty_string(self.fecha, "fecha"))
        object.__setattr__(
            self,
            "id_evento_origen",
            optional_string(self.id_evento_origen, "id_evento_origen"),
        )

        if not isinstance(self.estado_formulario, FormularioEstado):
            raise TypeError("estado_formulario debe ser una instancia de FormularioEstado")

        if self.origen_disparo is not None and not isinstance(self.origen_disparo, OrigenEvento):
            raise TypeError("origen_disparo debe ser una instancia de OrigenEvento o None")

    def to_dict(self) -> dict:
        return {
            "id_formulario": self.id_formulario,
            "op": self.op,
            "area": self.area,
            "maquina": self.maquina,
            "fecha": self.fecha,
            "estado_formulario": self.estado_formulario.value,
            "id_evento_origen": self.id_evento_origen,
            "origen_disparo": self.origen_disparo.value if self.origen_disparo else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Formulario":
        return cls(
            id_formulario=data["id_formulario"],
            op=data["op"],
            area=data["area"],
            maquina=data["maquina"],
            fecha=data["fecha"],
            estado_formulario=FormularioEstado(data.get("estado_formulario", FormularioEstado.PENDIENTE.value)),
            id_evento_origen=data.get("id_evento_origen"),
            origen_disparo=OrigenEvento(data["origen_disparo"]) if data.get("origen_disparo") else None,
        )