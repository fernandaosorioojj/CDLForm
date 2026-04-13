from __future__ import annotations

from dataclasses import dataclass

from core.validators import require_non_empty_string


@dataclass(frozen=True)
class OpcionPregunta:
    valor: str
    accion_correctiva: str = ""
    id_opcion: str = ""
    activa: bool = True
    version: int = 1
    clave_opcion: str = ""

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
        object.__setattr__(
            self,
            "clave_opcion",
            self.clave_opcion.strip() if self.clave_opcion else self.id_opcion,
        )

        if not isinstance(self.activa, bool):
            raise TypeError("activa debe ser booleano")

        if not isinstance(self.version, int):
            raise TypeError("version debe ser un entero")
        if self.version <= 0:
            raise ValueError("version debe ser mayor que 0")

    def to_dict(self) -> dict:
        return {
            "id_opcion": self.id_opcion,
            "valor": self.valor,
            "accion_correctiva": self.accion_correctiva,
            "activa": self.activa,
            "version": self.version,
            "clave_opcion": self.clave_opcion,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OpcionPregunta":
        return cls(
            id_opcion=data.get("id_opcion", ""),
            valor=data["valor"],
            accion_correctiva=data.get("accion_correctiva", ""),
            activa=data.get("activa", True),
            version=data.get("version", 1),
            clave_opcion=data.get("clave_opcion", data.get("id_opcion", "")),
        )
