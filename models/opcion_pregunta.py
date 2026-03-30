from __future__ import annotations

from dataclasses import dataclass

from core.validators import require_non_empty_string


@dataclass(frozen=True)
class OpcionPregunta:
    valor: str
    accion_correctiva: str = ""

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

    def to_dict(self) -> dict:
        return {
            "valor": self.valor,
            "accion_correctiva": self.accion_correctiva,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OpcionPregunta":
        return cls(
            valor=data["valor"],
            accion_correctiva=data.get("accion_correctiva", ""),
        )