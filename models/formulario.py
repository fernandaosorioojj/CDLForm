from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ESTADO_EN_APERTURA = "en_apertura"
ESTADO_PENDIENTE_OPERARIO = "pendiente_operario"
ESTADO_COMPLETADO = "completado"
ESTADO_CANCELADO = "cancelado"

MAPA_ESTADOS_LEGACY = {
    "en_progreso": ESTADO_PENDIENTE_OPERARIO,
    "enviado": ESTADO_COMPLETADO,
}


def _normalizar_texto(valor: Any) -> str:
    if valor is None:
        return ""
    return str(valor).strip()


def _serializar_valor(valor: Any) -> Any:
    if valor is None:
        return None

    if hasattr(valor, "isoformat"):
        try:
            return valor.isoformat()
        except TypeError:
            pass

    return valor


def _normalizar_estado(valor: Any) -> str:
    estado = _normalizar_texto(valor)
    if not estado:
        return ESTADO_EN_APERTURA
    return MAPA_ESTADOS_LEGACY.get(estado, estado)


@dataclass
class Formulario:
    id_formulario: str
    identificador: str
    id_apontamento: str
    fecha_formulario: str
    area: str = ""
    maquina: str = ""
    cod_recurso: str = ""
    cod_setor: str = ""
    turno: Any = None
    hora_fim: Any = None
    operario: str = ""
    estacion: str = ""
    evento_origen: str = ""
    estado: str = ESTADO_EN_APERTURA
    descripcion_op: str = ""
    descripcion_proceso: str = ""
    observacion_general: str = ""
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""
    id_plantilla_preguntas: str = ""
    version_plantilla_preguntas: int = 0

    def __post_init__(self) -> None:
        self.id_formulario = _normalizar_texto(self.id_formulario)
        self.identificador = _normalizar_texto(self.identificador)
        self.id_apontamento = _normalizar_texto(self.id_apontamento)
        self.fecha_formulario = _normalizar_texto(self.fecha_formulario)
        self.area = _normalizar_texto(self.area)
        self.maquina = _normalizar_texto(self.maquina)
        self.cod_recurso = _normalizar_texto(self.cod_recurso)
        self.cod_setor = _normalizar_texto(self.cod_setor)
        self.operario = _normalizar_texto(self.operario)
        self.estacion = _normalizar_texto(self.estacion)
        self.evento_origen = _normalizar_texto(self.evento_origen)
        self.estado = _normalizar_estado(self.estado)
        self.descripcion_op = _normalizar_texto(self.descripcion_op)
        self.descripcion_proceso = _normalizar_texto(self.descripcion_proceso)
        self.observacion_general = _normalizar_texto(self.observacion_general)
        self.fecha_creacion = _normalizar_texto(self.fecha_creacion)
        self.fecha_actualizacion = _normalizar_texto(self.fecha_actualizacion)
        self.id_plantilla_preguntas = _normalizar_texto(self.id_plantilla_preguntas)

        self.turno = _serializar_valor(self.turno)
        self.hora_fim = _serializar_valor(self.hora_fim)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Formulario":
        return cls(
            id_formulario=data.get("id_formulario", ""),
            identificador=data.get("identificador", ""),
            id_apontamento=data.get("id_apontamento", ""),
            fecha_formulario=data.get("fecha_formulario", ""),
            area=data.get("area", ""),
            maquina=data.get("maquina", ""),
            cod_recurso=data.get("cod_recurso", ""),
            cod_setor=data.get("cod_setor", ""),
            turno=data.get("turno"),
            hora_fim=data.get("hora_fim"),
            operario=data.get("operario", ""),
            estacion=data.get("estacion", ""),
            evento_origen=data.get("evento_origen", ""),
            estado=data.get("estado", ESTADO_EN_APERTURA),
            descripcion_op=data.get("descripcion_op", ""),
            descripcion_proceso=data.get("descripcion_proceso", ""),
            observacion_general=data.get("observacion_general", ""),
            fecha_creacion=data.get("fecha_creacion", ""),
            fecha_actualizacion=data.get("fecha_actualizacion", ""),
            id_plantilla_preguntas=data.get("id_plantilla_preguntas", ""),
            version_plantilla_preguntas=int(
                data.get("version_plantilla_preguntas", 0) or 0
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_formulario": self.id_formulario,
            "identificador": self.identificador,
            "id_apontamento": self.id_apontamento,
            "fecha_formulario": self.fecha_formulario,
            "area": self.area,
            "maquina": self.maquina,
            "cod_recurso": self.cod_recurso,
            "cod_setor": self.cod_setor,
            "turno": _serializar_valor(self.turno),
            "hora_fim": _serializar_valor(self.hora_fim),
            "operario": self.operario,
            "estacion": self.estacion,
            "evento_origen": self.evento_origen,
            "estado": _normalizar_estado(self.estado),
            "descripcion_op": self.descripcion_op,
            "descripcion_proceso": self.descripcion_proceso,
            "observacion_general": self.observacion_general,
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion,
            "id_plantilla_preguntas": self.id_plantilla_preguntas,
            "version_plantilla_preguntas": self.version_plantilla_preguntas,
        }

    def actualizar(self, cambios: dict[str, Any]) -> None:
        for clave, valor in cambios.items():
            if hasattr(self, clave):
                setattr(self, clave, valor)
        self.__post_init__()

    def get(self, clave: str, default: Any = None) -> Any:
        return getattr(self, clave, default)
