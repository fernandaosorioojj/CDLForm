from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Formulario:
    id_formulario: str
    op: str
    area: str
    maquina: str
    operario: Optional[str] = None
    evento_origen: Optional[str] = None
    estado: str = "pendiente"

    def __post_init__(self) -> None:
        self.id_formulario = str(self.id_formulario).strip()
        self.op = str(self.op).strip()
        self.area = str(self.area).strip()
        self.maquina = str(self.maquina).strip()
        self.estado = str(self.estado).strip()

        if self.operario is not None:
            self.operario = str(self.operario).strip()

        if self.evento_origen is not None:
            self.evento_origen = str(self.evento_origen).strip()

        if not self.id_formulario:
            raise ValueError("id_formulario es obligatorio.")

        if not self.op:
            raise ValueError("op es obligatoria.")

        if not self.area:
            raise ValueError("area es obligatoria.")

        if not self.maquina:
            raise ValueError("maquina es obligatoria.")

        if not self.estado:
            raise ValueError("estado es obligatorio.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_formulario": self.id_formulario,
            "op": self.op,
            "area": self.area,
            "maquina": self.maquina,
            "operario": self.operario,
            "evento_origen": self.evento_origen,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Formulario":
        if not isinstance(data, dict):
            raise ValueError("Los datos del formulario deben venir en formato dict.")

        return cls(
            id_formulario=data.get("id_formulario", ""),
            op=data.get("op", ""),
            area=data.get("area", ""),
            maquina=data.get("maquina", ""),
            operario=data.get("operario"),
            evento_origen=data.get("evento_origen"),
            estado=data.get("estado", "pendiente"),
        )