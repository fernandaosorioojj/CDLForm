from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Formulario:
    id_formulario: str
    identificador: str
    operario: str
    id_operario: str = ""
    cod_setor: str = ""
    cod_recurso: str = ""
    cod_ativ: str = ""
    turno: str = ""
    tipo_trabajo: str = ""
    evento_origen: Optional[str] = None
    estado: str = "pendiente"

    def __post_init__(self) -> None:
        self.id_formulario = str(self.id_formulario).strip()
        self.identificador = str(self.identificador).strip()
        self.operario = str(self.operario).strip()
        self.id_operario = str(self.id_operario).strip()
        self.cod_setor = str(self.cod_setor).strip()
        self.cod_recurso = str(self.cod_recurso).strip()
        self.cod_ativ = str(self.cod_ativ).strip()
        self.turno = str(self.turno).strip()
        self.tipo_trabajo = str(self.tipo_trabajo).strip()
        self.estado = str(self.estado).strip()

        if self.evento_origen is not None:
            self.evento_origen = str(self.evento_origen).strip()
            if not self.evento_origen:
                self.evento_origen = None

        if not self.id_formulario:
            raise ValueError("id_formulario es obligatorio.")

        if not self.identificador:
            raise ValueError("identificador es obligatorio.")

        if not self.operario:
            raise ValueError("operario es obligatorio.")

        if not self.estado:
            raise ValueError("estado es obligatorio.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_formulario": self.id_formulario,
            "identificador": self.identificador,
            "operario": self.operario,
            "id_operario": self.id_operario,
            "cod_setor": self.cod_setor,
            "cod_recurso": self.cod_recurso,
            "cod_ativ": self.cod_ativ,
            "turno": self.turno,
            "tipo_trabajo": self.tipo_trabajo,
            "evento_origen": self.evento_origen,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Formulario":
        if not isinstance(data, dict):
            raise ValueError("Los datos del formulario deben venir en formato dict.")

        return cls(
            id_formulario=data.get("id_formulario", ""),
            identificador=data.get("identificador", ""),
            operario=data.get("operario", ""),
            id_operario=data.get("id_operario", ""),
            cod_setor=data.get("cod_setor", ""),
            cod_recurso=data.get("cod_recurso", ""),
            cod_ativ=data.get("cod_ativ", ""),
            turno=data.get("turno", ""),
            tipo_trabajo=data.get("tipo_trabajo", ""),
            evento_origen=data.get("evento_origen"),
            estado=data.get("estado", "pendiente"),
        )