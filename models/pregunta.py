from __future__ import annotations

from dataclasses import dataclass, field

from core.enums import TipoPregunta
from core.validators import normalize_string_list, require_bool, require_non_empty_string


@dataclass(frozen=True)
class Pregunta:
    id_pregunta: str
    texto: str
    tipo: TipoPregunta
    activa: bool = True
    roles_asociados: list[str] = field(default_factory=list)
    areas_asociadas: list[str] = field(default_factory=list)
    maquinas_asociadas: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "id_pregunta",
            require_non_empty_string(self.id_pregunta, "id_pregunta"),
        )
        object.__setattr__(
            self,
            "texto",
            require_non_empty_string(self.texto, "texto"),
        )

        if not isinstance(self.tipo, TipoPregunta):
            raise TypeError("tipo debe ser una instancia de TipoPregunta")

        object.__setattr__(
            self,
            "activa",
            require_bool(self.activa, "activa"),
        )
        object.__setattr__(
            self,
            "roles_asociados",
            normalize_string_list(
                self.roles_asociados,
                "roles_asociados",
                allow_empty=False,
                unique=True,
            ),
        )
        object.__setattr__(
            self,
            "areas_asociadas",
            normalize_string_list(
                self.areas_asociadas,
                "areas_asociadas",
                allow_empty=False,
                unique=True,
            ),
        )
        object.__setattr__(
            self,
            "maquinas_asociadas",
            normalize_string_list(
                self.maquinas_asociadas,
                "maquinas_asociadas",
                allow_empty=True,
                unique=True,
            ),
        )

    def to_dict(self) -> dict:
        return {
            "id_pregunta": self.id_pregunta,
            "texto": self.texto,
            "tipo": self.tipo.value,
            "activa": self.activa,
            "roles_asociados": self.roles_asociados,
            "areas_asociadas": self.areas_asociadas,
            "maquinas_asociadas": self.maquinas_asociadas,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pregunta":
        return cls(
            id_pregunta=data["id_pregunta"],
            texto=data["texto"],
            tipo=TipoPregunta(data["tipo"]),
            activa=data.get("activa", True),
            roles_asociados=data.get("roles_asociados", []),
            areas_asociadas=data.get("areas_asociadas", []),
            maquinas_asociadas=data.get("maquinas_asociadas", []),
        )