from __future__ import annotations

from dataclasses import dataclass

from core.validators import require_non_empty_string


@dataclass(frozen=True)
class OpcionPregunta:
    valor: str
    accion_correctiva: str = ""
    id_opcion: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "valor",
            require_non_empty_string(self.valor, "valor"),
        )
        object.__setattr__(
            self,
            "accion_correctiva",
            self.accion_correctiva.strip() if self.accion_correctiva else "",
        )
        object.__setattr__(
            self,
            "id_opcion",
            self.id_opcion.strip() if self.id_opcion else "",
        )

    def to_dict(self) -> dict:
        return {
            "id_opcion": self.id_opcion,
            "valor": self.valor,
            "accion_correctiva": self.accion_correctiva,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OpcionPregunta":
        return cls(
            id_opcion=data.get("id_opcion", ""),
            valor=data["valor"],
            accion_correctiva=data.get("accion_correctiva", ""),
        )