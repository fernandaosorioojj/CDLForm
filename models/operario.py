from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Operario:
    id_operario: str
    nombre: str
    area: str
    maquina: str
    activo: bool = True

    def __post_init__(self) -> None:
        self.id_operario = str(self.id_operario).strip()
        self.nombre = str(self.nombre).strip()
        self.area = str(self.area).strip()
        self.maquina = str(self.maquina).strip()

        if not self.id_operario:
            raise ValueError("id_operario es obligatorio.")

        if not self.nombre:
            raise ValueError("nombre es obligatorio.")

        if not self.area:
            raise ValueError("area es obligatoria.")

        if not self.maquina:
            raise ValueError("maquina es obligatoria.")

        self.activo = bool(self.activo)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_operario": self.id_operario,
            "nombre": self.nombre,
            "area": self.area,
            "maquina": self.maquina,
            "activo": self.activo,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Operario":
        if not isinstance(data, dict):
            raise ValueError("Los datos del operario deben venir en formato dict.")

        return cls(
            id_operario=data.get("id_operario", ""),
            nombre=data.get("nombre", ""),
            area=data.get("area", ""),
            maquina=data.get("maquina", ""),
            activo=data.get("activo", True),
        )